from pathlib import Path

import numpy as np
import xtgeo

from .pem_class_definitions import SimInitProperties, SimRstProperties
from .pem_config_validation import PemConfig
from .utils import restore_dir


def read_init_properties(
    property_file: Path, sim_grid: xtgeo.Grid
) -> SimInitProperties:
    """Read initial properties from INIT file
    Args:
        property_file: Full path to the .INIT file
        sim_grid: The simulation grid to use for reading properties
    Returns:
        SimInitProperties: The loaded initial grid properties
    """
    INIT_PROPS = ["PORO", "DEPTH"]
    sim_init_props = xtgeo.gridproperties_from_file(
        property_file, fformat="init", names=INIT_PROPS, grid=sim_grid
    )
    props_dict = {
        sim_init_props[name].name.lower(): sim_init_props[name].values
        for name in INIT_PROPS
    }
    return SimInitProperties(**props_dict)


def create_rst_list(
    rst_props: xtgeo.GridProperties,
    seis_dates: list[str],
    rst_prop_names: list[str],
) -> list[SimRstProperties]:
    """Create list of SimRstProperties from raw restart properties
    Args:
        rst_props: Raw restart properties
        seis_dates: list of dates to process
        rst_prop_names: list of property names to include
    Returns:
        list[SimRstProperties]: list of processed restart properties by date
    """
    return [
        SimRstProperties(
            **{
                name.lower(): rst_props[name + "_" + date].values
                for name in rst_prop_names
                if name + "_" + date in rst_props.names
            }
        )
        for date in seis_dates
    ]


def read_sim_grid_props(
    rel_dir_sim_files: Path,
    egrid_file: Path,
    init_property_file: Path,
    restart_property_file: Path,
    seis_dates: list[str],
) -> tuple[xtgeo.Grid, SimInitProperties, list[SimRstProperties]]:
    """Read grid and properties from simulation run, both initial and restart properties

    Args:
        rel_dir_sim_files: start dir for PEM script run
        egrid_file: Path to the EGRID file
        init_property_file: Path to the INIT file
        restart_property_file: Path to the UNRST file
        seis_dates: list of dates for which to read restart properties

    Returns:
        sim_grid: grid definition for eclipse input
        init_props: object with initial properties of simulation grid
        rst_list: list with time-dependent simulation properties
    """
    sim_grid = xtgeo.grid_from_file(rel_dir_sim_files / egrid_file)

    init_props = read_init_properties(rel_dir_sim_files / init_property_file, sim_grid)

    # TEMP will only be available for eclipse-300
    RST_PROPS = ["SWAT", "SGAS", "SOIL", "RS", "RV", "PRESSURE", "SALT", "TEMP"]

    # Restart properties - set strict to False, False in case RV is not included in
    # the UNRST file. NB: This has the effect that other missing parameters will not
    # raise an error here, but that is handled by the following try-except statement.
    rst_props = xtgeo.gridproperties_from_file(
        rel_dir_sim_files / restart_property_file,
        fformat="unrst",
        names=RST_PROPS,
        dates=seis_dates,
        grid=sim_grid,
        strict=(False, False),
    )

    try:
        rst_list = create_rst_list(rst_props, seis_dates, RST_PROPS)
    except (AttributeError, TypeError) as e:
        raise ValueError(f"eclipse simulator restart file is missing parameters: {e}")

    return sim_grid, init_props, rst_list


def import_fractions(
    root_dir: Path,
    fraction_path: Path,
    fraction_files: list[Path],
    fraction_names: list[str],
    grd: xtgeo.Grid,
) -> list:
    """Import volume fractions

    Args:
        root_dir (str): model directory, relative paths refer to it
        fraction_path: path to the fractions files
        fraction_files: list of fraction files
        fraction_names: list of parameter names in fraction files
        grd (xtgeo.Grid): model grid

    Returns:
        list: fraction properties
    """
    with restore_dir(root_dir.joinpath(fraction_path)):
        try:
            grid_props = [
                xtgeo.gridproperty_from_file(
                    file,
                    name=name,
                    grid=grd,
                )
                for name in fraction_names
                for file in fraction_files
            ]
        except ValueError as exc:
            raise ImportError(
                f"{__file__}: failed to import volume fractions files {fraction_files}"
            ) from exc
    return [grid_prop.values for grid_prop in grid_props]
