from pathlib import Path

import numpy as np
import resfo
import xtgeo

from .enum_defs import PhaseSystem
from .pem_class_definitions import SimInitProperties, SimRstProperties
from .pem_config_validation import (
    ConstantNonNetPorosity,
    NoPorosityAdjustment,
    PorosityAdjustment,
    PreAdjustedPorosityGrid,
)
from .utils import bar_to_pa, restore_dir

# Eclipse stores the phase indicator in INTEHEAD item 15 (1-indexed) and the
# simulator program identifier (IPROG) in item 95.
_PHASE_INDICATOR_INDEX = 14
_IPROG_INDEX = 94

# IPROG values written by Eclipse 300 (regular and thermal). Eclipse 300 always
# carries oil, water and gas internally, regardless of which phases are active
# in the deck, so the per-run phase indicator in INTEHEAD item 15 is not
# reliable for these runs. Eclipse 100 uses 100 and OPM Flow mirrors that.
_ECLIPSE_300_IPROG = {300, 500}


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
        SimInitProperties: The loaded initial grid properties. ``ntg`` is
        populated when the NTG keyword is present in the INIT file and
        left as ``None`` otherwise.
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
    try:
        ntg_prop = xtgeo.gridproperty_from_file(
            property_file, fformat="init", name="NTG", grid=sim_grid
        )
        props_dict["ntg"] = ntg_prop.values
    except (ValueError, KeyError):
        # NTG is optional; absence means each cell is treated as fully net.
        pass
    return SimInitProperties(**props_dict)


