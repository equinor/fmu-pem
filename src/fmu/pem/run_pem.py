import os
from pathlib import Path

from fmu.pem import pem_functions as pem_fcns
from fmu.pem import pem_utilities as pem_utils


def pem_fcn(
    start_dir: Path,
    rel_path_pem: Path,
    pem_config_file_name: Path,
    run_from_rms=False,
    proj=None,
) -> None:
    """
    Run script for extended petro elastic module within sim2seis. Parameters in
    yaml-file control the selections made in the PEM.

    """
    # Read and validate all PEM parameters
    config = pem_utils.read_pem_config(
        start_dir.joinpath(rel_path_pem, pem_config_file_name)
    )

    # Read necessary part of global configurations and parameters
    config.update_with_global(
        pem_utils.get_global_params_and_dates(
            start_dir, config.paths.rel_path_fmu_config
        )
    )

    # Import Eclipse simulation grid - INIT and RESTART
    egrid_file = start_dir / config.paths.rel_path_simgrid / "ECLIPSE.EGRID"
    init_property_file = start_dir / config.paths.rel_path_simgrid / "ECLIPSE.INIT"
    restart_property_file = start_dir / config.paths.rel_path_simgrid / "ECLIPSE.UNRST"

    sim_grid, constant_props, time_step_props = pem_utils.read_sim_grid_props(
        egrid_file,
        init_property_file,
        restart_property_file,
        config.global_params.seis_dates,
    )

    # Calculate rock properties - fluids and minerals
    # Fluid properties calculated for all time-steps
    fluid_properties = pem_fcns.effective_fluid_properties(
        time_step_props, config.fluids
    )

    # Effective mineral (matrix) properties - one set valid for all time-steps
    vsh, matrix_properties = pem_fcns.effective_mineral_properties(
        start_dir, config, constant_props, sim_grid
    )
    # VSH is exported with other constant results, add it to the constant properties
    constant_props.ntg_pem = vsh

    # Estimate effective pressure
    eff_pres = pem_fcns.estimate_pressure(
        config, constant_props, time_step_props, matrix_properties, fluid_properties
    )

    # Estimate saturated rock properties
    sat_rock_props = pem_fcns.estimate_saturated_rock(
        config, constant_props, eff_pres, matrix_properties, fluid_properties
    )

    # Delta and cumulative time estimates (only TWT properties are kept)
    sum_delta_time = pem_utils.delta_cumsum_time.estimate_sum_delta_time(
        constant_props, sat_rock_props, config
    )

    # Calculate difference properties. Possible properties are all that vary with time
    diff_props, diff_date_strs = pem_utils.calculate_diff_properties(
        [time_step_props, eff_pres, sat_rock_props, sum_delta_time], config
    )

    # As a precaution, update the grid mask for inactive cells, based on the saturated
    # rock properties
    sim_grid = pem_utils.update_inactive_grid_cells(sim_grid, sat_rock_props)

    # Save results to disk or RMS project according to settings in the PEM config
    pem_utils.save_results(
        start_dir,
        run_from_rms,
        config,
        proj,
        sim_grid,
        eff_pres,
        sat_rock_props,
        diff_props,
        diff_date_strs,
        matrix_properties,
        fluid_properties,
    )

    # Restore original path
    os.chdir(start_dir)
    return
