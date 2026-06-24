# ruff: noqa: E501
import subprocess
from math import isclose

import pytest
import xtgeo

from fmu.pem.pem_utilities.rock_physics_adapter import HAS_PROPRIETARY_ROCK_PHYSICS

try:
    # pylint: disable=unused-import
    import ert.shared  # noqa

    HAVE_ERT = True
except ImportError:
    HAVE_ERT = False


@pytest.mark.skipif(
    not HAVE_ERT, reason="ERT is not installed, skipping hook implementation tests."
)
def test_pem_through_ert(testdata, monkeypatch, data_dir):
    monkeypatch.chdir(data_dir)
    pem_output_path = data_dir / "sim2seis/output/pem"
    share_output_path = data_dir / "share/results/grids"

    subprocess.run(
        ["ert", "test_run", "ert/model/run_pem_no_condensate.ert"],
        check=True,
    )

    grid = xtgeo.grid_from_file(share_output_path / "simgrid.roff")
    actnum = xtgeo.gridproperty_from_file(
        pem_output_path / "simgrid.grdecl",
        name="ACTNUM",
        grid=grid,
    ).values

    # Files that are produced are too large for snapshot test.
    # Instead, we make sure sums of values do not change.
    assert actnum.shape == (46, 73, 32)
    assert actnum.sum() == 71475
    assert (grid.actnum_array == actnum).all()

    if HAS_PROPRIETARY_ROCK_PHYSICS:
        truth_values = {
            "simgrid--effective_pressure--20180101.roff": 360008292337.79907,
            "simgrid--pressure--20180101.roff": 2204158466687.0117,
            "simgrid--overburden_pressure--20180101.roff": 2564166759072.876,
            "simgrid--density--20180101.roff": 169814178.1279297,
            "simgrid--vp--20180101.roff": 275354659.3679199,
            "simgrid--vs--20180101.roff": 163355426.4251709,
            "pem--20180101.grdecl_vp": 275354659.318,
            "pem--20180101.grdecl_vs": 163355426.415,
            "pem--20180101.grdecl_dens": 169814178.144,
            "simgrid--sidiff--20180701_20180101.roff": 3304694686.2208695,
            "simgrid--sidiffpercent--20180701_20180101.roff": 60577.2778733396,
            "simgrid--siratio--20180701_20180101.roff": 72080.7727842927,
            "simgrid--twtppdiff--20180701_20180101.roff": -4968.3944744072505,
        }
    else:
        truth_values = {
            "simgrid--effective_pressure--20180101.roff": 360008292348.5,
            "simgrid--pressure--20180101.roff": 2204158466512.0,
            "simgrid--overburden_pressure--20180101.roff": 2564166759012.0,
            "simgrid--density--20180101.roff": 169819421.64660645,
            "simgrid--vp--20180101.roff": 275423306.38964844,
            "simgrid--vs--20180101.roff": 163353050.142,
            "pem--20180101.grdecl_vp": 275423306.45299995,
            "pem--20180101.grdecl_vs": 163353050.142,
            "pem--20180101.grdecl_dens": 169819421.64,
            "simgrid--sidiff--20180701_20180101.roff": 3305689888.80869,
            "simgrid--sidiffpercent--20180701_20180101.roff": 60598.37976185710,
            "simgrid--siratio--20180701_20180101.roff": 72080.9837949872,
            "simgrid--twtppdiff--20180701_20180101.roff": -4957.894073498945,
        }

    estimated_values = {
        "simgrid--effective_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--effective_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "simgrid--pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--pressure--20180101.roff", grid=grid
        ).values.sum(),
        "simgrid--overburden_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--overburden_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "simgrid--density--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--density--20180101.roff", grid=grid
        ).values.sum(),
        "simgrid--vp--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--vp--20180101.roff", grid=grid
        ).values.sum(),
        "simgrid--vs--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--vs--20180101.roff", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vp": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="VP", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vs": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="VS", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_dens": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="DENSITY", grid=grid
        ).values.sum(),
        "simgrid--sidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--sidiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "simgrid--sidiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--sidiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "simgrid--siratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--siratio--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "simgrid--twtppdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "simgrid--twtppdiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
    }

    if truth_values != estimated_values:
        # First go through all cases, report differences without raising an error
        for key, value in truth_values.items():
            if not isclose(value, estimated_values[key], rel_tol=0.0001, abs_tol=0.001):
                print(
                    f"test mismatch for {key}: estimated {estimated_values[key]}, "
                    f"stored value {value}"
                )
        # Now raise an assertion error is at least one case is outside of tolerance limits
        for key, value in truth_values.items():
            assert isclose(value, estimated_values[key], rel_tol=0.0001, abs_tol=0.001)
