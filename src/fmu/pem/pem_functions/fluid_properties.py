from __future__ import annotations

import warnings
from typing import TypeAlias

import numpy as np
from rock_physics_open import fluid_models as flag
from rock_physics_open import span_wagner
from rock_physics_open.equinor_utilities.std_functions import brie, multi_wood
from rock_physics_open.fluid_models.oil_model.oil_bubble_point import bp_standing

from fmu.pem import INTERNAL_EQUINOR
from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    Fluids,
    SimRstProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import CO2Models, FluidMixModel, TemperatureMethod

if INTERNAL_EQUINOR:
    from rock_physics_open.fluid_models import saturations_below_bubble_point

PrepareArraysReturn: TypeAlias = tuple[
    np.ma.MaskedArray,  # sw
    np.ma.MaskedArray,  # sg
    np.ma.MaskedArray,  # so
    np.ndarray,  # gor
    np.ndarray,  # pres
    np.ndarray,  # salinity
    np.ndarray,  # temp
    np.ndarray,  # gas_gravity (may be modified later)
    np.ndarray | None,  # rv (None if not present)
    np.ndarray | None,  # mask (None if no filtering)
    np.ndarray,  # oil_density_ref
    np.ndarray,  # oil_gas_gravity
]


def _verify_inputs(
    inp: list[SimRstProperties] | SimRstProperties,
) -> list[SimRstProperties]:
    """Return list of SimRstProperties (accepts single instance)."""
    if isinstance(inp, SimRstProperties):
        return [inp]
    if isinstance(inp, list) and all(isinstance(p, SimRstProperties) for p in inp):
        return inp
    raise ValueError(
        f"Input must be SimRstProperties or list[SimRstProperties], is {type(inp)}."
    )


def _saturation_triplet(
    sw: np.ma.MaskedArray, sg: np.ma.MaskedArray
) -> tuple[np.ma.MaskedArray, ...]:
    """Clip water/gas and derive oil saturation; renormalize if sum exceeds 1."""
    sw = np.ma.MaskedArray(np.ma.clip(sw, 0.0, 1.0))
    sg = np.ma.MaskedArray(np.ma.clip(sg, 0.0, 1.0))
    # sw and sg come from the same grid, and will have the same mask, so there
    # should be no need for special handling of possible different masks
    s_sum = np.ma.max(sw + sg)
    if s_sum > 1.0:  # renormalize if overlapping
        sw /= s_sum
        sg /= s_sum
    so = 1.0 - sw - sg
    return sw, sg, so


def _prepare_arrays(
    prop: SimRstProperties,
    fluids: Fluids,
) -> PrepareArraysReturn:
    """Collect and shape per-cell arrays; apply 1-D filtering.
    Returns (sw, sg, so, gor, pres, salinity, temp, gas_gravity, rv, mask,
    oil_density_ref, oil_gas_gravity).
    """
    sw, sg, so = _saturation_triplet(prop.swat, prop.sgas)
    gor = prop.rs
    pres = 1.0e5 * prop.pressure  # bar -> Pa

    # Check if salinity and temperature should come from simulator model,
    # use constant values as fallback
    if fluids.salinity_from_sim and prop.salt is not None:
        salinity = 1000.0 * prop.salt
    else:
        salinity = to_masked_array(fluids.brine.salinity, sw)

    if fluids.temperature.type == TemperatureMethod.FROMSIM:
        if not hasattr(prop, "temp") or prop.temp is None:
            raise ValueError(
                "Eclipse simulation restart file does not have temperature attribute. "
                "Constant temperature must be set in parameter file."
            )
        temp = prop.temp
    else:
        temp = to_masked_array(fluids.temperature.temperature_value, sw)

    if isinstance(fluids.gas.gas_gravity, float):
        gas_gravity = to_masked_array(fluids.gas.gas_gravity, sw)
    else:
        gas_gravity = fluids.gas.gas_gravity

    # There is always an "rv" attribute in SimRstProperties, but it can be None
    if prop.rv is not None:
        mask, sw, sg, so, gor, pres, rv, salinity, temp, gas_gravity = (
            filter_and_one_dim(
                sw, sg, so, gor, pres, prop.rv, salinity, temp, gas_gravity
            )
        )
    else:
        mask, sw, sg, so, gor, pres, salinity, temp = filter_and_one_dim(
            sw, sg, so, gor, pres, salinity, temp
        )
        rv = None

    oil_density_ref = fluids.oil.reference_density * np.ones_like(sw)
    oil_gas_gravity = fluids.oil.gas_gravity * np.ones_like(sw)

    return (
        sw,
        sg,
        so,
        gor,
        pres,
        salinity,
        temp,
        gas_gravity,
        rv,
        mask,
        oil_density_ref,
        oil_gas_gravity,
    )


