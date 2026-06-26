"""Tests for the post-run cleanup utilities in
:mod:`fmu.pem.pem_utilities.cleanup`.

The tests cover filename classification, the date-string detection, the strict
resolution of FMU run/ensemble locations, and the end-to-end removal behaviour of
:func:`cleanup_pem_results`.
"""

from pathlib import Path

import pytest

from fmu.pem.pem_utilities.cleanup import (
    _count_dates,
    _find_run_grids_dir,
    _is_grids_dir,
    _normalise_remove_categories,
    _resolve_remove_categories,
    categorise_filename,
    cleanup_pem_results,
    crawl_ensemble,
    make_type_dict,
    remove_files,
)
from fmu.pem.pem_utilities.enum_defs import SaveTypes

# A representative set of exported result files, grouped by expected category.
GRID_FILES = ["simgrid.roff"]
ELASTIC_FILES = [
    "simgrid--vp--20180101.roff",
    "simgrid--density--20180101.roff",
]
INTERMEDIATE_FILES = [
    "simgrid--pressure--20180101.roff",
    "simgrid--density_fluid--20180101.roff",
    "simgrid--bulk_modulus_mineral.roff",
]
DIFFERENCE_FILES = ["simgrid--sidiffpercent--20180701_20180101.roff"]
UNRELATED_FILES = ["notes.txt"]
RESULT_FILES = GRID_FILES + ELASTIC_FILES + INTERMEDIATE_FILES + DIFFERENCE_FILES


def _populate(grids_dir: Path) -> None:
    """Create the representative result files (plus an unrelated file) in grids_dir."""
    grids_dir.mkdir(parents=True, exist_ok=True)
    for name in RESULT_FILES + UNRELATED_FILES:
        (grids_dir / name).touch()


def _make_ensemble(root: Path, n_real: int = 2) -> list[Path]:
    """Build an ensemble tree below root and return the populated grids directories."""
    grids_dirs = []
    for realization in range(n_real):
        grids_dir = (
            root
            / f"realization-{realization}"
            / "iter-0"
            / "share"
            / "results"
            / "grids"
        )
        _populate(grids_dir)
        grids_dirs.append(grids_dir)
    return grids_dirs


def _names(grids_dir: Path) -> set[str]:
    """Return the set of file names currently present in grids_dir."""
    return {path.name for path in grids_dir.iterdir()}


# --------------------------------------------------------------------------- #
# _count_dates
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),
        ("20180101", 1),
        ("20180701_20180101", 2),
        ("99999999", 0),  # eight digits, but not a valid calendar date
        ("20181301", 0),  # month 13 is invalid
        ("notadate", 0),
    ],
)
def test_count_dates(text, expected):
    assert _count_dates(text) == expected


# --------------------------------------------------------------------------- #
# categorise_filename
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, expected",
    [
        ("simgrid.roff", SaveTypes.GRID),
        ("simgrid--vp--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--vs--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--density--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--ai--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--si--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--vpvs--20180101.roff", SaveTypes.ELASTIC_PROPERTIES),
        ("simgrid--pressure--20180101.roff", SaveTypes.INTERMEDIATE_PROPERTIES),
        (
            "simgrid--effective_pressure--20180101.roff",
            SaveTypes.INTERMEDIATE_PROPERTIES,
        ),
        (
            "simgrid--overburden_pressure--20180101.roff",
            SaveTypes.INTERMEDIATE_PROPERTIES,
        ),
        ("simgrid--density_fluid--20180101.roff", SaveTypes.INTERMEDIATE_PROPERTIES),
        ("simgrid--bulk_modulus_mineral.roff", SaveTypes.INTERMEDIATE_PROPERTIES),
        ("simgrid--vp_dry_rock--20180101.roff", SaveTypes.INTERMEDIATE_PROPERTIES),
        (
            "simgrid--below_bubble_point--20180101.roff",
            SaveTypes.INTERMEDIATE_PROPERTIES,
        ),
        (
            "simgrid--sidiffpercent--20180701_20180101.roff",
            SaveTypes.DIFFERENCE_PROPERTIES,
        ),
        ("simgrid--twtppdiff--20180701_20180101.roff", SaveTypes.DIFFERENCE_PROPERTIES),
        ("simgrid--siratio--20180701_20180101.roff", SaveTypes.DIFFERENCE_PROPERTIES),
    ],
)
def test_categorise_filename(name, expected):
    assert categorise_filename(Path(name)) == expected


