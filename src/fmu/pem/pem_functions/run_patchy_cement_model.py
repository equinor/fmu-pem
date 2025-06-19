from typing import List, Union

import numpy as np
from rock_physics_open.sandstone_models import (
    patchy_cement_model_cem_frac as patchy_cement,
)

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    PressureProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)


def run_patchy_cement(
    mineral: MatrixProperties,
    fluid: Union[list[EffectiveFluidProperties], EffectiveFluidProperties],
    cement: MatrixProperties,
    porosity: np.ma.MaskedArray,
    pressure: Union[list[PressureProperties], PressureProperties],
    config: PemConfig,
) -> List[SaturatedRockProperties]:
    """Prepare inputs and parameters for running the Patchy Cement model

    Args:
        mineral: mineral properties containing k [Pa], mu [Pa] and rho [kg/m3]
        fluid: fluid properties containing k [Pa] and rho [kg/m3], can be several fluid
            properties in a list
        cement: cement properties containing k [Pa], mu [Pa] and rho [kg/m3]
        porosity: porosity fraction
        pressure: steps in effective pressure in [bar] due to Eclipse standard
        config: parameters for the PEM

    Returns:
        saturated rock properties with vp [m/s], vs [m/s], density [kg/m^3], ai
        (vp * density), si (vs * density), vpvs (vp / vs)
    """
    # Mineral and porosity are assumed to be single objects, fluid and
    # effective_pressure can be lists
    fluid, pressure = _verify_inputs(fluid, pressure)
    saturated_props = []
    pat_cem_params = config.rock_matrix.rpm.parameters
    for fl_prop, pres in zip(fluid, pressure):
        (
            mask,
            tmp_min_k,
            tmp_min_mu,
            tmp_min_rho,
            tmp_cem_k,
            tmp_cem_mu,
            tmp_cem_rho,
            tmp_fl_prop_k,
            tmp_fl_prop_rho,
            tmp_por,
            tmp_pres,
        ) = filter_and_one_dim(
            mineral.bulk_modulus,
            mineral.shear_modulus,
            mineral.dens,
            cement.bulk_modulus,
            cement.shear_modulus,
            cement.dens,
            fl_prop.bulk_modulus,
            fl_prop.dens,
            porosity,
            pres.effective_pressure * 1.0e5,
            return_numpy_array=True,
        )
        """Estimation of effective mineral properties must be able to handle cases where
         there is a more complex combination of minerals than the standard sand/shale
         case. For carbonates the input can be based on minerals (e.g. calcite,
         dolomite, quartz, smectite, ...) or PRTs (petrophysical rock types) that each
         have been assigned elastic properties to."""
        vp, vs, rho, _, _ = patchy_cement(
            tmp_min_k,
            tmp_min_mu,
            tmp_min_rho,
            tmp_cem_k,
            tmp_cem_mu,
            tmp_cem_rho,
            tmp_fl_prop_k,
            tmp_fl_prop_rho,
            tmp_por,
            tmp_pres,
            pat_cem_params.cement_fraction,
            pat_cem_params.critical_porosity,
            pat_cem_params.coord_num_function,
            pat_cem_params.coordination_number,
            pat_cem_params.shear_reduction,
        )
        vp, vs, rho = reverse_filter_and_restore(mask, vp, vs, rho)
        props = SaturatedRockProperties(vp=vp, vs=vs, dens=rho)
        saturated_props.append(props)
    return saturated_props


def _verify_inputs(fl_prop, pres_prop):
    if isinstance(fl_prop, list) and isinstance(pres_prop, list):
        if not len(fl_prop) == len(pres_prop):
            raise ValueError(
                f"{__file__}: unequal steps in fluid properties and pressure: "
                f"{len(fl_prop)} vs. {len(pres_prop)}"
            )
        return fl_prop, pres_prop
    if isinstance(fl_prop, EffectiveFluidProperties) and (
        isinstance(pres_prop, PressureProperties)
    ):
        return [
            fl_prop,
        ], [
            pres_prop,
        ]
    raise ValueError(
        f"{__file__}: mismatch between fluid and pressure objects, both should either "
        f"be lists or single objects, are {type(fl_prop)} and {type(pres_prop)}"
    )
