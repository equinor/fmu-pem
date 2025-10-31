import warnings
from dataclasses import asdict
from pathlib import Path

import xtgeo

from .enum_defs import Sim2SeisRequiredParams
from .pem_class_definitions import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SaturatedRockProperties,
)
from .utils import _verify_export_inputs, restore_dir


def save_results(
    start_dir: Path,
    run_from_rms_flag: bool,
    rms_project: object,
    sim_grid: xtgeo.grid3d.Grid,
    grid_name: str,
    seis_dates: list[str],
    save_to_rms: bool,
    save_to_disk: bool,
    save_intermediate: bool,
    mandatory_path: Path,
    pem_output_path: Path,
    eff_pres_props: list[PressureProperties],
    sat_rock_props: list[SaturatedRockProperties],
    difference_props: list[dict],
    difference_date_strs: list[str],
    matrix_props: EffectiveMineralProperties,
    fluid_props: list[EffectiveFluidProperties],
) -> None:
    """Saves all intermediate and final results according to the settings in the PEM
    and global config files

    Args:
        start_dir: initial directory setting
        run_from_rms_flag: call to PEM from RMS
        rms_project: RMS project
        sim_grid: grid definition
        grid_name: stem of output grid name
        seis_dates: list of dates for simulation runs
        save_to_rms: save results to RMS project
        save_to_disk: save non-mandatory results to disk
        save_intermediate: save intermediate calculations to disk
        mandatory_path: path for mandatory output
        pem_output_path: path for non-mandatory PEM output
        eff_pres_props: effective, overburden and formation pressure per time step
        sat_rock_props: elastic properties of saturated rock
        difference_props: differences in elastic properties between selected restart
            dates
        difference_date_strs: dates for difference calculation
        matrix_props: intermediate results - mineral properties
        fluid_props: intermediate results - fluid properties per time step

    Returns:
        None, warning or KeyError
    """
    # Saving results:

    # 1. Mandatory part: Save Vp, Vs, Density to disk for seismic forward modelling.
    full_mandatory_path = start_dir / mandatory_path
    full_output_path = start_dir / pem_output_path
    output_set = [
        {
            k: v
            for (k, v) in asdict(sat_prop).items()  # type: ignore
            if k in list(Sim2SeisRequiredParams)
        }
        for sat_prop in sat_rock_props
    ]
    export_results_disk(
        output_set,
        sim_grid,
        grid_name,
        full_mandatory_path,
        time_steps=seis_dates,
        export_format="grdecl",
    )

    # 2. Save results to rms and/or disk according to config file

    # create list of dict from list of pressure and saturated rock objects
    eff_pres_dict_list = [asdict(obj) for obj in eff_pres_props]  # type: ignore  # NB: this is a pycharm bug to be removed
    sat_prop_dict_list = [asdict(obj) for obj in sat_rock_props]  # type: ignore

    try:
        if save_to_rms and run_from_rms_flag:
            # Time dependent absolute properties
            for props in [eff_pres_dict_list, sat_prop_dict_list]:
                prop_dict = list(props)
                export_results_roxar(
                    rms_project,
                    prop_dict,
                    sim_grid,
                    grid_name,
                    time_steps=seis_dates,
                )
            # Difference properties
            export_results_roxar(
                rms_project,
                difference_props,
                sim_grid,
                grid_name,
                time_steps=difference_date_strs,
            )
    except KeyError:  # warn user that results are not saved
        warnings.warn(
            f"{__file__}: no parameter for saving results to rms is found in the "
            f"config file"
        )
    try:
        if save_to_disk:
            for props in [eff_pres_dict_list, sat_prop_dict_list]:
                prop_dict = list(props)
                export_results_disk(
                    prop_dict,
                    sim_grid,
                    sim_grid.name,
                    full_output_path,
                    time_steps=seis_dates,
                )
            export_results_disk(
                difference_props,
                sim_grid,
                grid_name,
                full_output_path,
                time_steps=difference_date_strs,
            )
    except KeyError:  # warn user that results are not saved
        warnings.warn(
            f"{__file__}: no parameter for saving results to disk is found in the "
            f"config file"
        )

    # 3. Save intermediate results only if specified in the config file
    try:
        if save_intermediate:
            export_results_disk(
                [asdict(fl_props) for fl_props in fluid_props],  # type: ignore
                sim_grid,
                grid_name,
                full_output_path,
                time_steps=seis_dates,
                name_suffix="_FLUID",
            )
            export_results_disk(
                asdict(matrix_props),  # type: ignore
                sim_grid,
                grid_name,
                full_output_path,
                name_suffix="_MINERAL",
            )
    except KeyError:
        # just skip silently if save_intermediate_results is not present in the
        # pem_config
        pass
    return


