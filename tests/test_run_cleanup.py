"""Tests for the command-line and ERT forward-model entry points of pem_cleanup.

The cleanup logic itself is covered in :mod:`tests.test_cleanup`; these tests
exercise the wiring: the ``parse_cleanup`` argument parser, the ``run_pem_cleanup``
console-script runner, and the ``PemCleanup`` ERT forward-model step.
"""

from pathlib import Path

import pytest

from fmu.pem.pem_utilities.argument_parser import parse_cleanup
from fmu.pem.run_cleanup import run_pem_cleanup

GRID_FILE = "simgrid.roff"
ELASTIC_FILES = ["simgrid--vp--20180101.roff", "simgrid--density--20180101.roff"]
INTERMEDIATE_FILES = ["simgrid--pressure--20180101.roff"]
DIFFERENCE_FILES = ["simgrid--sidiffpercent--20180701_20180101.roff"]
RESULT_FILES = [GRID_FILE] + ELASTIC_FILES + INTERMEDIATE_FILES + DIFFERENCE_FILES


def _populate(grids_dir: Path) -> None:
    grids_dir.mkdir(parents=True, exist_ok=True)
    for name in RESULT_FILES:
        (grids_dir / name).touch()


def _names(grids_dir: Path) -> set[str]:
    return {path.name for path in grids_dir.iterdir()}


# --------------------------------------------------------------------------- #
# parse_cleanup
# --------------------------------------------------------------------------- #
def test_parse_cleanup_single_save_type_is_a_word():
    args = parse_cleanup(["-g", "/tmp/grids", "-s", "elastic"])
    assert args.save_type_list == ["elastic"]


def test_parse_cleanup_multiple_save_types():
    args = parse_cleanup(["-g", "/tmp/grids", "-s", "elastic", "intermediate"])
    assert args.save_type_list == ["elastic", "intermediate"]


def test_parse_cleanup_invalid_save_type_rejected():
    with pytest.raises(SystemExit):
        parse_cleanup(["-g", "/tmp/grids", "-s", "elasctic"])


def test_parse_cleanup_defaults():
    args = parse_cleanup(["-g", "/tmp/grids", "-s", "all"])
    assert args.prefix == "simgrid"
    assert args.extension == ".roff"
    assert args.is_ensemble is False


def test_parse_cleanup_is_ensemble_false_string():
    args = parse_cleanup(["-g", "/tmp/grids", "-s", "all", "-i", "false"])
    assert args.is_ensemble is False


def test_parse_cleanup_is_ensemble_true_string():
    args = parse_cleanup(["-g", "/tmp/grids", "-s", "all", "-i", "true"])
    assert args.is_ensemble is True


# --------------------------------------------------------------------------- #
# run_pem_cleanup (CLI)
# --------------------------------------------------------------------------- #
def test_run_pem_cleanup_single_run(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    run_pem_cleanup(["-g", str(grids), "-s", "elastic"])

    remaining = _names(grids)
    assert all(name not in remaining for name in ELASTIC_FILES)
    assert all(name in remaining for name in INTERMEDIATE_FILES)
    assert GRID_FILE in remaining


def test_run_pem_cleanup_all(tmp_path):
    grids = tmp_path / "share" / "results" / "grids"
    _populate(grids)

    run_pem_cleanup(["-g", str(grids), "-s", "all"])

    assert _names(grids) == set()


def test_run_pem_cleanup_ensemble(tmp_path):
    grids_dirs = []
    for realization in range(2):
        grids = (
            tmp_path
            / f"realization-{realization}"
            / "iter-0"
            / "share"
            / "results"
            / "grids"
        )
        _populate(grids)
        grids_dirs.append(grids)

    run_pem_cleanup(["-g", str(tmp_path), "-s", "elastic", "-i", "true"])

    for grids in grids_dirs:
        remaining = _names(grids)
        assert all(name not in remaining for name in ELASTIC_FILES)
        assert all(name in remaining for name in INTERMEDIATE_FILES)


# --------------------------------------------------------------------------- #
# PemCleanup ERT forward-model step
# --------------------------------------------------------------------------- #
def test_pem_cleanup_forward_model_command():
    from fmu.pem.forward_models import PemCleanup

    step = PemCleanup()
    assert step.name == "PEM_CLEANUP"
    assert step.executable == "pem_cleanup"
    for flag in ("--grid_dir", "--save_type_list", "--prefix"):
        assert flag in step.arglist


def test_pem_cleanup_validate_hooks_pass():
    from fmu.pem.forward_models import PemCleanup

    step = PemCleanup()
    assert step.validate_pre_realization_run({}) == {}
    assert step.validate_pre_experiment({}) is None


def test_pem_cleanup_registered_as_forward_model_step():
    from fmu.pem.forward_models import PemCleanup
    from fmu.pem.hook_implementations.jobs import installable_forward_model_steps

    assert PemCleanup in installable_forward_model_steps().data
