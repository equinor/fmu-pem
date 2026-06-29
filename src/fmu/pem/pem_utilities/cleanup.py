from datetime import datetime
from pathlib import Path
from typing import Iterator

from fmu.pem.pem_utilities.enum_defs import SaveTypes

# Exported result files follow the grammar ``<grid>--<attribute>[--<date(s)>].<ext>``
# (separator is ``--``). Dates are formatted as ``YYYYMMDD``; a difference property
# carries two of them joined by an underscore, e.g. ``20180701_20180101``.
_DATE_FORMAT = "%Y%m%d"

# Substrings in the attribute token that mark a QC/intermediate result. ``pressure``
# also captures ``effective_pressure`` and ``overburden_pressure``; the ``_fluid`` /
# ``_mineral`` / ``_dry_rock`` markers also catch the intermediate ``density`` grids.
_INTERMEDIATE_MARKERS = (
    "_mineral",
    "_fluid",
    "_dry_rock",
    "below_bubble_point",
    "adjusted_porosity",
    "pressure",
)

# The three "property" save types; the grid itself is handled separately.
_PROPERTY_CATEGORIES = (
    SaveTypes.INTERMEDIATE_PROPERTIES,
    SaveTypes.ELASTIC_PROPERTIES,
    SaveTypes.DIFFERENCE_PROPERTIES,
)

# Result grids live in the FMU ``<run>/share/results/grids`` directory; ensemble runs
# add a ``<project>/realization-<n>/iter-<m>/`` prefix (see ERT RUNPATH).
_GRIDS_SUBPATH = ("share", "results", "grids")
_GRIDS_GLOB = "/".join(_GRIDS_SUBPATH)
_REALIZATION_GLOB = "realization-*/iter-*"


def _count_dates(text: str) -> int:
    """Count valid ``YYYYMMDD`` dates in an underscore-separated string.

    Validation uses :func:`datetime.strptime`, so only real calendar dates are
    counted rather than any run of eight digits.
    """
    dates = 0
    for token in text.split("_"):
        try:
            datetime.strptime(token, _DATE_FORMAT)
        except ValueError:
            continue
        dates += 1
    return dates


def categorise_filename(filename: Path) -> SaveTypes | None:
    """Classify a single result file into one of the :class:`SaveTypes`.

    Classification is driven by the structure of the name (split on ``--``) and the
    number of dates it carries:

    - two dates                     -> difference property
    - an intermediate marker        -> intermediate property (with or without date)
    - a single date, no marker      -> elastic property
    - no attribute (bare grid name) -> grid

    Returns ``None`` for files that do not match the expected pattern.
    """
    # parts == [grid] for the grid itself, otherwise [grid, attribute, date(s)?].
    parts = filename.stem.split("--")
    if len(parts) == 1:
        return SaveTypes.GRID

    attribute = parts[1]
    date_part = parts[2] if len(parts) > 2 else ""
    n_dates = _count_dates(date_part)

    if n_dates == 2:
        return SaveTypes.DIFFERENCE_PROPERTIES
    if any(marker in attribute for marker in _INTERMEDIATE_MARKERS):
        return SaveTypes.INTERMEDIATE_PROPERTIES
    if n_dates == 1:
        return SaveTypes.ELASTIC_PROPERTIES
    return None


def make_type_dict(
    directory_path: Path,
    suffix: str = "simgrid",
    extension: str = ".roff",
) -> dict[Path, SaveTypes]:
    """Map every matching file in ``directory_path`` to its :class:`SaveTypes`.

    Only files whose name starts with ``suffix`` and ends with ``extension`` are
    considered; unrecognised names are skipped.
    """
    type_dict: dict[Path, SaveTypes] = {}
    for file_path in sorted(directory_path.glob(f"{suffix}*{extension}")):
        category = categorise_filename(file_path)
        if category is not None:
            type_dict[file_path] = category
    return type_dict


def remove_files(file_names: list[Path]) -> None:
    """Unlink every file in ``file_names``.

    Raises ``OSError`` if one or more files could not be deleted.
    """
    not_deleted = []
    for file_name in file_names:
        try:
            file_name.unlink(missing_ok=True)
        except OSError:
            not_deleted.append(file_name)
    if not_deleted:
        raise OSError(
            "cleanup: could not delete the following files: "
            + ", ".join(str(path) for path in not_deleted)
        )


def crawl_ensemble(directory_path: Path) -> Iterator[Path]:
    """Yield the ``share/results/grids`` directory of every realisation/iteration.

    ``directory_path`` MUST be the top of the ensemble, i.e. directly contain
    ``realization-<n>/iter-<m>`` subdirectories (no upward or recursive search is
    performed). Raises ``ValueError`` if it is not.
    """
    directory_path = directory_path.resolve()
    grids_dirs = sorted(
        path
        for path in directory_path.glob(f"{_REALIZATION_GLOB}/{_GRIDS_GLOB}")
        if path.is_dir()
    )
    if not grids_dirs:
        raise ValueError(
            f"cleanup: {directory_path} is not the top of an FMU ensemble; expected "
            "'realization-*/iter-*' subdirectories below it"
        )
    yield from grids_dirs


