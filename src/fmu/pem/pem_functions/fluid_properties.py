# pylint: disable=missing-module-docstring
import warnings

import numpy as np
from rock_physics_open import fluid_models as flag
from rock_physics_open import span_wagner
from rock_physics_open.equinor_utilities.std_functions import brie, multi_wood

from fmu.pem import INTERNAL_EQUINOR

if INTERNAL_EQUINOR:
    from rock_physics_open.fluid_models import (
        saturations_below_bubble_point,  # pylint: disable=import-error
    )

from rock_physics_open.fluid_models.oil_model.oil_bubble_point import bp_standing

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    Fluids,
    SimRstProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import CO2Models, FluidMixModel, TemperatureMethod


def effective_fluid_properties(
    restart_props: list[SimRstProperties] | SimRstProperties,
    fluid_params: Fluids,
) -> list[EffectiveFluidProperties]:
    """effective_fluid_properties
    Calculate effective fluid properties (bulk modulus, density) from a fluid mix.

    6/1-25: Now also incorporating fluid properties in the case where the formation
    pressure is below the oil bubble point.

    Parameters
    ----------
    restart_props :
        list of dicts or a single dict with saturation, GOR and pressure per
        time step
    fluid_params : Fluids class
        parameter set containing fluid parameters for FLAG models

    Returns
    -------
    list
        fluid properties (bulk modulus and density) per time step
    """
    restart_props = _verify_inputs(restart_props)
    prop_list = []
    for prop in restart_props:
        # Initial check of saturation for gas and brine and calculation of oil
        # saturation
        sat_wat, sat_gas, sat_oil = _saturation_check(prop.swat, prop.sgas)

        # RS is one of the required properties from the restart file. If it is not
        # present, an error will be raised during file import.
        gor = prop.rs

        fluid_keys = ("vp", "density", "bulk_modulus")

        # Convert pressure from bar to Pa
        pres = 1.0e5 * prop.pressure

        # Salinity and temperature are either taken as constants from config file or
        # from eclipse simulator model
        if fluid_params.salinity_from_sim:
            # Convert from ppk to ppm
            salinity = 1000.0 * prop.salt
        else:
            salinity = to_masked_array(fluid_params.brine.salinity, sat_wat)
        # Temperature will normally be set as a constant. It can come from eclipse in
        # the case a compositional fluid model is run.
        if fluid_params.temperature.type == TemperatureMethod.FROMSIM:
            if hasattr(prop, "temp") and prop.temp is not None:
                temp = prop.temp
            else:
                raise ValueError(
                    "eclipse simulation restart file does not have "
                    "temperature attribute. Constant temperature must "
                    "be set in parameter file"
                )
        else:
            temp = to_masked_array(fluid_params.temperature.temperature_value, sat_wat)

        # Gas gravity has to be expanded to a masked array if it comes as a float
        if isinstance(fluid_params.gas.gas_gravity, float):
            gas_gravity = to_masked_array(fluid_params.gas.gas_gravity, sat_wat)
        else:
            gas_gravity = fluid_params.gas.gas_gravity

        if hasattr(prop, "rv"):
            (
                mask,
                sat_wat,
                sat_gas,
                sat_oil,
                gor,
                pres,
                rv,
                salinity,
                temp,
                gas_gravity,
            ) = filter_and_one_dim(
                sat_wat,
                sat_gas,
                sat_oil,
                gor,
                pres,
                prop.rv,
                salinity,
                temp,
                gas_gravity,
            )
        else:
            (
                mask,
                sat_wat,
                sat_gas,
                sat_oil,
                gor,
                pres,
                salinity,
                temp,
            ) = filter_and_one_dim(sat_wat, sat_gas, sat_oil, gor, pres, salinity, temp)
            rv = None

        # Brine
        brine_par = fluid_params.brine
        p_na = np.array(brine_par.perc_na)
        p_ca = np.array(brine_par.perc_ca)
        p_k = np.array(brine_par.perc_k)
        brine_props = flag.brine_properties(
            temp, pres, salinity, p_nacl=p_na, p_cacl=p_ca, p_kcl=p_k
        )
        brine = dict(zip(fluid_keys, brine_props))

        # Oil
        oil_par = fluid_params.oil
        oil_gr = oil_par.gas_gravity * np.ones_like(sat_wat)
        oil_density = oil_par.reference_density * np.ones_like(sat_wat)

        # If we are below bubble point, gas will come out of solution, and this has
        # to be taken into account
        try:
            idx_below_bubble_point = pres <= bp_standing(oil_density, gor, oil_gr, temp)
            if np.any(~idx_below_bubble_point):
                warnings.warn(
                    f"Detected pressure below bubble point for oil in "
                    f"{np.sum(~idx_below_bubble_point)} cells"
                )
        except NotImplementedError:
            # If the function is not available, a case above bubble point is assumed
            warnings.warn(
                "Function for bubble point not implemented. Conditions above "
                "bubble point is assumed."
            )
            idx_below_bubble_point = np.zeros_like(sat_wat)
        try:
            if np.any(idx_below_bubble_point):
                sat_gas, sat_oil, gor, gas_gravity = saturations_below_bubble_point(
                    gas_saturation_init=sat_gas,
                    oil_saturation_init=sat_oil,
                    brine_saturation_init=sat_wat,
                    gor_init=gor,
                    oil_gas_gravity=oil_gr,
                    free_gas_gravity=gas_gravity,
                    oil_density=oil_density,
                    z_factor=fluid_params.gas_z_factor,
                    pres_depl=pres,
                    temp_res=temp,
                )
        except (ModuleNotFoundError, NotImplementedError):
            warnings.warn(
                "Function to calculate effective fluid properties below "
                "bubble point is not implemented. Estimates of fluid "
                "properties may be uncertain."
            )

        oil_props = flag.oil_properties(
            temperature=temp,
            pressure=pres,
            gas_gravity=oil_gr,
            rho0=oil_density,
            gas_oil_ratio=gor,
        )
        oil = dict(zip(fluid_keys, oil_props))

        # Gas, condensate or CO2 - select case based on CO2 flag or presence of RV
        # property in the Eclipse restart file

        if fluid_params.gas_saturation_is_co2:
            if fluid_params.co2_model == CO2Models.FLAG and INTERNAL_EQUINOR:
                gas_props = flag.co2_properties(temp=temp, pres=pres)
            else:
                gas_props = span_wagner.co2_properties(temp=temp, pres=pres)
        else:
            gas_par = fluid_params.gas
            gas_gr = gas_gravity
            gas_model = gas_par.model
            gas_props = flag.gas_properties(temp, pres, gas_gr, model=gas_model)[0:3]
        # The RV parameter is used to calculate condensate properties, but the inverse
        # property (GOR) which is used as an input to the FLAG module, is Inf if RV is
        # 0.0. An RV of 0.0 means that the gas is dry, which is already calculated
        # NB: condensate properties calculation requires proprietary model
        if fluid_params.calculate_condensate and (rv is not None) and INTERNAL_EQUINOR:
            cond_par = fluid_params.condensate
            idx_rv_zero = np.isclose(rv, 0.0, atol=1e-10)
            if np.any(~idx_rv_zero) and INTERNAL_EQUINOR:
                cond_gor = 1.0 / rv[~idx_rv_zero]
                cond_gr = cond_par.gas_gravity * np.ones_like(cond_gor)
                cond_density = cond_par.reference_density * np.ones_like(cond_gor)
                cond_props = flag.condensate_properties(
                    temperature=temp[~idx_rv_zero],
                    pressure=pres[~idx_rv_zero],
                    rho0=cond_density,
                    gas_oil_ratio=cond_gor,
                    gas_gravity=cond_gr,
                )
                for i in range(len(gas_props)):
                    gas_props[i][~idx_rv_zero] = cond_props[i]

        gas = dict(zip(fluid_keys, gas_props))

        if fluid_params.fluid_mix_method == FluidMixModel.WOOD:
            mixed_fluid_bulk_modulus = multi_wood(
                [sat_wat, sat_gas, sat_oil],
                [brine["bulk_modulus"], gas["bulk_modulus"], oil["bulk_modulus"]],
            )
        else:
            mixed_fluid_bulk_modulus = brie(
                sat_gas,
                gas["bulk_modulus"],
                sat_wat,
                brine["bulk_modulus"],
                sat_oil,
                oil["bulk_modulus"],
                fluid_params.fluid_mix_method.brie_exponent,
            )
        mixed_fluid_density = (
            sat_wat * brine["density"]
            + sat_gas * gas["density"]
            + sat_oil * oil["density"]
        )
        mixed_fluid_density, mixed_fluid_bulk_modulus = reverse_filter_and_restore(
            mask, mixed_fluid_density, mixed_fluid_bulk_modulus
        )
        fluid_props = EffectiveFluidProperties(
            density=mixed_fluid_density,
            bulk_modulus=mixed_fluid_bulk_modulus,
        )
        prop_list.append(fluid_props)
    return prop_list


