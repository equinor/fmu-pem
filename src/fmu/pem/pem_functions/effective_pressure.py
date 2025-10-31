import numpy as np

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PemConfig,
    PressureProperties,
    SimInitProperties,
    SimRstProperties,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import (
    OverburdenPressureTypes,
    RPMType,
)
from fmu.pem.pem_utilities.pem_config_validation import (
    OverburdenPressureConstant,
    OverburdenPressureTrend,
)

from .density import estimate_bulk_density


def estimate_pressure(
    rpm_model: RPMType,
    cement_fraction: float | None,
    cement_density: float | None,
    overburden_pressure: OverburdenPressureTrend | OverburdenPressureConstant,
    sim_init: SimInitProperties,
    sim_rst: list[SimRstProperties],
    matrix_props: EffectiveMineralProperties,
    fluid_props: list[EffectiveFluidProperties],
    sim_dates: list[str],
) -> list[PressureProperties]:
    """Estimate effective and overburden pressure.
    Effective pressure is defined as overburden pressure minus formation (or pore)
    pressure multiplied with the Biot factor

    Args:
        rpm_model: model for saturated rock properties
        cement_fraction: volume fraction of cement, if patchy cement model is set
        cement_density: cement mineral density, if patchy cement model is set
        overburden_pressure: trend or constant value for overburden pressure
        sim_init: initial properties from simulation model
        sim_rst: restart properties from the simulation model
        matrix_props: rock properties
        fluid_props: effective fluid properties
        sim_dates: list of dates for simulation

    Returns:
        effective pressure [bar], overburden_pressure [bar]

    Raises:
        ValueError: If sim_rst is an empty list.
    """
    # Effective pressure, get formation pressures and convert to Pa from bar
    # Saturated rock bulk density bulk
    fl_density = [fluid.density for fluid in fluid_props]
    b_patchy_cement = rpm_model == RPMType.PATCHY_CEMENT
    bulk_density = estimate_bulk_density(
        porosity=sim_init.poro,
        fluid_density=fl_density,
        mineral_density=matrix_props.density,
        patchy_cement=b_patchy_cement,
        cement_fraction=cement_fraction,
        cement_density=cement_density,
    )

    if overburden_pressure.type == OverburdenPressureTypes.CONSTANT:
        eff_pres = [
            estimate_effective_pressure(
                formation_pressure=sim_date.pressure * 1.0e5,
                bulk_density=dens,  # type: ignore
                reference_overburden_pressure=overburden_pressure.value,
            )
            for (sim_date, dens) in zip(sim_rst, bulk_density)
        ]
    else:  # overburden_pressure.type == 'trend':
        eff_pres = [
            estimate_effective_pressure(
                formation_pressure=sim_date.pressure * 1.0e5,
                bulk_density=dens,  # type: ignore
                reference_overburden_pressure=overburden_pressure_from_trend(
                    inter=overburden_pressure.intercept,
                    grad=overburden_pressure.gradient,
                    depth=sim_init.depth,
                ),
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
    # Add effective pressure to RST properties
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
        formation_pressure=formation_pressure * 1.0e-5,
        effective_pressure=effective_pressure * 1.0e-5,
        overburden_pressure=reference_overburden_pressure * 1.0e-5,
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
