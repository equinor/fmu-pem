from pathlib import Path
from types import SimpleNamespace

import numpy as np

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    RockMatrixProperties,
    SaturatedRockProperties,
    SimInitProperties,
    estimate_cement,
    get_masked_array_mask,
    set_mask,
    to_masked_array,
)
from fmu.pem.pem_utilities.fipnum_pvtnum_utilities import (
    input_num_string_to_list,
    validate_zone_coverage,
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
    press_props: list[PressureProperties],
    matrix_props: EffectiveMineralProperties,
    fluid_props: list[EffectiveFluidProperties],
    model_directory: Path,
    fipnum_param: np.ma.MaskedArray,
) -> list[SaturatedRockProperties]:
    """Estimate saturated rock properties with zone-specific RPM selection.

    Each FIPNUM zone (string specification allowing lists/ranges/wildcards) can have
    its own rock physics model (Friable, Patchy Cement, Regression, T-Matrix). The
    workflow per zone is:
      1. Create zone-masked inputs (mask outside zone cells only for filtering).
      2. Call the appropriate RPM wrapper which internally flattens inputs using
         filter_and_one_dim, runs the physics, and restores to 3D using
         reverse_filter_and_restore.
      3. Copy computed data values back into the global 3D result grids for cells in
         this zone. The original simulation mask (inactive cells) is preserved; no
         per‑zone mask overwrites occur.

    Notes:
    - Intermediate zone masks are not propagated to final outputs; only the original
      reservoir inactive mask (fipnum_param.mask) remains.
    - NaN handling (invalid physics results) is deferred to later processing, not
      adjusted here.

    Args:
        rock_matrix: zone-aware rock matrix configuration
        sim_init: simulation model initial properties (contains porosity, vsh, etc.)
        eff_pres: effective / formation / overburden pressure objects per time step
        matrix_props: effective mineral properties (already estimated upstream)
        fluid_props: effective fluid properties per time step
        model_directory: directory for model-specific parameter files (T-Matrix)
        fipnum_param: FIPNUM grid partition descriptor

    Returns:
        List of SaturatedRockProperties (one per time step)

    Raises:
        ValueError: invalid zone coverage or unknown RPM type
    """
    # Validate zone coverage
    fipnum_strings: list[str] = [zone.fipnum for zone in rock_matrix.zone_regions]
    validate_zone_coverage(fipnum_strings, fipnum_param, zone_name="FIPNUM")

    # Get FIPNUM grid data and mask
    fipnum_data = fipnum_param.data
    fipnum_mask = get_masked_array_mask(fipnum_param)

    # Initialize result grids for each time step
    # We'll accumulate results per zone and merge them
    sat_rock_props_list: list[SaturatedRockProperties] = []

    # Initialize grids for each time step
    sat_rock_props_list = [
        SaturatedRockProperties(
            vp=to_masked_array(np.nan, fipnum_param),
            vs=to_masked_array(np.nan, fipnum_param),
            density=to_masked_array(np.nan, fipnum_param),
        )
        for _ in fluid_props
    ]

    # Process each zone with its specific rock physics model
    # Get actual FIPNUM values present in grid for use with input_num_string_to_list
    actual_fipnum_values = list(np.unique(fipnum_data[~fipnum_mask]).astype(int))

    # Process each unique zone (may contain multiple FIPNUMs)
    for zone_region in rock_matrix.zone_regions:
        # Get all FIPNUM values for this zone using input_num_string_to_list
        fipnum_values = input_num_string_to_list(
            zone_region.fipnum, actual_fipnum_values
        )

        # Build combined mask for all FIPNUMs in this zone using vectorized operation
        zone_mask = np.isin(fipnum_data, fipnum_values) & ~fipnum_mask

        # Create zone-specific masked arrays by masking cells OUTSIDE the zone
        # The RPM functions will call filter_and_one_dim internally to flatten arrays
        # and remove masked values before calling rock_physics_open library
        zone_porosity = np.ma.masked_where(~zone_mask, sim_init.poro)

        zone_matrix_props = matrix_props.masked_where(zone_mask)
        zone_fluid_props = [
            fluid_date.masked_where(zone_mask) for fluid_date in fluid_props
        ]
        zone_eff_pres = [pres_date.masked_where(zone_mask) for pres_date in press_props]

        # Call the appropriate rock physics model for this zone
        zone_sat_props = _call_zone_rpm_model(
            zone_region=zone_region,
            rock_matrix=rock_matrix,
            sim_init=sim_init,
            zone_porosity=zone_porosity,
            zone_matrix_props=zone_matrix_props,
            zone_fluid_props=zone_fluid_props,
            zone_eff_pres=zone_eff_pres,
            model_directory=model_directory,
        )

        # Merge zone results into the full grid for each time step (data only;
        # mask preserved)
        for time_idx, zone_props in enumerate(zone_sat_props):
            sat_rock_props_list[time_idx].vp.data[zone_mask] = zone_props.vp.data[
                zone_mask
            ]
            sat_rock_props_list[time_idx].vs.data[zone_mask] = zone_props.vs.data[
                zone_mask
            ]
            sat_rock_props_list[time_idx].density.data[zone_mask] = (
                zone_props.density.data[zone_mask]
            )

    # Recalculate derived properties (ai, si, vpvs) after all zones have been
    # merged
    for sat_props in sat_rock_props_list:
        sat_props.recalculate_derived()

    return sat_rock_props_list