def _is_grids_dir(path: Path) -> bool:
    """Return ``True`` if ``path`` is an FMU ``.../share/results/grids`` directory."""
    return path.is_dir() and path.parts[-len(_GRIDS_SUBPATH) :] == _GRIDS_SUBPATH


def _find_run_grids_dir(directory_path: Path) -> Path:
    """Resolve the single ``share/results/grids`` directory of a one-off run.

    Accepts exactly one of:

    - the grids directory itself (``.../share/results/grids``), or
    - the FMU run root that contains it directly (as returned by
      ``_resolve_fmu_rootpath``).

    No upward or recursive search is performed, so an unrelated parent can never be
    matched. Raises ``ValueError`` for any other location.
    """
    directory_path = directory_path.resolve()
    if _is_grids_dir(directory_path):
        return directory_path
    run_grids = directory_path.joinpath(*_GRIDS_SUBPATH)
    if _is_grids_dir(run_grids):
        return run_grids
    raise ValueError(
        f"cleanup: {directory_path} is not a single FMU run location; expected a "
        "'share/results/grids' directory or an FMU run root that contains it directly"
    )


def _normalise_remove_categories(
    remove_categories: list[SaveTypes | str],
) -> list[SaveTypes]:
    """Coerce each requested category to a :class:`SaveTypes` member.

    Plain strings matching a save-type value (e.g. ``"elastic"``) are accepted and
    converted. Raises ``ValueError`` with the list of valid options for any value
    that is not a recognised save type, so typos fail loudly instead of silently
    deleting nothing.
    """
    normalised = []
    for category in remove_categories:
        try:
            normalised.append(SaveTypes(category))
        except ValueError:
            raise ValueError(
                f"cleanup: '{category}' is not a valid save type; "
                f"expected one of: {SaveTypes.options()}"
            ) from None
    return normalised


def _resolve_remove_categories(remove_categories: list[SaveTypes]) -> set[SaveTypes]:
    """Expand the requested categories into the concrete set of types to delete.

    The grid is removed only alongside everything else: either when ``SaveTypes.ALL``
    is requested, or when all three property categories are listed explicitly.
    """
    requested = set(remove_categories)
    if SaveTypes.ALL in requested or set(_PROPERTY_CATEGORIES).issubset(requested):
        return {*_PROPERTY_CATEGORIES, SaveTypes.GRID}
    # Otherwise act only on the requested property categories, never the grid.
    return requested & set(_PROPERTY_CATEGORIES)


def cleanup_pem_results(
    directory: Path,
    prefix: str,
    extension: str,
    remove_categories: list[SaveTypes | str],
    is_ensemble: bool = False,
) -> None:
    """Remove selected PEM result files from a single run or a whole ensemble.

    ``directory`` must be one of a small set of well-defined FMU locations; no upward
    or recursive search is performed, so an unrelated parent can never be matched:

    - ``is_ensemble=False`` (single run): the ``share/results/grids`` directory itself,
      or the FMU run root that contains it directly (as returned by
      ``_resolve_fmu_rootpath``).
    - ``is_ensemble=True`` (ensemble): the top of the ensemble, which MUST directly
      contain ``realization-<n>/iter-<m>`` subdirectories; every realisation/iteration
      ``share/results/grids`` directory is then processed.

    A ``ValueError`` is raised if ``directory`` does not match the requested run type.

    If SaveTypes.ALL is in the list, all recognised files are deleted. If not, files
    are deleted according to categories.

    SaveTypes.GRID is only removed if SaveTypes.ALL is set, or the three distinct
    categories are all given.

    Parameters
    ----------
    directory : Path
        The ensemble top (``is_ensemble=True``) or a single-run grids/root directory.
    prefix : str
        Grid-name prefix of the files to consider (e.g. ``"simgrid"``).
    extension : str
        File extension of the files to consider (e.g. ``".roff"``).
    remove_categories : list[SaveTypes | str]
        Categories of files to delete. Plain strings matching a save-type value
        (e.g. ``"elastic"``) are accepted; an unrecognised value raises
        ``ValueError``.
    is_ensemble : bool, optional
        Treat ``directory`` as part of an ensemble, by default False.
    """
    categories = _normalise_remove_categories(remove_categories)
    if is_ensemble:
        grids_dirs: Iterator[Path] = crawl_ensemble(directory)
    else:
        grids_dirs = iter([_find_run_grids_dir(directory)])
    categories_to_remove = _resolve_remove_categories(categories)
    for grids_dir in grids_dirs:
        type_dict = make_type_dict(grids_dir, prefix, extension)
        remove_files(
            [
                path
                for path, category in type_dict.items()
                if category in categories_to_remove
            ]
        )
