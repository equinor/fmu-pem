import logging
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import numpy as np
import xtgeo

from .pem_class_definitions import EffectiveMineralProperties, PressureProperties


@contextmanager
def restore_dir(path: Path) -> Generator:  # type: ignore[return-value]
    """restore_dir run block of code from a given path, restore original path

    Args:
        path: path where the call is made from

    Returns:
        None
    """
    old_pwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_pwd)


def to_masked_array(
    value: float | int, masked_array: np.ma.MaskedArray
) -> np.ma.MaskedArray:
    """Create a masked array with a constant value from an int or float and a template
    masked array

    Args:
        value: constant value for the returned masked array
        masked_array: template for shape and mask of returned masked array

    Returns:
        constant value masked array
    """
    return np.ma.MaskedArray(value * np.ones_like(masked_array), mask=masked_array.mask)


def get_masked_array_mask(masked_array: np.ma.MaskedArray) -> np.ndarray:
    """Extract mask from MaskedArray or create default mask."""
    return (
        masked_array.mask
        if hasattr(masked_array, "mask")
        else np.zeros_like(masked_array.data, dtype=bool)
    )


def set_mask(
    masked_template: np.ma.MaskedArray,
    prop_array: np.ma.MaskedArray | None,
) -> np.ma.MaskedArray | None:
    """Check for existence of mask in masked_template, return prop_array
    with masked values. In case prop_array is None, return None"""
    if prop_array is None:
        return None
    return np.ma.masked_where(
        masked_template.mask
        if hasattr(masked_template, "mask")
        else np.zeros_like(prop_array),
        prop_array,
    )


def filter_and_one_dim(
    *args: np.ma.MaskedArray, return_numpy_array: bool = False
) -> tuple[np.ma.MaskedArray | np.ndarray, ...]:
    """Filters multiple masked arrays by removing masked values and flattens them to 1D.

    If no elements are masked (i.e., mask is scalar False), this function will still
    flatten the arrays to 1D by treating all entries as valid. This ensures
    downstream rock physics functions always receive 1D arrays, avoiding shape
    issues (e.g. (1, nx, ny, nz)) when no masking occurs.

    Args:
        *args: One or more masked arrays of identical shape. Each array contains data
            with some values potentially masked as invalid.
        return_numpy_array: If True, returns regular numpy arrays instead of
            masked arrays for the filtered data. Defaults to False.

    Returns:
        tuple containing:
            - mask: Boolean array of same shape where True indicates masked positions
            - filtered arrays: 1D arrays containing the unmasked values from each arg
    """
    if not np.all([isinstance(arg, np.ma.MaskedArray) for arg in args]):
        raise ValueError(f"{__file__}: all inputs should be numpy masked arrays")

    # Combine masks
    mask = args[0].mask
    for i in range(1, len(args)):
        mask = np.logical_or(mask, args[i].mask)

    # If mask is scalar (no masked elements), expand to full-shape False array
    if np.isscalar(mask):  # covers True/False scalar
        # All values valid -> create explicit False mask array matching input shape
        mask = np.zeros(args[0].shape, dtype=bool)

    # Extract unmasked (valid) entries and flatten to 1D
    if return_numpy_array:
        out_args = [arg.data[~mask] for arg in args]
    else:
        out_args = [arg[~mask] for arg in args]

    return mask, *out_args  # type: ignore[return-value]


def reverse_filter_and_restore(
    mask: np.ndarray, *args: np.ndarray
) -> tuple[np.ma.MaskedArray, ...]:
    """Restores 1D filtered arrays back to their original shape with masking.

    Typically called with results returned from the rock-physics library.

    Args:
        mask: Boolean array where True indicates positions that should be masked
            in the restored arrays.
        *args: One or more 1D numpy arrays containing the filtered values to be
            restored. Each array should contain exactly enough values to fill
            the unmasked positions in the mask.

    Returns:
        tuple of masked arrays where:
            - Each array has the same shape as the input mask
            - Unmasked positions contain values from the input args
            - Masked positions (where mask is True) contain zeros and are masked
            - All returned arrays share the same mask
    """
    out_args: list[np.ma.MaskedArray] = []
    for arg in args:
        tmp = np.zeros(mask.shape)
        tmp[~mask] = arg
        out_args.append(np.ma.MaskedArray(tmp, mask=mask))

    return tuple(out_args)