def test_categorise_filename_invalid_date_returns_none():
    # An eight-digit run that is not a real date is not treated as an elastic property.
    assert categorise_filename(Path("simgrid--vp--20181301.roff")) is None


# --------------------------------------------------------------------------- #
# make_type_dict
# --------------------------------------------------------------------------- #
def test_make_type_dict_classifies_and_skips(tmp_path):
    grids = tmp_path / "grids"
    _populate(grids)
    # An unrecognised file with a matching suffix/extension must be skipped.
    (grids / "simgrid--vp--20181301.roff").touch()

    type_dict = make_type_dict(grids)
    by_name = {path.name: category for path, category in type_dict.items()}

    assert by_name["simgrid.roff"] == SaveTypes.GRID
    for name in ELASTIC_FILES:
        assert by_name[name] == SaveTypes.ELASTIC_PROPERTIES
    for name in INTERMEDIATE_FILES:
        assert by_name[name] == SaveTypes.INTERMEDIATE_PROPERTIES
    for name in DIFFERENCE_FILES:
        assert by_name[name] == SaveTypes.DIFFERENCE_PROPERTIES
    # Unrelated and unrecognised files are not present.
    assert "notes.txt" not in by_name
    assert "simgrid--vp--20181301.roff" not in by_name


# --------------------------------------------------------------------------- #
# remove_files
# --------------------------------------------------------------------------- #
def test_remove_files_unlinks(tmp_path):
    files = [tmp_path / f"file_{i}.roff" for i in range(3)]
    for file in files:
        file.touch()

    remove_files(files)

    assert all(not file.exists() for file in files)


def test_remove_files_missing_is_not_an_error(tmp_path):
    remove_files([tmp_path / "absent.roff"])  # must not raise


def test_remove_files_raises_when_deletion_fails(tmp_path):
    # Unlinking a directory raises an OSError subclass, which must be reported.
    a_directory = tmp_path / "a_directory"
    a_directory.mkdir()
    with pytest.raises(OSError):
        remove_files([a_directory])


