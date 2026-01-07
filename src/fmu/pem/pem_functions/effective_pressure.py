from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SimInitProperties,
    SimRstProperties,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import (
    OverburdenPressureTypes,
    RPMType,
)
from fmu.pem.pem_utilities.fipnum_pvtnum_utilities import (
    input_num_string_to_list,
    validate_zone_coverage,
)
from fmu.pem.pem_utilities.pem_config_validation import (
    OverburdenPressureConstant,
    OverburdenPressureTrend,
)

from .density import estimate_bulk_density

if TYPE_CHECKING:
    from fmu.pem.pem_utilities import RockMatrixProperties


def estimate_pressure(
    rock_matrix: "RockMatrixProperties",
    overburden_pressure: list[OverburdenPressureTrend | OverburdenPressureConstant],
    sim_init: SimInitProperties,
    sim_rst: list[SimRstProperties],
    matrix_props: EffectiveMineralProperties,
    fluid_props: list[EffectiveFluidProperties],
    sim_dates: list[str],
    fipnum: np.ma.MaskedArray,
) -> list[PressureProperties]:
    """Estimate effective and overburden pressure with per-zone overburden pressure
    definitions.

    Effective pressure is defined as overburden pressure minus formation (or pore)
    pressure multiplied with the Biot factor. Overburden pressure is zone-aware
    (defined per FIPNUM group) but constant in time, while effective pressure
    varies with time as formation pressure changes.

    This function now supports zone-based rock physics models. Each zone can have
    its own model type (e.g., Patchy Cement, Friable), which affects bulk density
    calculation for overburden pressure estimation.

    Args:
        rock_matrix: rock matrix properties with zone-specific model definitions
        overburden_pressure: list of trend or constant value for overburden pressure
            per FIPNUM zone group
        sim_init: initial properties from simulation model
        sim_rst: restart properties from the simulation model (time-dependent)
        matrix_props: effective mineral properties
        fluid_props: effective fluid properties (time-dependent)
        sim_dates: list of dates for simulation
        fipnum: grid parameter with zone/region information

    Returns:
        List of PressureProperties for each time step containing effective pressure
        [bar], formation pressure [bar], and overburden_pressure [bar]

    Raises:
        ValueError: If FIPNUM zone definitions are invalid or if effective pressure
            is negative for any cells.
    """
    # Validate zone coverage
    fipnum_strings: list[str] = [str(zone.fipnum) for zone in overburden_pressure]
    validate_zone_coverage(fipnum_strings, fipnum, zone_name="FIPNUM")

    # Get FIPNUM grid data and mask
    fipnum_data = fipnum.data
    fipnum_mask = (
        fipnum.mask
        if hasattr(fipnum, "mask")
        else np.zeros_like(fipnum_data, dtype=bool)
    )

    # Get actual FIPNUM values present in grid for use with input_num_string_to_list
    actual_fipnum_values = list(np.unique(fipnum_data[~fipnum_mask]).astype(int))

    # Calculate bulk density for all time steps (needed for overburden pressure
    # calculation)
    # Bulk density calculation needs to be zone-aware for patchy cement models
    fl_density = [fluid.density for fluid in fluid_props]

    # Check if any zone uses patchy cement model and needs special handling
    bulk_density = []
    for fl_dens in fl_density:
        bulk_dens_grid = np.ma.masked_array(
            np.zeros(sim_init.poro.shape, dtype=float), mask=fipnum_mask
        )

        # Calculate bulk density per zone based on zone-specific model
        for zone_region in rock_matrix.zone_regions:
            # Get all FIPNUM values for this zone using input_num_string_to_list
            fipnum_values = input_num_string_to_list(
                zone_region.fipnum, actual_fipnum_values
            )

            # Build combined mask for all FIPNUMs in this zone using vectorized
            # operation
            zone_mask = np.isin(fipnum_data, fipnum_values) & ~fipnum_mask

            # Check if this zone uses patchy cement model
            is_patchy_cement = zone_region.model.model_name == RPMType.PATCHY_CEMENT

            if is_patchy_cement:
                # Get cement fraction and density for patchy cement model
                cement_fraction = zone_region.model.parameters.cement_fraction
                cement_density = rock_matrix.minerals[rock_matrix.cement].density
            else:
                cement_fraction = None
                cement_density = None

            # Calculate bulk density for this zone
            zone_bulk_density = estimate_bulk_density(
                porosity=np.ma.masked_where(~zone_mask, sim_init.poro),
                fluid_density=[np.ma.masked_where(~zone_mask, fl_dens)],
                mineral_density=np.ma.masked_where(~zone_mask, matrix_props.density),
                patchy_cement=is_patchy_cement,
                cement_fraction=cement_fraction,
                cement_density=cement_density,
            )

            # Merge zone bulk density into full grid
            bulk_dens_grid[zone_mask] = zone_bulk_density[0][zone_mask]

            bulk_density.append(bulk_dens_grid)

    # Calculate overburden pressure per zone (time-independent)
    # Initialize overburden pressure grid
    overburden_pressure_grid = np.ma.masked_array(
        np.full(sim_init.depth.shape, np.nan, dtype=float), mask=fipnum_mask
    )

    for zone in overburden_pressure:
        # Get all FIPNUM values for this zone using input_num_string_to_list
        fipnum_values = input_num_string_to_list(zone.fipnum, actual_fipnum_values)

        # Build combined mask for all FIPNUMs in this zone using vectorized operation
        mask_cells = np.isin(fipnum_data, fipnum_values) & ~fipnum_mask

        if zone.type == OverburdenPressureTypes.CONSTANT:
            # Constant overburden pressure for this zone
            overburden_pressure_grid[mask_cells] = zone.value
        else:  # zone.type == OverburdenPressureTypes.TREND
            # Calculate overburden pressure from trend for this zone (already in Pa)
            zone_ovb_pres = overburden_pressure_from_trend(
                inter=zone.intercept,
                grad=zone.gradient,
                depth=sim_init.depth,
            )
            overburden_pressure_grid[mask_cells] = zone_ovb_pres[mask_cells]

    # Calculate effective pressure for each time step
    # Formation pressure changes with time, but overburden pressure is constant
    eff_pres = [
        estimate_effective_pressure(
            formation_pressure=sim_date.pressure,
            bulk_density=dens,
            reference_overburden_pressure=overburden_pressure_grid,
        )
        for (sim_date, dens) in zip(sim_rst, bulk_density)
    ]

    # Sanity check on results - effective pressure should not be negative
    for i, pres in enumerate(eff_pres):
        if np.any(pres.effective_pressure < 0.0):
            raise ValueError(
                f"effective pressure calculation: formation pressure exceeds "
                f"overburden pressure for date {sim_dates[i]}, \n"
                f"minimum effective pressure is {np.min(pres.effective_pressure):.2f} "
                f"bar, the number of cells with negative effective pressure is "
                f"{np.sum(pres.effective_pressure < 0.0)}"
            )

    return eff_pres