def _verify_export_inputs(props, grid, dates, file_format=None):
    if file_format is not None and file_format not in ["roff", "grdecl"]:
        raise ValueError(
            f'{__file__}: output file format must be one of "roff", "grdecl", is '
            f"{file_format}"
        )
    if not isinstance(grid, xtgeo.grid3d.Grid):
        raise ValueError(
            f"{__file__}: model grid is not an xtgeo 3D grid, type: {type(grid)}"
        )
    if isinstance(props, list):
        if isinstance(dates, list):
            if len(props) == len(dates):
                return props, dates
            raise ValueError(
                f"{__file__}: length of property list does not match the number of "
                f"simulation model "
                f"dates: {len(props)} vs. {len(dates)}"
            )
        if dates is None:
            return props, [""] * len(props)
        raise ValueError(
            f"{__file__}: unknown input type, time_steps should be None or list, is "
            f"{type(dates)}"
        )
    if isinstance(props, dict):
        props = [
            props,
        ]
        if dates is None:
            return props, [
                "",
            ]
        if isinstance(dates, list) and len(dates) == 1:
            return props, dates
        raise ValueError(
            f"{__file__}: single length property list does not match the number of "
            f"simulation model "
            f"dates: {len(dates)}"
        )
    raise ValueError(
        f"{__file__}: unknown input types, result_props should be list or dict, is "
        f"{type(props)}, time_steps should be None or list, is {type(dates)}"
    )


def get_shale_fraction(
    vol_fractions: list[np.ma.MaskedArray],
    fraction_names: list[str],
    shale_fraction_names: str | list[str] | None = None,
) -> np.ma.MaskedArray | None:
    """

    Args:
        vol_fractions: volume fractions, already verified that there is consistency
            between named fractions and available fractions in property file
        fraction_names: names of the volume fractions
        shale_fraction_names: Names of fractions that should be considered shale

    Returns:
        sum of volume fractions that are defined as shale, None if there are no defined
            shale fractions
    """

    if not shale_fraction_names:
        return None

    if isinstance(shale_fraction_names, str):
        shale_fraction_names = [shale_fraction_names]

    sh_list: list[np.ma.MaskedArray] = []
    for shale_name in shale_fraction_names:
        try:
            idx = fraction_names.index(shale_name)
            sh_list.append(vol_fractions[idx])
        except ValueError:
            raise ValueError(f"unknown shale fraction: {shale_name}")

    # Note that masked elements are set to 0 internally.
    return np.ma.sum(sh_list, axis=0)


def estimate_cement(
    bulk_modulus: float | int,
    shear_modulus: float | int,
    density: float | int,
    grid: np.ma.MaskedArray,
) -> EffectiveMineralProperties:
    """Creates masked arrays filled with constant cement properties, matching the shape
    and mask of the input grid.

    Args:
        bulk_modulus: Bulk modulus of the cement
        shear_modulus: Shear modulus of the cement
        density: Density of the cement
        grid: Template array that defines the shape and mask for the output arrays

    Returns:
        cement properties as MatrixProperties containing constant-valued masked arrays
    """
    cement_k = to_masked_array(bulk_modulus, grid)
    cement_mu = to_masked_array(shear_modulus, grid)
    cement_rho = to_masked_array(density, grid)
    return EffectiveMineralProperties(
        bulk_modulus=cement_k, shear_modulus=cement_mu, density=cement_rho
    )


def update_dict_list(base_list: list[dict], add_list: list[dict]) -> list[dict]:
    """Update/add new key/value pairs to dicts in list

    Args:
        base_list: original list of dicts
        add_list: list of dicts to be added

    Returns:
        combined list of dicts
    """
    _verify_update_inputs(base_list, add_list)
    for i, item in enumerate(add_list):
        base_list[i].update(item)
    return base_list