# --------------------------------------------------------------------------- #
# _is_grids_dir / _find_run_grids_dir / crawl_ensemble
# --------------------------------------------------------------------------- #
def test_is_grids_dir(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    grids.mkdir(parents=True)
    assert _is_grids_dir(grids)
    assert not _is_grids_dir(tmp_path)


def test_find_run_grids_dir_accepts_grids_dir(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    grids.mkdir(parents=True)
    assert _find_run_grids_dir(grids) == grids.resolve()


def test_find_run_grids_dir_accepts_run_root(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    grids.mkdir(parents=True)
    # Pointing at the run root (one level above share/) resolves to the grids dir.
    assert _find_run_grids_dir(tmp_path) == grids.resolve()


def test_find_run_grids_dir_rejects_unrelated_location(tmp_path):
    with pytest.raises(ValueError):
        _find_run_grids_dir(tmp_path)


def test_crawl_ensemble_yields_sorted_grids(tmp_path):
    grids_dirs = _make_ensemble(tmp_path, n_real=3)
    result = list(crawl_ensemble(tmp_path))
    assert result == sorted(grids.resolve() for grids in grids_dirs)


def test_crawl_ensemble_rejects_non_ensemble(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    grids.mkdir(parents=True)  # a single run, not an ensemble top
    with pytest.raises(ValueError):
        list(crawl_ensemble(tmp_path))


# --------------------------------------------------------------------------- #
# _resolve_remove_categories
# --------------------------------------------------------------------------- #
def test_resolve_categories_all_includes_grid():
    result = _resolve_remove_categories([SaveTypes.ALL])
    assert result == {
        SaveTypes.INTERMEDIATE_PROPERTIES,
        SaveTypes.ELASTIC_PROPERTIES,
        SaveTypes.DIFFERENCE_PROPERTIES,
        SaveTypes.GRID,
    }


def test_resolve_categories_all_three_includes_grid():
    result = _resolve_remove_categories(
        [
            SaveTypes.INTERMEDIATE_PROPERTIES,
            SaveTypes.ELASTIC_PROPERTIES,
            SaveTypes.DIFFERENCE_PROPERTIES,
        ]
    )
    assert SaveTypes.GRID in result


def test_resolve_categories_subset_excludes_grid():
    result = _resolve_remove_categories([SaveTypes.ELASTIC_PROPERTIES])
    assert result == {SaveTypes.ELASTIC_PROPERTIES}


def test_resolve_categories_explicit_grid_dropped_without_all_three():
    result = _resolve_remove_categories([SaveTypes.ELASTIC_PROPERTIES, SaveTypes.GRID])
    assert result == {SaveTypes.ELASTIC_PROPERTIES}


# --------------------------------------------------------------------------- #
# _normalise_remove_categories
# --------------------------------------------------------------------------- #
def test_normalise_accepts_enum_members():
    result = _normalise_remove_categories(
        [SaveTypes.ELASTIC_PROPERTIES, SaveTypes.GRID]
    )
    assert result == [SaveTypes.ELASTIC_PROPERTIES, SaveTypes.GRID]


def test_normalise_accepts_strings():
    result = _normalise_remove_categories(["elastic", "all"])
    assert result == [SaveTypes.ELASTIC_PROPERTIES, SaveTypes.ALL]


def test_normalise_rejects_unknown_string():
    with pytest.raises(ValueError):
        _normalise_remove_categories(["elasctic"])


# --------------------------------------------------------------------------- #
# cleanup_pem_results - single run
# --------------------------------------------------------------------------- #
def test_cleanup_single_run_removes_only_requested(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    cleanup_pem_results(grids, "simgrid", ".roff", [SaveTypes.INTERMEDIATE_PROPERTIES])

    remaining = _names(grids)
    assert all(name not in remaining for name in INTERMEDIATE_FILES)
    kept = GRID_FILES + ELASTIC_FILES + DIFFERENCE_FILES + UNRELATED_FILES
    assert all(name in remaining for name in kept)


def test_cleanup_accepts_string_categories(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    cleanup_pem_results(grids, "simgrid", ".roff", ["elastic"])

    remaining = _names(grids)
    assert all(name not in remaining for name in ELASTIC_FILES)
    assert all(name in remaining for name in INTERMEDIATE_FILES)


def test_cleanup_rejects_unknown_string_category(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    with pytest.raises(ValueError):
        cleanup_pem_results(grids, "simgrid", ".roff", ["elasctic"])


def test_cleanup_single_run_via_run_root(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    # Point at the run root rather than the grids directory.
    cleanup_pem_results(tmp_path, "simgrid", ".roff", [SaveTypes.ELASTIC_PROPERTIES])

    remaining = _names(grids)
    assert all(name not in remaining for name in ELASTIC_FILES)
    assert all(name in remaining for name in INTERMEDIATE_FILES)


def test_cleanup_all_removes_every_result_but_keeps_unrelated(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    cleanup_pem_results(grids, "simgrid", ".roff", [SaveTypes.ALL])

    remaining = _names(grids)
    assert all(name not in remaining for name in RESULT_FILES)
    assert "notes.txt" in remaining


def test_cleanup_keeps_grid_without_all_three_categories(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    cleanup_pem_results(
        grids,
        "simgrid",
        ".roff",
        [SaveTypes.ELASTIC_PROPERTIES, SaveTypes.DIFFERENCE_PROPERTIES],
    )

    assert "simgrid.roff" in _names(grids)


def test_cleanup_removes_grid_with_all_three_categories(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    cleanup_pem_results(
        grids,
        "simgrid",
        ".roff",
        [
            SaveTypes.INTERMEDIATE_PROPERTIES,
            SaveTypes.ELASTIC_PROPERTIES,
            SaveTypes.DIFFERENCE_PROPERTIES,
        ],
    )

    assert "simgrid.roff" not in _names(grids)


def test_cleanup_single_run_rejects_unrelated_location(tmp_path):
    with pytest.raises(ValueError):
        cleanup_pem_results(
            tmp_path, "simgrid", ".roff", [SaveTypes.ELASTIC_PROPERTIES]
        )


# --------------------------------------------------------------------------- #
# cleanup_pem_results - ensemble
# --------------------------------------------------------------------------- #
def test_cleanup_ensemble_processes_all_realizations(tmp_path):
    grids_dirs = _make_ensemble(tmp_path, n_real=2)

    cleanup_pem_results(
        tmp_path,
        "simgrid",
        ".roff",
        [SaveTypes.ELASTIC_PROPERTIES],
        is_ensemble=True,
    )

    for grids in grids_dirs:
        remaining = _names(grids)
        assert all(name not in remaining for name in ELASTIC_FILES)
        assert all(name in remaining for name in INTERMEDIATE_FILES)


def test_cleanup_ensemble_rejects_single_run_location(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    with pytest.raises(ValueError):
        cleanup_pem_results(
            tmp_path,
            "simgrid",
            ".roff",
            [SaveTypes.ELASTIC_PROPERTIES],
            is_ensemble=True,
        )