def _adjust_bubble_point(
    pres: np.ndarray,
    gor: np.ndarray,
    sw: np.ma.MaskedArray,
    sg: np.ma.MaskedArray,
    so: np.ma.MaskedArray,
    temp: np.ndarray,
    oil_density_ref: np.ndarray,
    oil_gas_gravity: np.ndarray,
    free_gas_gravity: np.ndarray,
    fluids: Fluids,
) -> tuple[
    np.ma.MaskedArray, np.ma.MaskedArray, np.ma.MaskedArray, np.ndarray, np.ndarray
]:
    """
    If we are below bubble point, gas will come out of solution, and this has
    to be taken into account

    If below bubble point: evolve saturations, GOR and free gas gravity."""
    try:
        bp = bp_standing(
            density=oil_density_ref,
            gas_oil_ratio=gor,
            gas_gravity=oil_gas_gravity,
            temperature=temp,
        )
        idx_below = pres <= bp
        if np.any(idx_below):
            warnings.warn(
                f"Detected pressure below bubble point for oil in "
                f"{np.sum(idx_below)} cells"
            )
    except NotImplementedError:
        warnings.warn("Bubble point function unavailable; assuming above bubble point.")
        idx_below = np.zeros_like(pres, dtype=bool)

    if np.any(idx_below):
        try:
            sg, so, gor, free_gas_gravity = saturations_below_bubble_point(
                gas_saturation_init=sg,
                oil_saturation_init=so,
                brine_saturation_init=sw,
                gor_init=gor,
                oil_gas_gravity=oil_gas_gravity,
                free_gas_gravity=free_gas_gravity,
                oil_density=oil_density_ref,
                z_factor=fluids.gas_z_factor,
                pres_depl=pres,
                temp_res=temp,
            )
        except (NameError, ModuleNotFoundError, NotImplementedError):
            warnings.warn(
                "Estimation of oil properties below bubble point requires proprietary "
                "model. Estimation of oil properties below bubble point are uncertain."
            )
    return sw, sg, so, gor, free_gas_gravity


