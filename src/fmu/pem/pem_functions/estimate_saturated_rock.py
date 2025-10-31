from pathlib import Path

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PemConfig,
    PressureProperties,
    RockMatrixProperties,
    SaturatedRockProperties,
    SimInitProperties,
    estimate_cement,
)
from fmu.pem.pem_utilities.rpm_models import (
    FriableRPM,
    PatchyCementRPM,
    RegressionRPM,
    TMatrixRPM,
)

from .regression_models import run_regression_models
from .run_friable_model import run_friable
from .run_patchy_cement_model import run_patchy_cement
from .run_t_matrix_model import run_t_matrix_model


def estimate_saturated_rock(
    rock_matrix: RockMatrixProperties,
    sim_init: SimInitProperties,
    eff_pres: list[PressureProperties],
    matrix_props: EffectiveMineralProperties,
    fluid_props: list[EffectiveFluidProperties],
    model_directory: Path,
) -> list[SaturatedRockProperties]:
    """Wrapper to call rock physics model

    Args:
        rock_matrix: rock matrix properties
        sim_init: initial properties from simulation model
        eff_pres: restart properties from simulation model
        matrix_props: rock properties (mineral and fluids)
        fluid_props: effective fluid properties
        model_directory: directory for model files

    Returns:
        saturated rock properties per restart date
    """
    if isinstance(rock_matrix.model, PatchyCementRPM):
        # Patchy cement model
        cement = rock_matrix.minerals[rock_matrix.cement]
        cement_properties = estimate_cement(
            density=cement.density,
            bulk_modulus=cement.bulk_modulus,
            shear_modulus=cement.shear_modulus,
            grid=sim_init.poro,
        )
        sat_rock_props = run_patchy_cement(
            mineral=matrix_props,
            fluid=fluid_props,
            cement=cement_properties,
            porosity=sim_init.poro,
            pressure=eff_pres,
            rock_matrix_props=rock_matrix,
        )
    elif isinstance(rock_matrix.model, FriableRPM):
        # Friable sandstone model
        sat_rock_props = run_friable(
            mineral=matrix_props,
            fluid=fluid_props,
            porosity=sim_init.poro,
            pressure=eff_pres,
            rock_matrix=rock_matrix,
        )
    elif isinstance(rock_matrix.model, RegressionRPM):
        # Regression models for dry rock properties, saturation by Gassmann
        sat_rock_props = run_regression_models(
            matrix=matrix_props,
            fluid_properties=fluid_props,
            porosity=sim_init.poro,
            pressure=eff_pres,
            rock_matrix=rock_matrix,
            vsh=sim_init.vsh_pem,
        )
    elif isinstance(rock_matrix.model, TMatrixRPM):
        # Using default values for T-Matrix parameter file and vp and vs pressure
        # model files
        sat_rock_props = run_t_matrix_model(
            mineral_properties=matrix_props,
            fluid_properties=fluid_props,
            porosity=sim_init.poro,
            vsh=sim_init.vsh_pem,
            pressure=eff_pres,
            rock_matrix=rock_matrix,
            model_directory=model_directory,
        )
    else:
        raise ValueError(f"unknown rock model type: {rock_matrix.model}")
    return sat_rock_props