def create_rst_list(
    rst_props: xtgeo.GridProperties,
    seis_dates: list[str],
    rst_prop_names: list[str],
) -> list[SimRstProperties]:
    """Create list of SimRstProperties from raw restart properties

    Eclipse and OPM Flow only writes the phase saturations that are physically present
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
    """Read the phase system in use from the first INTEHEAD record of a UNRST file.

    The UNRST file repeats the INTEHEAD record once per report step. The
    phase indicator is invariant within a run, so the first occurrence is
    used.

    The simulator program identifier (INTEHEAD item 95, ``IPROG``) is
    inspected first. Eclipse 300 (``IPROG`` 300 or 500) always carries
    oil, water and gas internally regardless of the active phases in the
    deck, so the phase indicator in item 15 is unreliable; the function
    returns ``OIL | WATER | GAS`` for those runs. For Eclipse 100 and OPM
    Flow (``IPROG`` 100) the phase indicator in item 15 is used.

    Args:
        unrst_file: Path to the UNRST file.

    Returns:
        PhaseSystem flag enumerating the phases present in the simulation.

    Raises:
        ValueError: If no INTEHEAD record is found in the file, or if the
            phase indicator is zero or contains bits outside the documented
            ``OIL | WATER | GAS`` mask (Eclipse 100 / OPM Flow only).
    """
    valid_mask = int(PhaseSystem.OIL | PhaseSystem.WATER | PhaseSystem.GAS)
    for keyword, values in resfo.read(unrst_file):
        if keyword.strip() == "INTEHEAD":
            iprog = int(values[_IPROG_INDEX])
            if iprog in _ECLIPSE_300_IPROG:
                return PhaseSystem(valid_mask)
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


def apply_porosity_adjustment(
    adjustment: PorosityAdjustment,
    sim_init: SimInitProperties,
    sim_grid: xtgeo.Grid,
    root_dir: Path,
) -> None:
    """Adjust ``sim_init.poro`` in-place according to the configured option.

    Three options are supported:

    * :class:`NoPorosityAdjustment`: leave PORO unchanged.
    * :class:`ConstantNonNetPorosity`: use ``sim_init.ntg`` (read from the
      Eclipse INIT file by :func:`read_init_properties`) to apply
      ``por_tot = ntg * PORO + (1 - ntg) * non_net_porosity``.
    * :class:`PreAdjustedPorosityGrid`: replace PORO with the values of a
      grid parameter file (already containing the NTG-adjusted total
      porosity).
    """
    if isinstance(adjustment, NoPorosityAdjustment):
        return

    if isinstance(adjustment, ConstantNonNetPorosity):
        if sim_init.ntg is None:
            raise ImportError(
                "NTG is required for the constant non-net porosity adjustment "
                "but is not present in the Eclipse INIT file."
            )
        ntg = np.ma.masked_array(sim_init.ntg.data, mask=sim_init.poro.mask)
        _verify_ntg_is_non_binary(ntg)
        sim_init.poro = ntg * sim_init.poro + (1.0 - ntg) * adjustment.non_net_porosity
        return

    if isinstance(adjustment, PreAdjustedPorosityGrid):
        grid_file = root_dir / adjustment.rel_path / adjustment.file_name
        try:
            new_poro = xtgeo.gridproperty_from_file(grid_file, grid=sim_grid)
        except (ValueError, FileNotFoundError) as exc:
            raise ImportError(
                f"failed to import pre-adjusted porosity grid {grid_file}"
            ) from exc
        except IndexError as exc:
            raise ValueError(
                f"pre-adjusted porosity grid {grid_file} does not match the "
                f"simulation grid dimensions {tuple(sim_grid.dimensions)}."
            ) from exc
        _verify_grid_dimensions_match(new_poro, sim_grid, grid_file)
        _verify_pre_adjusted_poro_mask_compatibility(
            new_poro.values, sim_init.poro, grid_file
        )
        sim_init.poro = np.ma.masked_array(
            new_poro.values.data, mask=sim_init.poro.mask
        )
        return

    raise TypeError(f"unsupported porosity adjustment type: {type(adjustment)!r}")


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


def _verify_grid_dimensions_match(
    grid_prop: xtgeo.GridProperty,
    sim_grid: xtgeo.Grid,
    source: Path,
) -> None:
    """Raise if ``grid_prop`` does not have the same (ncol, nrow, nlay) as
    the simulation grid.
    """
    grid_dims = sim_grid.dimensions
    value_dims = tuple(grid_prop.values.shape)
    prop_dims = (grid_prop.ncol, grid_prop.nrow, grid_prop.nlay)
    if value_dims != tuple(grid_dims) or prop_dims != tuple(grid_dims):
        raise ValueError(
            f"pre-adjusted porosity grid {source} has dimensions {prop_dims} "
            f"(values shape {value_dims}) which do not match the simulation "
            f"grid dimensions {tuple(grid_dims)}."
        )


def _verify_pre_adjusted_poro_mask_compatibility(
    new_poro: np.ma.MaskedArray,
    reference_poro: np.ma.MaskedArray,
    source: Path,
) -> None:
    """Raise if ``new_poro`` masks cells that are active in ``reference_poro``.

    The pre-adjusted grid is considered invalid input if it masks cells that are
    active in the simulation PORO mask.
    """
    new_mask = np.ma.getmaskarray(new_poro)
    reference_mask = np.ma.getmaskarray(reference_poro)
    invalid_mask = new_mask & ~reference_mask
    if np.any(invalid_mask):
        raise ValueError(
            f"pre-adjusted porosity grid {source} masks active simulation cells; "
            "input mask must be compatible with the simulation PORO mask."
        )


def _verify_ntg_is_non_binary(ntg: np.ma.MaskedArray, atol: float = 1.0e-3) -> None:
    """Raise if NTG values are effectively binary (only 0 or 1 within ``atol``).

    The constant non-net porosity adjustment is only meaningful when the
    upscaled NTG is a continuous fraction; a binary NTG indicates the
    adjustment is misconfigured.
    """
    values = ntg.compressed()
    if values.size == 0:
        return
    is_zero_or_one = np.isclose(values, 0.0, atol=atol) | np.isclose(
        values, 1.0, atol=atol
    )
    if np.all(is_zero_or_one):
        raise ValueError(
            "NTG read from the Eclipse INIT file is binary (all values within "
            f"{atol} of 0 or 1); the constant non-net porosity adjustment is "
            "only meaningful for a non-binary, fractional NTG."
        )