def export_results_roxar(
    prj: object,
    result_props: list[dict] | dict,
    grid: xtgeo.grid3d.Grid,
    rms_grid_name: str,
    time_steps: list[str] | None = None,
    name_suffix: str = "",
    force_write_grid: bool = False,
) -> None:
    """Export results directly to RMS. Properties to be exported can be with time-steps
        or single

    Args:
        prj: rms project
        result_props: properties, list of or single dict, with numpy masked array
            values
        grid: 3D grid definition
        rms_grid_name: name of grid within rms project
        time_steps: list of simulation model dates, None if properties is not linked to
            a simulation model date
        name_suffix: extra suffix for variable names
        force_write_grid: lag to overwrite grid model in RMS

    Returns:
        None
    """
    result_props, time_steps = _verify_export_inputs(result_props, grid, time_steps)
    if force_write_grid:
        grid.to_roxar(prj, rms_grid_name)  # type: ignore
    else:
        _verify_gridmodel(prj, rms_grid_name, grid)
    for props, step in zip(result_props, time_steps):  # type: ignore
        if step != "":
            step = "_" + step
        for key, value in props.items():
            grid_property_name = key.upper() + name_suffix + step
            grid_prop = xtgeo.grid3d.GridProperty(
                grid, values=value, name=grid_property_name, date=step
            )
            grid_prop.to_roxar(prj, rms_grid_name, grid_property_name)  # type: ignore
    return


def _verify_gridmodel(prj: object, rms_grid_model_name: str, grid: xtgeo.grid3d.Grid):
    if hasattr(prj, "grid_models"):
        for model in prj.grid_models:
            if model.name == rms_grid_model_name:
                return
        grid.to_roxar(prj, rms_grid_model_name)  # type: ignore
    else:
        raise AttributeError(
            f'{__file__}: RMS project object does not have "grid_model" attribute '
            f"({print(prj)})s"
        )
    return


def export_results_disk(
    result_props: list[dict] | dict,
    grid: xtgeo.grid3d.Grid,
    grid_name: str,
    results_dir: Path,
    time_steps: list[str] | None = None,
    name_suffix: str = "",
    export_format: str = "roff",
) -> None:
    """Disk export of PEM results, all file names in lower case

    Args:
        result_props: list of dicts with properties to export
        grid: grid definition
        grid_name: name of grid
        results_dir: output directory
        time_steps: dates for simulation run
        name_suffix: extra string suffix for export names
        export_format: one of "roff" or "grdecl"

    Returns:
        None
    """
    result_props, time_steps = _verify_export_inputs(
        result_props, grid, time_steps, export_format
    )
    with restore_dir(results_dir):
        # First write the grid itself to disk
        if export_format == "grdecl":
            grid.to_file(grid_name.lower() + ".grdecl", fformat="grdecl")
        else:
            grid.to_file(grid_name.lower() + ".roff")
        out_file = ""
        for props, step in zip(result_props, time_steps):  # type: ignore
            if step != "":
                step = "--" + step
            if export_format == "grdecl":
                out_file = "pem" + step + ".grdecl"
                grid.units = None
                grid.to_file(out_file, fformat="grdecl")
            for key, value in props.items():
                attr_name = (
                    grid_name.lower() + "--" + key.lower() + name_suffix.lower() + step
                )
                grid_prop = xtgeo.grid3d.GridProperty(
                    grid, values=value, name=attr_name, date=step
                )
                if export_format == "grdecl":
                    grid_prop.to_file(
                        out_file, fformat="grdecl", append=True, name=key.upper()
                    )
                else:
                    grid_prop.to_file(attr_name + ".roff")  # "roff" is default format