def _saturation_check(
    s_water: np.ma.MaskedArray, s_gas: np.ma.MaskedArray
) -> tuple[np.ma.MaskedArray, ...]:
    s_water = np.ma.MaskedArray(np.ma.clip(s_water, 0.0, 1.0))
    s_gas = np.ma.MaskedArray(np.ma.clip(s_gas, 0.0, 1.0))
    max_water_gas_factor = np.ma.max(s_water + s_gas)
    if max_water_gas_factor > 1.0:
        s_water /= max_water_gas_factor
        s_gas /= max_water_gas_factor
    s_oil = 1.0 - s_water - s_gas
    return s_water, s_gas, s_oil  # type: ignore


def _verify_inputs(
    inp_props: list[SimRstProperties] | SimRstProperties,
) -> list[SimRstProperties]:
    if isinstance(inp_props, list):
        if not all(isinstance(prop, SimRstProperties) for prop in inp_props):
            raise ValueError(
                f"{__file__}: input to effective fluid properties should be list of "
                f"SimRstProperties or a single SimRstProperties instance, "
                f"is {[type(prop) for prop in inp_props]}"
            )
        return inp_props
    raise ValueError(
        f"{__file__}: input to effective fluid properties should be list of "
        f"SimRstProperties or a single SimRstProperties instance, is {type(inp_props)}"
    )