def _call_zone_rpm_model(
    zone_region,
    rock_matrix: RockMatrixProperties,
    sim_init: SimInitProperties,
    zone_porosity: np.ma.MaskedArray,
    zone_matrix_props: EffectiveMineralProperties,
    zone_fluid_props: list[EffectiveFluidProperties],
    zone_eff_pres: list[PressureProperties],
    model_directory: Path,
) -> list[SaturatedRockProperties]:
    """Call the appropriate rock physics model for a specific zone.

    This helper function dispatches to the correct RPM model (Patchy Cement, Friable,
    Regression, or T-Matrix) based on the zone's configuration. It creates a temporary
    RockMatrixProperties object with zone-specific model parameters.

    Args:
        zone_region: zone-specific rock matrix parameters
        rock_matrix: full rock matrix properties (for minerals and other shared config)
        sim_init: initial simulation properties
        zone_porosity: porosity for this zone only
        zone_matrix_props: effective mineral properties for this zone
        zone_fluid_props: effective fluid properties for this zone (per time step)
        zone_eff_pres: effective pressure properties for this zone (per time step)
        model_directory: directory for model files

    Returns:
        List of SaturatedRockProperties for each time step for this zone

    Raises:
        ValueError: If unknown rock physics model type is encountered
    """
    # Create a simple object with zone-specific model attributes
    # We can't instantiate RockMatrixProperties with already-instantiated zone_region
    # because Pydantic validators expect dict input. Instead, create a namespace object
    # with the attributes that RPM functions need.

    zone_rock_matrix = SimpleNamespace(
        model=zone_region.model,
        pressure_sensitivity=zone_region.pressure_sensitivity,
        pressure_sensitivity_model=zone_region.pressure_sensitivity_model,
        minerals=rock_matrix.minerals,
        cement=rock_matrix.cement,
        volume_fractions=rock_matrix.volume_fractions,
        fraction_names=rock_matrix.fraction_names,
        fraction_minerals=rock_matrix.fraction_minerals,
        shale_fractions=rock_matrix.shale_fractions,
        complement=rock_matrix.complement,
        mineral_mix_model=rock_matrix.mineral_mix_model,
    )

    if isinstance(zone_region.model, PatchyCementRPM):
        # Patchy cement model
        cement = rock_matrix.minerals[rock_matrix.cement]
        cement_properties = estimate_cement(
            density=cement.density,
            bulk_modulus=cement.bulk_modulus,
            shear_modulus=cement.shear_modulus,
            grid=zone_porosity,
        )
        zone_sat_props = run_patchy_cement(
            mineral=zone_matrix_props,
            fluid=zone_fluid_props,
            cement=cement_properties,
            porosity=zone_porosity,
            pressure=zone_eff_pres,
            rock_matrix_props=zone_rock_matrix,
        )
    elif isinstance(zone_region.model, FriableRPM):
        # Friable sandstone model
        zone_sat_props = run_friable(
            mineral=zone_matrix_props,
            fluid=zone_fluid_props,
            porosity=zone_porosity,
            pressure=zone_eff_pres,
            rock_matrix=zone_rock_matrix,
        )
    elif isinstance(zone_region.model, RegressionRPM):
        # Regression models for dry rock properties, saturation by Gassmann
        zone_vsh = set_mask(
            masked_template=zone_porosity,
            prop_array=sim_init.vsh_pem,
        )
        zone_sat_props = run_regression_models(
            matrix=zone_matrix_props,
            fluid_properties=zone_fluid_props,
            porosity=zone_porosity,
            pressure=zone_eff_pres,
            rock_matrix=zone_rock_matrix,
            vsh=zone_vsh,
        )
    elif isinstance(zone_region.model, TMatrixRPM):
        # T-Matrix model - estimates dry rock and saturated rock in one integrated model
        zone_vsh = set_mask(
            masked_template=zone_porosity,
            prop_array=sim_init.vsh_pem,
        )
        zone_sat_props = run_t_matrix_model(
            mineral_properties=zone_matrix_props,
            fluid_properties=zone_fluid_props,
            porosity=zone_porosity,
            vsh=zone_vsh,
            pressure=zone_eff_pres,
            rock_matrix=zone_rock_matrix,
            model_directory=model_directory,
        )
    else:
        raise ValueError(f"Unknown rock model type: {zone_region.model}")

    return zone_sat_props