def estimate_effective_pressure(
    formation_pressure: np.ma.MaskedArray,
    bulk_density: np.ma.MaskedArray,
    reference_overburden_pressure: np.ma.MaskedArray | float,
    biot_coeff: float = 1.0,
) -> PressureProperties:
    """Estimate effective pressure from reference overburden pressure, formation
        pressure, depth and bulk density

        Args:
            formation_pressure: formation pressure [Pa]
            bulk_density: bulk density [kg/m3]
            reference_overburden_pressure: constant or one-layer array with reference
            biot_coeff: Biot coefficient, in the range [0.0, 1.0] [unitless]
    .mineral
        Returns:
            PressureProperties object with formation pressure [bar], effective pressure
            [bar], overburden_pressure [bar]

        Raises:
            ValueError: If reference overburden pressure is not of type float or numpy
            masked array, or if reference overburden pressure is not of the same
            dimension as comparable grids, or if reference overburden pressure does
            not have the same shape as comparable grids.
    """
    reference_overburden_pressure = _verify_ovb_press(
        reference_overburden_pressure, bulk_density
    )
    effective_pressure = reference_overburden_pressure - biot_coeff * formation_pressure
    return PressureProperties(
        formation_pressure=formation_pressure,
        effective_pressure=effective_pressure,
        overburden_pressure=reference_overburden_pressure,
    )


def _verify_ovb_press(
    ref_pres: float | np.ma.MaskedArray, reference_cube: np.ma.MaskedArray
) -> np.ma.MaskedArray:
    if isinstance(ref_pres, float):
        return to_masked_array(ref_pres, reference_cube)
    if not isinstance(ref_pres, np.ma.MaskedArray):
        raise ValueError(
            f"{__file__}: Reference overburden pressure is not of type float or numpy "
            "masked array"
        )
    if not ref_pres.ndim == reference_cube.ndim:
        raise ValueError(
            f"{__file__}: Reference overburden pressure is not of the same dimension "
            "as comparable grids"
        )
    if not np.all(ref_pres.shape[0:-1] == reference_cube.shape[0:-1]):
        raise ValueError(
            f"{__file__}: Reference overburden pressure does not have the same shape "
            "as comparable grids"
        )
    return ref_pres


def overburden_pressure_from_trend(
    inter: float, grad: float, depth: np.ma.MaskedArray
) -> np.ma.MaskedArray:
    """Calculate overburden pressure from depth trend for top of depth grid

    Args:
        inter: intercept in trend
        grad: gradient in trend
        depth: depth cube [m]

    Returns:
        overburden pressure [Pa]

    Raises:
        ValueError: If unable to calculate overburden pressure due to non-numeric
        intercept or gradient.
    """
    try:
        a = float(inter)
        b = float(grad)
        ovb_pres = a + b * depth
    except ValueError as err:
        raise ValueError(
            f"{__file__}: unable to calculate overburden pressure:"
        ) from err
    return ovb_pres
