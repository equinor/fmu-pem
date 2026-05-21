from pathlib import Path

import numpy as np
import resfo
import xtgeo

from .enum_defs import PhaseSystem
from .pem_class_definitions import SimInitProperties, SimRstProperties
from .utils import bar_to_pa, restore_dir

# Eclipse stores the phase indicator in INTEHEAD item 15 (1-indexed).
_PHASE_INDICATOR_INDEX = 14


def read_init_properties(
    property_file: Path,
    sim_grid: xtgeo.Grid,
    fipnum_param: str,
) -> SimInitProperties:
    """Read initial properties from INIT file
    Args:
        property_file: Full path to the .INIT file
        sim_grid: The simulation grid to use for reading properties
        fipnum_param: Name for zone/region parameter, normally 'FIPNUM'
    Returns:
        SimInitProperties: The loaded initial grid properties
    """
    init_props = ["PORO", "DEPTH", "PVTNUM", "AQUIFERN"] + [fipnum_param]
    sim_init_props = xtgeo.gridproperties_from_file(
        property_file,
        fformat="init",
        names=init_props,
        grid=sim_grid,
        strict=(False, False),  # in case AQUIFERN
    )
    # Aquifer number is used to identify aquifer input cells, which may have
    # anomalous porosity values. Cells with negative numbers are added to inactive
    # (masked) cells
    if "AQUIFERN" in sim_init_props and np.any(sim_init_props["AQUIFERN"].values < 0):
        for key in init_props:
            # Don't change AQUIFERN
            if key != "AQUIFERN":
                sim_init_props[key].values = adjust_mask(
                    property=sim_init_props[key].values,
                    indicator=sim_init_props["AQUIFERN"].values,
                    threshold=0,
                    filter_below=True,
                )
    # Dictionary with lower-case names and the values as masked arrays
    props_dict = {
        sim_init_props[name].name.lower(): sim_init_props[name].values
        for name in sim_init_props.names
    }

    return SimInitProperties(**props_dict)


def create_rst_list(
    rst_props: xtgeo.GridProperties,
    seis_dates: list[str],
    rst_prop_names: list[str],
) -> list[SimRstProperties]:
    """Create list of SimRstProperties from raw restart properties

    Eclipse only writes the phase saturations that are physically present
    (e.g. only ``SWAT`` in a gas+water run). Any of ``SWAT``/``SGAS``/``SOIL``
    that is absent from ``rst_props`` is filled with a zero array shaped like
    the pressure field; ``reconcile_phase_saturations`` then derives the
    appropriate value using the run's :class:`PhaseSystem`.

    Args:
        rst_props: Raw restart properties
        seis_dates: list of dates to process
        rst_prop_names: list of property names to include
    Returns:
        list[SimRstProperties]: list of processed restart properties by date
    """
    saturation_names = {"SWAT", "SGAS", "SOIL"}
    result: list[SimRstProperties] = []
    for date in seis_dates:
        kwargs = {
            name.lower(): rst_props[name + "_" + date].values
            for name in rst_prop_names
            if name + "_" + date in rst_props.names
        }
        if "pressure" not in kwargs:
            raise ValueError(
                f"eclipse simulator restart file is missing PRESSURE for date {date}"
            )
        # Fill any missing phase saturation with zeros sized like pressure.
        pressure = kwargs["pressure"]
        zeros = np.ma.masked_array(np.zeros_like(pressure.data), mask=pressure.mask)
        for sat_name in saturation_names:
            kwargs.setdefault(sat_name.lower(), zeros)
        result.append(SimRstProperties(**kwargs))
    return result


def read_phase_system(unrst_file: Path) -> PhaseSystem:
    """Read the Eclipse phase indicator from INTEHEAD item 15 of a UNRST file.

    The UNRST file repeats the INTEHEAD record once per report step. The
    phase indicator is invariant within a run, so the first occurrence is
    used.

    Args:
        unrst_file: Path to the UNRST file.

    Returns:
        PhaseSystem flag enumerating the phases present in the simulation.

    Raises:
        ValueError: If no INTEHEAD record is found in the file, or if the
            phase indicator is zero or contains bits outside the documented
            ``OIL | WATER | GAS`` mask.
    """
    valid_mask = int(PhaseSystem.OIL | PhaseSystem.WATER | PhaseSystem.GAS)
    for keyword, values in resfo.read(unrst_file):
        if keyword.strip() == "INTEHEAD":
            indicator = int(values[_PHASE_INDICATOR_INDEX])
            if indicator == 0 or indicator & ~valid_mask:
                raise ValueError(
                    f"Unexpected phase indicator {indicator} in INTEHEAD item 15 "
                    f"of {unrst_file}; expected non-zero subset of 1|2|4."
                )
            return PhaseSystem(indicator)
    raise ValueError(f"No INTEHEAD record found in {unrst_file}")


