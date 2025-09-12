from pathlib import Path
from typing import List, Tuple

import numpy as np
import xtgeo

from .pem_class_definitions import SimInitProperties, SimRstProperties
from .pem_config_validation import PemConfig
from .utils import restore_dir


def read_geogrid(root_dir: Path, config: PemConfig) -> dict:
    """Not in use? Read porosity from geo-grid

    Args:
        root_dir: start dir for PEM script run
        config: PEM specific parameters

    Returns:
        Dict object with porosity
    """
    with restore_dir(root_dir.joinpath(config.paths.rel_path_geogrid)):
        return {"poro": xtgeo.gridproperty_from_file("geogrid--phit.roff").values}


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
    INIT_PROPS = ["PORO", "DEPTH", "NTG"]
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
    seis_dates: List[str],
    rst_prop_names: List[str],
) -> List[SimRstProperties]:
    """Create list of SimRstProperties from raw restart properties
    Args:
        rst_props: Raw restart properties
        seis_dates: List of dates to process
        rst_prop_names: List of property names to include
    Returns:
        List[SimRstProperties]: List of processed restart properties by date
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
    egrid_file: Path,
    init_property_file: Path,
    restart_property_file: Path,
    seis_dates: List[str],
) -> Tuple[xtgeo.Grid, SimInitProperties, List[SimRstProperties]]:
    """Read grid and properties from simulation run, both initial and restart properties

    Args:
        egrid_file: Path to the EGRID file
        init_property_file: Path to the INIT file
        restart_property_file: Path to the UNRST file
        seis_dates: List of dates for which to read restart properties

    Returns:
        sim_grid: grid definition for eclipse input
        init_props: object with initial properties of simulation grid
        rst_list: list with time-dependent simulation properties
    """
    sim_grid = xtgeo.grid_from_file(egrid_file)

    init_props = read_init_properties(init_property_file, sim_grid)

    # TEMP will only be available for eclipse-300
    RST_PROPS = ["SWAT", "SGAS", "SOIL", "RS", "RV", "PRESSURE", "SALT", "TEMP"]

    # Restart properties - set strict to False, False in case RV is not included in
    # the UNRST file
    rst_props = xtgeo.gridproperties_from_file(
        restart_property_file,
        fformat="unrst",
        names=RST_PROPS,
        dates=seis_dates,
        grid=sim_grid,
        strict=(False, False),
    )

    rst_list = create_rst_list(rst_props, seis_dates, RST_PROPS)

    return sim_grid, init_props, rst_list


def read_ntg_grid(ntg_grid_file: Path) -> np.ma.MaskedArray:
    """Read PEM specific NTG property
    Args:
        ntg_grid_file: path to the NTG grid file
    Returns:
        net to gross property from simgrid adapted to PEM definition
    """
    return xtgeo.gridproperty_from_file(ntg_grid_file).values


def import_fractions(root_dir: Path, config: PemConfig, grd: xtgeo.Grid) -> list:
    """Import volume fractions

    Args:
        root_dir (str): model directory, relative paths refer to it
        config (PemConfig): configuration file with PEM parameters
        grd (xtgeo.Grid): model grid

    Returns:
        list: fraction properties
    """
    with restore_dir(
        root_dir.joinpath(config.rock_matrix.volume_fractions.rel_path_fractions)
    ):
        try:
            fracs = config.rock_matrix.fraction_names
            grid_props = [
                xtgeo.gridproperty_from_file(
                    file,
                    name=name,
                    grid=grd,
                )
                for name in fracs
                for file in config.rock_matrix.volume_fractions.fractions_prop_file_names  # noqa: E501
            ]
        except ValueError as exc:
            raise ImportError(
                f"{__file__}: failed to import volume fractions files "
                f"{config.rock_matrix.volume_fractions.fractions_prop_file_names}"
            ) from exc
    return [grid_prop.values for grid_prop in grid_props]
