from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

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
)
from fmu.pem.pem_utilities.enum_defs import CO2Models, FluidMixModel, TemperatureMethod
from fmu.pem.pem_utilities.fipnum_pvtnum_utilities import (
    input_num_string_to_list,
    validate_zone_coverage,
)

if TYPE_CHECKING:
    from fmu.pem.pem_utilities.pem_config_validation import PVTZone

if INTERNAL_EQUINOR:
    from rock_physics_open.fluid_models import (
        saturations_below_bubble_point,  # noqa: F821
    )


def _saturation_triplet(
    sw: np.ma.MaskedArray, sg: np.ma.MaskedArray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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


def _adjust_bubble_point(
    pres: np.ndarray,
    gor: np.ndarray,
    sw: np.ndarray,
    sg: np.ndarray,
    so: np.ndarray,
    temp: np.ndarray,
    oil_density_ref: np.ndarray,
    oil_gas_gravity: np.ndarray,
    free_gas_gravity: np.ndarray,
    zone: PVTZone,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
                z_factor=zone.gas_z_factor,
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
    zone: PVTZone,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate brine properties by FLAG or Batzle & Wang model."""
    p_na = np.array(zone.brine.perc_na)
    p_ca = np.array(zone.brine.perc_ca)
    p_k = np.array(zone.brine.perc_k)
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
    zone: PVTZone,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate gas properties by FLAG or Batzle & Wang and co2 properties by
    FLAG or Span & Wagner model."""
    if zone.gas_saturation_is_co2:
        if zone.co2_model == CO2Models.FLAG and INTERNAL_EQUINOR:
            vp, rho, bulk = flag.co2_properties(  # noqa: F821
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
            model=zone.gas.model,
        )[0:3]
    return rho, bulk, vp


def _apply_condensate_if_any(
    rv: np.ndarray | None,
    temp: np.ndarray,
    pres: np.ndarray,
    zone: PVTZone,
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
    if not (zone.calculate_condensate and rv is not None and INTERNAL_EQUINOR):
        return
    idx_dry = np.isclose(rv, 0.0, atol=1e-10)
    if np.all(idx_dry):
        return
    cond = zone.condensate
    cond_gor = 1.0 / rv[~idx_dry]
    cond_gr = cond.gas_gravity * np.ones_like(cond_gor)
    cond_rho0 = cond.reference_density * np.ones_like(cond_gor)
    if rv is not None and temp is not None and pres is not None:
        vp_c, rho_c, bulk_c = flag.condensate_properties(  # noqa: F821
            temperature=temp[~idx_dry],
            pressure=pres[~idx_dry],
            rho0=cond_rho0,
            gas_oil_ratio=cond_gor,
            gas_gravity=cond_gr,
        )
        gas_rho[~idx_dry] = rho_c
        gas_bulk[~idx_dry] = bulk_c
        gas_vp[~idx_dry] = vp_c
    else:
        raise ValueError(
            "Condensate properties calculation requires non-null `rv`, `temp`, and "
            "`pres`."
        )


def _mix(
    sw: np.ndarray,
    sg: np.ndarray,
    so: np.ndarray,
    rho_w: np.ndarray,
    bulk_w: np.ndarray,
    rho_g: np.ndarray,
    bulk_g: np.ndarray,
    rho_o: np.ndarray,
    bulk_o: np.ndarray,
    method: FluidMixModel,
    brie_exponent: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Selects the fluid mixing function based on the `fluid_mix_method` input parameter.
    If `fluid_mix_method` is set to WOOD, the Wood mixing function is used.
    Otherwise, the Brie mixing function is used by default.
    """
    if method == FluidMixModel.WOOD:
        bulk_eff = multi_wood([sw, sg, so], [bulk_w, bulk_g, bulk_o])  # type: ignore
    else:
        bulk_eff = brie(
            sg,
            bulk_g,
            sw,
            bulk_w,
            so,
            bulk_o,
            brie_exponent,
        )
    rho_eff = sw * rho_w + sg * rho_g + so * rho_o
    return rho_eff, bulk_eff


def effective_fluid_properties_zoned(
    restart_props: list[SimRstProperties] | SimRstProperties,
    fluids: Fluids,
    pvtnum: np.ma.MaskedArray,
) -> list[EffectiveFluidProperties]:
    """
    Compute per time-step effective fluid density and bulk modulus honoring PVT zone
    groupings.

    Steps:
      1. Normalize `restart_props` to a list.
      2. Validate PVT zone coverage (single wildcard '*' or explicit non-overlapping
         sets).
      3. Build mapping from grid PVTNUM values to zone indices.
      4. For each time-step:
         a. Initialize result arrays with NaN (masked/inactive cells untouched).
         b. Loop zone values, select cells, extract saturations, pressure, GOR,
            salinity, temperature.
         c. Apply bubble point adjustment (may release solution gas and modify GOR &
            free gas gravity).
         d. Compute phase properties (brine, oil, gas or CO₂).
         e. Overwrite gas properties where condensate present (RV > 0) if enabled and
            proprietary model available.
         f. Mix phase properties using Wood or Brie model.
         g. Insert zone results into full-grid arrays.
      5. Collect `EffectiveFluidProperties` objects for all time-steps.

    Args:
        restart_props (list[SimRstProperties] | SimRstProperties): One or more restart
            property containers holding phase saturations (`swat`, `sgas`), pressure,
            gas-oil ratio (`rs`), optional condensate ratio (`rv`), and (if modeled)
            temperature / salinity.
        fluids (Fluids): Fluid configuration including per-zone parameters (brine, oil,
            gas, condensate flags), mixing method, and model selections.
        pvtnum (np.ma.MaskedArray): Masked array of PVTNUM integers defining zone
            partitioning on the simulation grid (masked cells are inactive).

    Returns:
        list[EffectiveFluidProperties]: Ordered list matching input time-step order.
        Each element contains:
            density (np.ndarray): Effective fluid density (kg/m³) per active cell.
            bulk_modulus (np.ndarray): Effective fluid bulk modulus (Pa) per active
            cell.

    Raises:
        ValueError: If PVT zone definitions overlap, have uncovered grid values, misuse
            wildcard '*', or condensate calculation is requested but `rv` is missing.
        NotImplementedError: If condensate modeling is requested without proprietary
            implementation (`INTERNAL_EQUINOR` is False), or bubble point evolution
            depends on an unavailable model.
        RuntimeError: If array shape mismatches prevent assignment to result arrays.
        TypeError: If input types do not conform to expected models / masked arrays.

    Notes:
        - Salinity and temperature are sourced from simulation only if corresponding
          flags are set; otherwise zone constants are used.
        - Condensate overwrite operates in-place on gas property arrays.
        - Inactive (masked) cells retain NaN in outputs to preserve grid masking.
    """
    # Validate zone coverage
    pvtnum_strings: list[str] = [zone.pvtnum for zone in fluids.pvt_zones]  # type: ignore
    validate_zone_coverage(pvtnum_strings, pvtnum, zone_name="PVTNUM")

    # Normalize input to list
    props_list = restart_props if isinstance(restart_props, list) else [restart_props]

    # Get actual PVTNUM values present in grid for use with input_num_string_to_list
    # The PVTNUM mask from the INIT file will be the same as the mask from UNRST file
    # for all dates
    pvtnum_data = pvtnum.data
    pvtnum_mask = (
        pvtnum.mask
        if hasattr(pvtnum, "mask")
        else np.zeros_like(pvtnum_data, dtype=bool)
    )
    actual_pvtnum_values = list(np.unique(pvtnum_data[~pvtnum_mask]).astype(int))

    # Allocate outputs
    results: list[EffectiveFluidProperties] = []

    for rst_date_prop in props_list:
        # Initialize masked result arrays
        rho_eff_full = np.ma.masked_array(
            np.full(rst_date_prop.swat.shape, np.nan, dtype=float), mask=pvtnum_mask
        )
        bulk_eff_full = np.ma.masked_array(
            np.full(rst_date_prop.swat.shape, np.nan, dtype=float), mask=pvtnum_mask
        )

        # Process each unique zone (may contain multiple PVTNUMs grouped)
        for zone in fluids.pvt_zones:
            # Get all PVTNUM values for this zone using input_num_string_to_list
            pvtnum_values = input_num_string_to_list(zone.pvtnum, actual_pvtnum_values)

            # Build combined mask for all PVTNUMs in this zone using vectorized
            # operation
            mask_cells = np.isin(pvtnum_data, pvtnum_values) & (~pvtnum_mask)

            if not np.any(mask_cells):
                continue

            # Extract saturations, pressure, GOR, etc. (placeholder for existing logic)
            sw = rst_date_prop.swat[mask_cells]
            sg = rst_date_prop.sgas[mask_cells]
            sw, sg, so = _saturation_triplet(sw, sg)
            pres = rst_date_prop.pressure[mask_cells]
            gor = rst_date_prop.rs[mask_cells]

            # Salinity
            if (
                fluids.salinity_from_sim
                and hasattr(rst_date_prop, "salt")
                and rst_date_prop.salt is not None
            ):
                sal = rst_date_prop.salt[mask_cells]
            else:
                sal = np.full(sw.shape, zone.brine.salinity)

            # Temperature
            if (
                zone.temperature.type == TemperatureMethod.FROMSIM
                and hasattr(rst_date_prop, "temp")
                and rst_date_prop.temp is not None
            ):
                temp = rst_date_prop.temp[mask_cells]
            else:
                temp = np.full(sw.shape, zone.temperature.temperature_value)

            # RV (condensate)
            rv = (
                rst_date_prop.rv[mask_cells]
                if (
                    zone.calculate_condensate
                    and hasattr(rst_date_prop, "rv")
                    and rst_date_prop.rv is not None
                )
                else None
            )

            # Expand scalars to numpy arrays for fluid properties
            oil_dens = np.full(sw.shape, zone.oil.reference_density, dtype=float)
            oil_gas_grav = np.full(sw.shape, zone.oil.gas_gravity, dtype=float)
            gas_gravity = np.full(sw.shape, zone.gas.gas_gravity, dtype=float)

            # Bubble point adjustment
            sw, sg, so, gor, gas_gravity = _adjust_bubble_point(
                pres=pres,
                gor=gor,
                sw=sw,
                sg=sg,
                so=so,
                temp=temp,
                oil_density_ref=oil_dens,
                oil_gas_gravity=oil_gas_grav,
                free_gas_gravity=gas_gravity,
                zone=zone,
            )

            # Phase properties
            rho_w, bulk_w, _ = _brine_props(temp, pres, sal, zone)
            rho_o, bulk_o, _ = _oil_props(temp, pres, gor, oil_dens, oil_gas_grav)
            rho_g, bulk_g, vp_g = _gas_or_co2_props(temp, pres, gas_gravity, zone)

            # Condensate overwrite (in-place)
            _apply_condensate_if_any(
                rv=rv,
                temp=temp,
                pres=pres,
                zone=zone,
                gas_rho=rho_g,
                gas_bulk=bulk_g,
                gas_vp=vp_g,
            )

            # Mix phases

            brie_exponent = (
                fluids.fluid_mix_method.brie_exponent
                if hasattr(fluids.fluid_mix_method, "brie_exponent")
                else None
            )
            rho_mix, bulk_mix = _mix(
                sw=sw,
                sg=sg,
                so=so,
                rho_w=rho_w,
                bulk_w=bulk_w,
                rho_g=rho_g,
                bulk_g=bulk_g,
                rho_o=rho_o,
                bulk_o=bulk_o,
                method=fluids.fluid_mix_method.method,
                brie_exponent=brie_exponent,
            )

            # Assign into masked arrays (preserve mask)
            rho_eff_full.data[mask_cells] = rho_mix
            bulk_eff_full.data[mask_cells] = bulk_mix

        results.append(
            EffectiveFluidProperties(density=rho_eff_full, bulk_modulus=bulk_eff_full)
        )

    return results
