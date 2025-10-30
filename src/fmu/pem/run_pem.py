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
        yaml_file=start_dir.joinpath(rel_path_pem, pem_config_file_name)
    )

    # Read necessary part of global configurations and parameters
    config.update_with_global(
        pem_utils.get_global_params_and_dates(
            root_dir=start_dir, conf_path=config.paths.rel_path_fmu_config
        )
    )

    # Import Eclipse simulation grid - INIT and RESTART
    sim_grid, constant_props, time_step_props = pem_utils.read_sim_grid_props(
        rel_dir_sim_files=config.eclipse_files.rel_path_simgrid,
        egrid_file=config.eclipse_files.egrid_file,
        init_property_file=config.eclipse_files.init_property_file,
        restart_property_file=config.eclipse_files.restart_property_file,
        seis_dates=config.global_params.seis_dates,
        fipnum_name=config.alternative_fipnum_name,
    )

    # Calculate rock properties - fluids and minerals
    # Effective mineral (matrix) properties - one set valid for all time-steps
    vsh, matrix_properties = pem_fcns.effective_mineral_properties(
        root_dir=start_dir,
        matrix=config.rock_matrix,
        sim_init=constant_props,
        sim_grid=sim_grid,
    )
    # VSH is exported with other constant results, add it to the constant properties
    constant_props.vsh_pem = vsh

    # Fluid properties calculated for all time-steps
    fluid_properties = pem_fcns.effective_fluid_properties_zoned(
        restart_props=time_step_props,
        fluids=config.fluids,
        pvtnum=constant_props.pvtnum,
    )

    # Estimate effective pressure
    eff_pres = pem_fcns.estimate_pressure(
        rock_matrix=config.rock_matrix,
        overburden_pressure=config.pressure,
        sim_init=constant_props,
        sim_rst=time_step_props,
        matrix_props=matrix_properties,
        fluid_props=fluid_properties,
        sim_dates=config.global_params.seis_dates,
        fipnum=constant_props.fipnum,
    )

    # Estimate saturated rock properties
    sat_rock_props = pem_fcns.estimate_saturated_rock(
        rock_matrix=config.rock_matrix,
        sim_init=constant_props,
        press_props=eff_pres,
        matrix_props=matrix_properties,
        fluid_props=fluid_properties,
        model_directory=config.paths.rel_path_pem,
        fipnum_param=constant_props.fipnum,
    )

    # Delta and cumulative time estimates (only TWT properties are kept)
    sum_delta_time = pem_utils.delta_cumsum_time.estimate_sum_delta_time(
        constant_props=constant_props,
        sat_rock_props=sat_rock_props,
    )

    # Calculate difference properties. Possible properties are all that vary with time
    diff_props, diff_date_strs = pem_utils.calculate_diff_properties(
        props=[time_step_props, eff_pres, sat_rock_props, sum_delta_time],
        diff_dates=config.global_params.diff_dates,
        seis_dates=config.global_params.seis_dates,
        diff_calculation=config.diff_calculation,
    )

    # As a precaution, update the grid mask for inactive cells, based on the saturated
    # rock properties
    sim_grid = pem_utils.update_inactive_grid_cells(
        grid=sim_grid,
        props=sat_rock_props,
    )

    # Save results to disk or RMS project according to settings in the PEM config
    pem_utils.save_results(
        start_dir=start_dir,
        run_from_rms_flag=run_from_rms,
        rms_project=proj,
        sim_grid=sim_grid,
        grid_name=config.global_params.grid_model,
        seis_dates=config.global_params.seis_dates,
        save_to_rms=config.results.save_results_to_rms,
        save_to_disk=config.results.save_results_to_disk,
        save_intermediate=config.results.save_intermediate_results,
        mandatory_path=config.paths.rel_path_mandatory_output,
        pem_output_path=config.paths.rel_path_output,
        eff_pres_props=eff_pres,
        sat_rock_props=sat_rock_props,
        difference_props=diff_props,
        difference_date_strs=diff_date_strs,
        matrix_props=matrix_properties,
        fluid_props=fluid_properties,
    )

    # Restore original path
    os.chdir(start_dir)
    return