def _verify_update_inputs(base, add_list):
    if not isinstance(base, list) and isinstance(add_list, list):
        raise TypeError(f"{__file__}: inputs are not lists")
    if not len(base) == len(add_list):
        raise ValueError(
            f"{__file__}: mismatch in list lengths: base list: {len(base)} vs. added "
            f"list: {len(add_list)}"
        )
    if not (
        all(isinstance(item, dict) for item in base)
        and all(isinstance(item, dict) for item in add_list)
    ):
        raise TypeError(f"{__file__}: all items in input lists are not dict")


def bar_to_pa(
    pres_bar: float | np.ndarray | np.ma.MaskedArray,
) -> float | np.ndarray | np.ma.MaskedArray:
    """
    Pressure unit conversion from bar to Pa
    """
    return pres_bar * 1.0e5


def pa_to_bar(
    pres_pa: float | np.ndarray | np.ma.MaskedArray,
) -> float | np.ndarray | np.ma.MaskedArray:
    """
    Pressure unit conversion from Pa to bar
    """
    return pres_pa * 1.0e-5


def convert_single_pressure_to_pa(
    single_press_bar: PressureProperties,
) -> PressureProperties:
    return PressureProperties(
        effective_pressure=bar_to_pa(single_press_bar.effective_pressure),
        formation_pressure=bar_to_pa(single_press_bar.formation_pressure),
        overburden_pressure=bar_to_pa(single_press_bar.overburden_pressure),
    )


def convert_pressures_list_to_pa(
    press_bar: list[PressureProperties],
) -> list[PressureProperties]:
    return [convert_single_pressure_to_pa(pres) for pres in press_bar]


def _format_elapsed(seconds: float) -> str:
    minutes, secs = divmod(seconds, 60)
    return f"{int(minutes)} min {secs:5.2f} sec"


_run_start_time: float | None = None


class _ElapsedFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level = "" if record.levelno == logging.INFO else f" {record.levelname}"
        if _run_start_time is None:
            return f"PEM{level}: {record.getMessage()}"
        elapsed = time.monotonic() - _run_start_time
        return f"PEM [{_format_elapsed(elapsed)}]{level}: {record.getMessage()}"


_PEM_FORMATTER = _ElapsedFormatter()

pem_logger = logging.getLogger("fmu.pem")
pem_logger.setLevel(logging.WARNING)
pem_logger.propagate = False

_stderr_handler = logging.StreamHandler(sys.stderr)
_stderr_handler.setFormatter(_PEM_FORMATTER)
_stderr_handler.setLevel(logging.WARNING)
pem_logger.addHandler(_stderr_handler)

_stdout_handler: logging.Handler | None = None


def start_pem_run_log(level: int = logging.INFO) -> None:
    """Activate verbose PEM run logging.

    Anchors the elapsed-time origin and attaches a stdout handler for
    records below ``WARNING``. ``WARNING`` and above always reach stderr,
    independent of this call. Repeated calls are no-ops; call
    :func:`stop_pem_run_log` first to re-anchor.
    """
    global _run_start_time, _stdout_handler
    if _run_start_time is not None:
        return
    _run_start_time = time.monotonic()

    _stdout_handler = logging.StreamHandler(sys.stdout)
    _stdout_handler.setFormatter(_PEM_FORMATTER)
    _stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)

    pem_logger.setLevel(level)
    pem_logger.addHandler(_stdout_handler)


def stop_pem_run_log() -> None:
    """Deactivate verbose PEM run logging.

    Detaches the stdout handler and resets the elapsed-time origin. The
    stderr handler for ``WARNING`` and above remains attached.
    """
    global _run_start_time, _stdout_handler
    if _stdout_handler is not None:
        pem_logger.removeHandler(_stdout_handler)
        _stdout_handler = None
    pem_logger.setLevel(logging.WARNING)
    _run_start_time = None


def pem_log(message: str, level: int = logging.INFO) -> None:
    """Emit ``message`` on the PEM logger at ``level`` (default ``INFO``).

    ``INFO``/``DEBUG`` go to stdout only while :func:`start_pem_run_log` is
    active. ``WARNING``/``ERROR``/``CRITICAL`` always go to stderr.
    """
    pem_logger.log(level, message)
