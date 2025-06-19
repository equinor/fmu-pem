from typing import List

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
    fluid_props: List[EffectiveFluidProperties],
    mineral_props: MatrixProperties,
) -> List:
    """
    Estimate the bulk density per restart date.

    Args:
        config: Parameter settings.
        init_prop: Constant properties, here using porosity.
        fluid_props: List of EffectiveFluidProperties objects representing the effective
            fluid properties per restart date.
        mineral_props: EffectiveMineralProperties object representing the effective
            properties.

    Returns:
        List of bulk densities per restart date.

    Raises:
        ValueError: If fluid_props is an empty list.
    """
    if config.rock_matrix.rpm == PatchyCementRPM:
        # Get cement mineral properties
        cement_mineral = config.rock_matrix.cement
        mineral = config.rock_matrix.minerals[cement_mineral]
        # Cement properties
        cement_properties = estimate_cement(
            mineral.bulk_modulus, mineral.shear_modulus, mineral.density, init_prop.poro
        )
        rel_frac_cem = (
            config.rock_matrix.rpm.parameters.cement_fraction / init_prop.poro
        )
        rho_m = (
            rel_frac_cem * cement_properties.dens
            + (1 - rel_frac_cem) * mineral_props.dens
        )
    else:
        rho_m = mineral_props.dens
    return [rho_b(init_prop.poro, fluid.dens, rho_m) for fluid in fluid_props]
