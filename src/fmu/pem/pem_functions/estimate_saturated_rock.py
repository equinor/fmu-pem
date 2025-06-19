from typing import List

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    PressureProperties,
    SaturatedRockProperties,
    SimInitProperties,
    estimate_cement,
)
from fmu.pem.pem_utilities.rpm_models import (
    FriableRPM,
    PatchyCementRPM,
    RegressionModels,
)

from .regression_models import run_regression_models
from .run_friable_model import run_friable
from .run_patchy_cement_model import run_patchy_cement
from .run_t_matrix_and_pressure import run_t_matrix_and_pressure_models


def estimate_saturated_rock(
    config: PemConfig,
    sim_init: SimInitProperties,
    eff_pres: list[PressureProperties],
    matrix_props: MatrixProperties,
    fluid_props: list[EffectiveFluidProperties],
) -> List[SaturatedRockProperties]:
    """Wrapper to call rock physics model

    Args:
        config: PEM configuration parameters
        sim_init: initial properties from simulation model
        eff_pres: restart properties from simulation model
        matrix_props: rock properties (mineral and fluids)
        fluid_props: effective fluid properties

    Returns:
        saturated rock properties per restart date
    """
    if isinstance(config.rock_matrix.rpm, PatchyCementRPM):
        # Patchy cement model
        cement = config.rock_matrix.minerals[config.rock_matrix.cement]
        cement_properties = estimate_cement(
            density=cement.density,
            bulk_modulus=cement.bulk_modulus,
            shear_modulus=cement.shear_modulus,
            grid=sim_init.poro,
        )
        sat_rock_props = run_patchy_cement(
            matrix_props,
            fluid_props,
            cement_properties,
            sim_init.poro,
            eff_pres,
            config,
        )
    elif isinstance(config.rock_matrix.rpm, FriableRPM):
        # Friable sandstone model
        sat_rock_props = run_friable(
            matrix_props,
            fluid_props,
            sim_init.poro,
            eff_pres,
            config,
        )
    elif isinstance(config.rock_matrix.rpm, RegressionModels):
        # Regression models for dry rock properties, saturation by Gassmann
        sat_rock_props = run_regression_models(
            matrix_props,
            fluid_props,
            sim_init.poro,
            eff_pres,
            config,
            vsh=sim_init.ntg_pem,
        )
    else:
        # Using default values for T-Matrix parameter file and vp and vs pressure
        # model files
        sat_rock_props = run_t_matrix_and_pressure_models(
            matrix_props,
            fluid_props,
            sim_init.poro,
            sim_init.ntg_pem,
            eff_pres,
            config,
        )
    return sat_rock_props
