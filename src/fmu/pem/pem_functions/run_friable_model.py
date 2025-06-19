from dataclasses import asdict
from typing import List, Union

import numpy as np
from rock_physics_open.sandstone_models import friable_model

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    PressureProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)


def run_friable(
    mineral: MatrixProperties,
    fluid: Union[list[EffectiveFluidProperties], EffectiveFluidProperties],
    porosity: np.ma.MaskedArray,
    pressure: Union[list[PressureProperties], PressureProperties],
    config: PemConfig,
) -> List[SaturatedRockProperties]:
    """
    Prepare inputs and parameters for running the Friable sandstone model

    Args:
        mineral: mineral properties containing k [Pa], mu [Pa] and rho [kg/m3]
        fluid: fluid properties containing k [Pa] and rho [kg/m3], can be several fluid
            properties in a list
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
    friable_params = config.rock_matrix.rpm.parameters
    for fl_prop, pres in zip(fluid, pressure):
        (
            mask,
            tmp_min_k,
            tmp_min_mu,
            tmp_min_rho,
            tmp_fl_prop_k,
            tmp_fl_prop_rho,
            tmp_por,
            tmp_pres,
        ) = filter_and_one_dim(
            mineral.bulk_modulus,
            mineral.shear_modulus,
            mineral.dens,
            fl_prop.bulk_modulus,
            fl_prop.dens,
            porosity,
            pres.effective_pressure * 1.0e5,
        )
        """Estimation of effective mineral properties must be able to handle cases where
         there is a more complex combination of minerals than the standard sand/shale
         case. For carbonates the input can be based on minerals (e.g. calcite,
         dolomite, quartz, smectite, ...) or PRTs (petrophysical rock types) that each
         have been assigned elastic properties to."""
        vp, vs, rho, _, _ = friable_model(
            tmp_min_k,
            tmp_min_mu,
            tmp_min_rho,
            tmp_fl_prop_k,
            tmp_fl_prop_rho,
            tmp_por,
            tmp_pres,
            friable_params.critical_porosity,
            friable_params.coord_num_function,
            friable_params.coordination_number,
            friable_params.shear_reduction,
        )
        vp, vs, rho = reverse_filter_and_restore(mask, vp, vs, rho)
        props = SaturatedRockProperties(vp=vp, vs=vs, dens=rho)
        saturated_props.append(props)
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
