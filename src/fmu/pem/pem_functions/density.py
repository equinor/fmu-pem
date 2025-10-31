from numpy.ma import MaskedArray
from rock_physics_open.equinor_utilities.std_functions import rho_b


def estimate_bulk_density(
    porosity: MaskedArray,
    fluid_density: list[MaskedArray],
    mineral_density: MaskedArray,
    *,
    patchy_cement: bool = False,
    cement_fraction: float | None = None,
    cement_density: float | None = None,
) -> list[MaskedArray]:
    r"""
    Estimate the bulk density per restart date.

    Args:
        porosity: Initial simulation  porosity.
        fluid_density: Effective fluid density per date.
        mineral_density: Effective mineral (matrix) density.
        patchy_cement: Enable patchy_cement mixing.
        cement_fraction: Cement volume fraction within pore space.
        cement_density: Cement density.

    Returns:
        list of bulk densities per restart date.

    Raises:
        ValueError: If fluid_props is an empty list.
    """
    if not fluid_density:
        raise ValueError("Fluid properties cannot be an empty list.")

    if patchy_cement:
        if any(v is None for v in (cement_fraction, cement_density)):
            raise ValueError(
                "cement_fraction and cement_props must be provided when "
                "patchy_cement is True."
            )
        # Cement properties
        rel_cement_fraction = cement_fraction / porosity
        rho_m = (
            rel_cement_fraction * cement_density
            + (1 - rel_cement_fraction) * mineral_density
        )
    else:
        rho_m = mineral_density

    return [rho_b(porosity, rho_fl, rho_m) for rho_fl in fluid_density]  # type: ignore