def read_sim_grid_props(
    rel_dir_sim_files: Path,
    egrid_file: Path,
    init_property_file: Path,
    restart_property_file: Path,
    seis_dates: list[str],
    fipnum_name: str = "FIPNUM",
) -> tuple[xtgeo.Grid, SimInitProperties, list[SimRstProperties], PhaseSystem]:
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
        phase_system: phases present in the simulation (from INTEHEAD item 15)
    """
    sim_grid = xtgeo.grid_from_file(rel_dir_sim_files / egrid_file)

    init_props = read_init_properties(
        rel_dir_sim_files / init_property_file, sim_grid, fipnum_name
    )

    phase_system = read_phase_system(rel_dir_sim_files / restart_property_file)

    # TEMP will only be available for eclipse-300
    rst_props_names = ["SWAT", "SGAS", "SOIL", "RS", "RV", "PRESSURE", "SALT", "TEMP"]

    # Restart properties - set strict to False, False in case RV is not included in
    # the UNRST file. NB: This has the effect that other missing parameters will not
    # raise an error here, but that is handled by the following try-except statement.
    rst_props = xtgeo.gridproperties_from_file(
        rel_dir_sim_files / restart_property_file,
        fformat="unrst",
        names=rst_props_names,
        dates=seis_dates,
        grid=sim_grid,
        strict=(False, False),
    )

    # The mask of INIT properties may have been adjusted if there are cells indicated
    # as aquifers. The UNRST properties must be adjusted accordingly
    if init_props.aquifern is not None and np.any(init_props.aquifern < 0.0):
        for key in rst_props:
            rst_props[key.name].values = adjust_mask(
                property=rst_props[key.name].values,
                indicator=init_props.aquifern,
                threshold=0,
                filter_below=True,
            )

    # Formation pressure has unit `bar` in eclipse, but in the PEM models, unit
    # `Pa` is expected. Perform unit conversion before class objects are populated
    for date in seis_dates:
        rst_props["PRESSURE" + "_" + date].values = bar_to_pa(
            rst_props["PRESSURE" + "_" + date].values
        )

    try:
        rst_list = create_rst_list(rst_props, seis_dates, rst_props_names)
    except (AttributeError, TypeError, KeyError) as e:
        raise ValueError(f"eclipse simulator restart file is missing parameters: {e}")

    for rst in rst_list:
        rst.reconcile_phase_saturations(phase_system)

    return sim_grid, init_props, rst_list, phase_system


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
    with restore_dir(root_dir / fraction_path):
        try:
            grid_props = [
                xtgeo.gridproperty_from_file(
                    file,
                    name=name,  # type: ignore
                    grid=grd,  # type: ignore
                )
                for name in fraction_names
                for file in fraction_files
            ]
        except ValueError as exc:
            raise ImportError(
                f"{__file__}: failed to import volume fractions files {fraction_files}"
            ) from exc
    return [grid_prop.values for grid_prop in grid_props]


def adjust_mask(
    property: np.ma.MaskedArray,
    indicator: np.ma.MaskedArray,
    threshold: float = 0.0,
    filter_below: bool = True,
) -> np.ma.MaskedArray:
    """Adjust mask by adding to masked cells those where the `indicator`
    values are below (True) or above (False) the threshold.

    Parameters
    ----------
    property : np.ma.MaskedArray
        any grid property
    indicator : np.ma.MaskedArray
        a grid property used for flagging anomalous values
    threshold : float, optional
        threshold for accept/reject filter
    filter_below: bool
        keep values above(True) or below (False) the threshold

    Returns
    -------
    np.ma.MaskedArray
        grid property with modified mask
    """
    ind_mask = indicator < threshold if filter_below else indicator > threshold
    property.mask = np.logical_or(property.mask, ind_mask)
    return property