def _brine_props(
    temp: np.ndarray,
    pres: np.ndarray,
    salinity: np.ndarray,
    fluids: Fluids,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate brine properties by FLAG or Batzle & Wang model."""
    p_na = np.array(fluids.brine.perc_na)
    p_ca = np.array(fluids.brine.perc_ca)
    p_k = np.array(fluids.brine.perc_k)
    vp, rho, bulk = flag.brine_properties(
        temperature=temp,
        pressure=pres,
        salinity=salinity,
        p_nacl=p_na,
        p_cacl=p_ca,
        p_kcl=p_k,
    )
    return rho, bulk, vp


def _oil_props(
    temp: np.ndarray,
    pres: np.ndarray,
    gor: np.ndarray,
    fluids: Fluids,
    oil_density_ref: np.ndarray,
    oil_gas_gravity: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate oil properties by FLAG or Batzle & Wang model."""
    vp, rho, bulk = flag.oil_properties(
        temperature=temp,
        pressure=pres,
        gas_gravity=oil_gas_gravity,
        rho0=oil_density_ref,
        gas_oil_ratio=gor,
    )
    return rho, bulk, vp


def _gas_or_co2_props(
    temp: np.ndarray,
    pres: np.ndarray,
    gas_gravity: np.ndarray,
    fluids: Fluids,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate gas properties by FLAG or Batzle & Wang and co2 properties by
    FLAG or Span & Wagner model."""
    if fluids.gas_saturation_is_co2:
        if fluids.co2_model == CO2Models.FLAG and INTERNAL_EQUINOR:
            vp, rho, bulk = flag.co2_properties(  # noqa: F821
                # Only available if INTERNAL_EQUINOR is True
                temp=temp,
                pres=pres,
            )
        else:
            vp, rho, bulk = span_wagner.co2_properties(
                temp=temp,
                pres=pres,
            )
    else:
        vp, rho, bulk = flag.gas_properties(
            temperature=temp,
            pressure=pres,
            gas_gravity=gas_gravity,
            model=fluids.gas.model,
        )[0:3]
    return rho, bulk, vp


def _apply_condensate_if_any(
    rv: np.ndarray | None,
    temp: np.ndarray,
    pres: np.ndarray,
    fluids: Fluids,
    gas_rho: np.ndarray,
    gas_bulk: np.ndarray,
    gas_vp: np.ndarray,
) -> None:
    """
    Overwrite gas properties where condensate is present (rv > 0).

    To be overly clear: Modifies gas_rho, gas_bulk, and gas_vp arrays in-place,
    returns None.

    The RV parameter is used to calculate condensate properties, but the inverse
    property (GOR) which is used as an input to the FLAG module, is Inf if RV is
    0.0. An RV of 0.0 means that the gas is dry, which is already calculated
    NB: condensate properties calculation requires proprietary model
    """
    if not (fluids.calculate_condensate and rv is not None and INTERNAL_EQUINOR):
        return
    idx_dry = np.isclose(rv, 0.0, atol=1e-10)
    if np.all(idx_dry):
        return
    cond = fluids.condensate
    cond_gor = 1.0 / rv[~idx_dry]
    cond_gr = cond.gas_gravity * np.ones_like(cond_gor)
    cond_rho0 = cond.reference_density * np.ones_like(cond_gor)
    vp_c, rho_c, bulk_c = flag.condensate_properties(  # noqa  F821
        temperature=temp[~idx_dry],
        pressure=pres[~idx_dry],
        rho0=cond_rho0,
        gas_oil_ratio=cond_gor,
        gas_gravity=cond_gr,
    )
    gas_rho[~idx_dry] = rho_c
    gas_bulk[~idx_dry] = bulk_c
    gas_vp[~idx_dry] = vp_c


def _mix(
    sw: np.ma.MaskedArray,
    sg: np.ma.MaskedArray,
    so: np.ma.MaskedArray,
    rho_w: np.ndarray,
    bulk_w: np.ndarray,
    rho_g: np.ndarray,
    bulk_g: np.ndarray,
    rho_o: np.ndarray,
    bulk_o: np.ndarray,
    fluids: Fluids,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Selects the fluid mixing function based on the `fluid_mix_method` input parameter.
    If `fluid_mix_method` is set to WOOD, the Wood mixing function is used.
    Otherwise, the Brie mixing function is used by default.
    """
    if fluids.fluid_mix_method == FluidMixModel.WOOD:
        bulk_eff = multi_wood([sw, sg, so], [bulk_w, bulk_g, bulk_o])  # type: ignore
    else:
        bulk_eff = brie(
            sg,
            bulk_g,
            sw,
            bulk_w,
            so,
            bulk_o,
            fluids.fluid_mix_method.brie_exponent,
        )
    rho_eff = sw * rho_w + sg * rho_g + so * rho_o
    return rho_eff, bulk_eff


def effective_fluid_properties(
    restart_props: list[SimRstProperties] | SimRstProperties,
    fluid_params: Fluids,
) -> list[EffectiveFluidProperties]:
    """
    Compute effective fluid density and bulk modulus for each simulation time step.

    Parameters
    ----------
    restart_props : list[SimRstProperties] or SimRstProperties
        Simulation restart properties for one or more time steps. Contains phase
        saturations, pressure, temperature, GOR, salinity, gas gravity, and other
        relevant properties.
    fluid_params : Fluids
        Fluid parameters and configuration, including mixing method, brine/oil/gas
        models, and bubble point handling options.
    Returns
    -------
    props : list[EffectiveFluidProperties]
        List of effective fluid properties (density and bulk modulus) for each time
        step.
        Each entry is an EffectiveFluidProperties object with fields:
            - density: np.ndarray
            - bulk_modulus: np.ndarray
    Notes
    -----
    Bubble point handling:
        If the pressure is below the oil bubble point, the function adjusts saturations,
        GOR, and gas gravity to reflect phase changes (liberation of gas from oil).
        This ensures physically consistent fluid properties in undersaturated and
        saturated conditions.
    """
    props = []
    for prop in _verify_inputs(restart_props):
        (
            sw,
            sg,
            so,
            gor,
            pres,
            salinity,
            temp,
            gas_gravity,
            rv,
            mask,
            oil_density_ref,
            oil_gas_gravity,
        ) = _prepare_arrays(prop, fluid_params)

        # Bubble point adjustment (may alter saturations, GOR, gas gravity)
        sw, sg, so, gor, gas_gravity = _adjust_bubble_point(
            pres,
            gor,
            sw,
            sg,
            so,
            temp,
            oil_density_ref,
            oil_gas_gravity,
            gas_gravity,
            fluid_params,
        )

        # Calculate the fluid properties for each fluid phase
        rho_w, bulk_w, _vp_w = _brine_props(temp, pres, salinity, fluid_params)
        rho_o, bulk_o, _vp_o = _oil_props(
            temp, pres, gor, fluid_params, oil_density_ref, oil_gas_gravity
        )
        rho_g, bulk_g, vp_g = _gas_or_co2_props(temp, pres, gas_gravity, fluid_params)

        # Moderate gas by condensate properties if applicable
        _apply_condensate_if_any(rv, temp, pres, fluid_params, rho_g, bulk_g, vp_g)

        # Mix phases according to selected mixing function
        rho_eff, bulk_eff = _mix(
            sw, sg, so, rho_w, bulk_w, rho_g, bulk_g, rho_o, bulk_o, fluid_params
        )

        # Restore original size
        rho_eff, bulk_eff = reverse_filter_and_restore(mask, rho_eff, bulk_eff)

        # Add to list of properties (per simulation date)
        props.append(EffectiveFluidProperties(density=rho_eff, bulk_modulus=bulk_eff))
    return props
