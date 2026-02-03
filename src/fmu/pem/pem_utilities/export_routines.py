import warnings
from dataclasses import asdict
from pathlib import Path

import numpy as np
import xtgeo

from .enum_defs import Sim2SeisRequiredParams
from .pem_class_definitions import (
    DryRockProperties,
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SaturatedRockProperties,
)
from .utils import _verify_export_inputs, restore_dir


def save_results(
    config_dir: Path,
    sim_grid: xtgeo.grid3d.Grid,
    grid_name: str,
    seis_dates: list[str],
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
    bubble_point_grids: list[dict[str, np.ma.MaskedArray]],
    dry_rock_props: list[DryRockProperties],
) -> None:
    """Saves all intermediate and final results according to the settings in the PEM
    and global config files

    Args:
        config_dir: initial directory setting
        sim_grid: grid definition
        grid_name: stem of output grid name
        seis_dates: list of dates for simulation runs
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
    full_mandatory_path = config_dir / mandatory_path
    full_output_path = config_dir / pem_output_path
    output_set = [
        {
            k: v
            for (k, v) in asdict(sat_prop).items()
            if k in list(Sim2SeisRequiredParams)
        }
        for sat_prop in sat_rock_props
    ]
    export_results_disk(
        result_props=output_set,
        grid=sim_grid,
        grid_name=grid_name,
        results_dir=full_mandatory_path,
        time_steps=seis_dates,
        export_format="grdecl",
    )

    # 2. Save results to disk according to config file

    # create list of dict from list of pressure and saturated rock objects
    eff_pres_dict_list = [asdict(obj) for obj in eff_pres_props]
    sat_prop_dict_list = [asdict(obj) for obj in sat_rock_props]

    try:
        if save_to_disk:
            for props in [eff_pres_dict_list, sat_prop_dict_list]:
                prop_dict = list(props)
                export_results_disk(
                    result_props=prop_dict,
                    grid=sim_grid,
                    grid_name=sim_grid.name,
                    results_dir=full_output_path,
                    time_steps=seis_dates,
                )
            export_results_disk(
                result_props=difference_props,
                grid=sim_grid,
                grid_name=grid_name,
                results_dir=full_output_path,
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
            export_dicts = [
                [asdict(fl_props) for fl_props in fluid_props],
                asdict(matrix_props),
                bubble_point_grids,
                [asdict(dry_props) for dry_props in dry_rock_props],
            ]
            suffices = [
                "_FLUID",
                "_MINERAL",
                "",
                "_DRY_ROCK",
            ]
            dates = [seis_dates, None, seis_dates, seis_dates]
            for props, date_info, suffix in zip(export_dicts, dates, suffices):
                export_results_disk(
                    result_props=props,
                    grid=sim_grid,
                    grid_name=grid_name,
                    results_dir=full_output_path,
                    time_steps=date_info,
                    name_suffix=suffix,
                )
    except KeyError:
        # just skip silently if save_intermediate_results is not present in the
        # pem_config
        pass
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
