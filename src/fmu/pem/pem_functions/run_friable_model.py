from dataclasses import asdict

import numpy as np
from rock_physics_open.equinor_utilities.std_functions import (
    gassmann,
    velocity,
)
from rock_physics_open.sandstone_models import friable_model_dry

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    RockMatrixProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)
from fmu.pem.pem_utilities.enum_defs import (
    ParameterTypes,
)

from .pressure_sensitivity import apply_dry_rock_pressure_sensitivity_model


def run_friable(
    mineral: EffectiveMineralProperties,
    fluid: list[EffectiveFluidProperties] | EffectiveFluidProperties,
    porosity: np.ma.MaskedArray,
    pressure: list[PressureProperties] | PressureProperties,
    rock_matrix: RockMatrixProperties,
) -> list[SaturatedRockProperties]:
    """
    Prepare inputs and parameters for running the Friable sandstone model

    Args:
        mineral: mineral properties containing k [Pa], mu [Pa] and rho [kg/m3]
        fluid: fluid properties containing k [Pa] and rho [kg/m3], can be several fluid
            properties in a list
        porosity: porosity fraction
        pressure: steps in effective pressure, unit Pa
        rock_matrix: parameters rock matrix

    Returns:
        saturated rock properties with vp [m/s], vs [m/s], density [kg/m^3], ai
        (vp * density), si (vs * density), vpvs (vp / vs)
    """
    # Mineral and porosity are assumed to be single objects, fluid and
    # effective_pressure can be lists
    fluid, pressure = _verify_inputs(fluid, pressure)

    # Depletion is calculated from the initial effective pressure
    initial_effective_pressure = pressure[0].effective_pressure
    # Container for saturated properties
    saturated_props = []

    # to please the IDE:
    k_dry = None
    mu = None
    k_init = None
    mu_init = None

    for time_step, (fl_prop, pres) in enumerate(zip(fluid, pressure)):
        (
            mask,
            tmp_min_k,
            tmp_min_mu,
            tmp_min_rho,
            tmp_fl_prop_k,
            tmp_fl_prop_rho,
            tmp_por,
            tmp_pres,
            init_press,
        ) = filter_and_one_dim(
            mineral.bulk_modulus,
            mineral.shear_modulus,
            mineral.density,
            fl_prop.bulk_modulus,
            fl_prop.density,
            porosity,
            pres.effective_pressure,
            initial_effective_pressure,
            return_numpy_array=True,
        )
        # At initial pressure, there is no need to estimate pressure effect on dry rock.
        # If there is no pressure sensitivity, we use the initial pressure for the dry
        # rock also after start of production, and the only differences will be due to
        # changes in fluid properties or saturation
        if time_step == 0:
            k_dry, mu = friable_model_dry(
                k_min=tmp_min_k,
                mu_min=tmp_min_mu,
                phi=tmp_por,
                p_eff=init_press,
                phi_c=rock_matrix.model.parameters.critical_porosity,
                coord_num_func=rock_matrix.model.parameters.coordination_number_function,
                n=rock_matrix.model.parameters.coord_num,
                shear_red=rock_matrix.model.parameters.shear_reduction,
            )
            # For use at depleted pressure
            k_init = k_dry
            mu_init = mu
        if time_step > 0 and rock_matrix.pressure_sensitivity:
            # estimate the properties for the initial pressure by friable model,
            # then apply correction for depletion

            # Prepare in situ properties
            in_situ_dict = {
                ParameterTypes.K.value: k_init,
                ParameterTypes.MU.value: mu_init,
                ParameterTypes.RHO.value: tmp_min_rho,
                ParameterTypes.POROSITY.value: tmp_por,
            }
            tmp_matrix = EffectiveMineralProperties(
                bulk_modulus=tmp_min_k,
                shear_modulus=tmp_min_mu,
                density=tmp_min_rho,
            )
            depl_props = apply_dry_rock_pressure_sensitivity_model(
                model=rock_matrix.pressure_sensitivity_model,
                initial_eff_pressure=init_press,
                depleted_eff_pressure=tmp_pres,
                in_situ_dict=in_situ_dict,
                mineral_properties=tmp_matrix,
                cement_properties=rock_matrix.minerals[rock_matrix.cement],
            )
            k_dry = depl_props[ParameterTypes.K.value]
            mu = depl_props[ParameterTypes.MU.value]

        # Saturate rock
        k_sat = gassmann(k_dry, tmp_por, tmp_fl_prop_k, tmp_min_k)
        rho_sat = (1.0 - tmp_por) * tmp_min_rho + tmp_por * tmp_fl_prop_rho
        vp, vs = velocity(k_sat, mu, rho_sat)[0:2]

        # Restore original size and shape
        vp, vs, rho_sat = reverse_filter_and_restore(mask, vp, vs, rho_sat)
        # Add results to list
        saturated_props.append(SaturatedRockProperties(vp=vp, vs=vs, density=rho_sat))

    return saturated_props


def _verify_inputs(fl_prop, pres_prop):
    # Ensure that properties of input objects are masked arrays
    def check_masked_arrays(inp_obj):
        for value in inp_obj.values():
            if not isinstance(value, np.ma.MaskedArray):
                raise ValueError("Expected all input object values to be masked arrays")

    if isinstance(fl_prop, list) and isinstance(pres_prop, list):
        if not len(fl_prop) == len(pres_prop):
            raise ValueError(
                f"{__file__}: unequal steps in fluid properties and pressure: "
                f"{len(fl_prop)} vs. {len(pres_prop)}"
            )
        for item in fl_prop + pres_prop:
            check_masked_arrays(asdict(item))
        return fl_prop, pres_prop
    if isinstance(fl_prop, EffectiveFluidProperties) and isinstance(
        pres_prop, PressureProperties
    ):
        check_masked_arrays(asdict(fl_prop))
        check_masked_arrays(asdict(pres_prop))
        return [
            fl_prop,
        ], [
            pres_prop,
        ]
    # else:
    raise ValueError(
        f"{__file__}: mismatch between fluid and pressure objects, both should "
        f"either be lists or class objects, are {type(fl_prop)} and "
        f"{type(pres_prop)}"
    )
