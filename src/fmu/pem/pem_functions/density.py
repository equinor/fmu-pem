from rock_physics_open.equinor_utilities.std_functions import rho_b

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    SimInitProperties,
    estimate_cement,
)
from fmu.pem.pem_utilities.rpm_models import PatchyCementRPM


def estimate_bulk_density(
    config: PemConfig,
    init_prop: SimInitProperties,
    fluid_props: list[EffectiveFluidProperties],
    mineral_props: MatrixProperties,
) -> list:
    """
    Estimate the bulk density per restart date.

    Args:
        config: Parameter settings.
        init_prop: Constant properties, here using porosity.
        fluid_props: list of EffectiveFluidProperties objects representing the effective
            fluid properties per restart date.
        mineral_props: EffectiveMineralProperties object representing the effective
            properties.

    Returns:
        list of bulk densities per restart date.

    Raises:
        ValueError: If fluid_props is an empty list.
    """
    if isinstance(config.rock_matrix.model, PatchyCementRPM):
        # Get cement mineral properties
        cement_mineral = config.rock_matrix.cement
        mineral = config.rock_matrix.minerals[cement_mineral]
        # Cement properties
        cement_properties = estimate_cement(
            mineral.bulk_modulus, mineral.shear_modulus, mineral.density, init_prop.poro
        )
        rel_cement_fraction = (
            config.rock_matrix.model.parameters.cement_fraction / init_prop.poro
        )
        rho_m = (
            rel_cement_fraction * cement_properties.density
            + (1 - rel_cement_fraction) * mineral_props.density
        )
    else:
        rho_m = mineral_props.density
    return [rho_b(init_prop.poro, fluid.density, rho_m) for fluid in fluid_props]
