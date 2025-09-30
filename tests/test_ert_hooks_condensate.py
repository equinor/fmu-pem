# ruff: noqa: E501
import os
import subprocess
from math import isclose

import pytest
import xtgeo

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
    monkeypatch.chdir(data_dir / "rms/model")
    start_path = data_dir / "rms/model"
    pem_output_path = data_dir / "sim2seis/output/pem"
    share_output_path = data_dir / "share/results/grids"
    subprocess.run(
        ["ert", "test_run", "../../ert/model/run_pem_condensate.ert"],
        env={**os.environ, "PEM_MODEL_DIR": str(start_path)},
    )

    grid = xtgeo.grid_from_file(share_output_path / "eclipsegrid_pem.roff")
    actnum = xtgeo.gridproperty_from_file(
        pem_output_path / "eclipsegrid_pem.grdecl",
        name="ACTNUM",
        grid=grid,
    ).values

    # Files that are produced are too large for snapshot test.
    # Instead, we make sure sums of values do not change.
    assert actnum.shape == (46, 73, 32)
    assert actnum.sum() == 71475
    assert (grid.actnum_array == actnum).all()

    truth_values = {
        "eclipse--ai--20180101.roff": 632136725693.75,
        "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
        "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
        "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
        "eclipse--dens--20180101.roff": 146829117.55212402,
        "eclipse--vp--20180101.roff": 304317009.2866211,
        "eclipse--vs--20180101.roff": 175065460.1656494,
        "pem--20180101.grdecl_vp": 304317009.127,
        "pem--20180101.grdecl_vs": 175065460.22300002,
        "pem--20180101.grdecl_dens": 146829117.55400002,
        "eclipse--si--20180101.roff": 365643950556.5,
        "eclipse--vpvs--20180101.roff": 125728.85543096066,
        "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 53260.39453013704,
        "eclipsegrid_pem--airatio--20180701_20180101.roff": 72007.60396528244,
        "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 147.80313034862314,
        "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
        "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
        "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60753.09078057007,
        "eclipsegrid_pem--siratio--20180701_20180101.roff": 72082.25804978609,
        "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
        "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -4379.44374777568,
        "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 53098.192230394634,
        "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71400.68238121271,
        "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60615.78208509988,
    }

    estimated_values = {
        "eclipse--ai--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--ai--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--effective_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--effective_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--formation_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--formation_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--overburden_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--overburden_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--dens--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--dens--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vp--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--vp--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vs--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--vs--20180101.roff", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vp": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="VP", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vs": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="VS", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_dens": xtgeo.gridproperty_from_file(
            pem_output_path / "pem--20180101.grdecl", name="DENS", grid=grid
        ).values.sum(),
        "eclipse--si--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--si--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vpvs--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--vpvs--20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--airatio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--airatio--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--pressurediff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--pressurediff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--sgasdiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--siratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--siratio--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--swatdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--swatdiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--twtppdiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--vpvsratio--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
    }
    if truth_values != estimated_values:
        # First go through all cases, report differences without raising an error
        for key, value in truth_values.items():
            if not isclose(
                value, estimated_values[key], rel_tol=0.00001, abs_tol=0.001
            ):
                print(
                    f"test mismatch for {key}: estimated {estimated_values[key]}, "
                    f"stored value {value}"
                )
        # Now raise an assertion error is at least one case is outside of tolerance limits
        for key, value in truth_values.items():
            assert isclose(value, estimated_values[key], rel_tol=0.00001, abs_tol=0.001)
