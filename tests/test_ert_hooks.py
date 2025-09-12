# ruff: noqa: E501
import os
import subprocess
from math import isclose

import pytest
import xtgeo

from fmu.pem import INTERNAL_EQUINOR

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
        ["ert", "test_run", "../../ert/model/run_pem_no_condensate.ert"],
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

    if INTERNAL_EQUINOR:
        truth_values = {
            "eclipse--ai--20180101.roff": 632135722078.75,
            "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
            "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
            "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
            "eclipse--dens--20180101.roff": 146827139.21728516,
            "eclipse--vp--20180101.roff": 304320673.8979492,
            "eclipse--vs--20180101.roff": 175066818.78979492,
            "pem--20180101.grdecl_vp": 304320673.71000004,
            "pem--20180101.grdecl_vs": 175066818.85900003,
            "pem--20180101.grdecl_dens": 146827139.22500002,
            "eclipse--si--20180101.roff": 365641672919.5,
            "eclipse--vpvs--20180101.roff": 125729.55125796795,
            "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 53278.50129698821,
            "eclipsegrid_pem--airatio--20180701_20180101.roff": 72007.78503239155,
            "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 172.87380671694098,
            "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
            "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60765.68130324621,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72082.35557192564,
            "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -4378.243091368568,
            "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 53091.133160057994,
            "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71400.73711311817,
            "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60603.220131961425,
        }
    else:
        truth_values = {
            "eclipse--ai--20180101.roff": 633489851422.5,
            "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
            "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
            "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
            "eclipse--dens--20180101.roff": 146814890.05639648,
            "eclipse--vp--20180101.roff": 305017136.54248047,
            "eclipse--vs--20180101.roff": 175075265.64208984,
            "pem--20180101.grdecl_vp": 305017136.491,
            "pem--20180101.grdecl_vs": 175075265.704,
            "pem--20180101.grdecl_dens": 146814889.781,
            "eclipse--si--20180101.roff": 365628513688.75,
            "eclipse--vpvs--20180101.roff": 126039.02598547935,
            "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 53443.10243313891,
            "eclipsegrid_pem--airatio--20180701_20180101.roff": 72009.43102067709,
            "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 378.75060630460166,
            "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
            "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60869.81756451081,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72083.15174680948,
            "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -4357.120079162007,
            "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 53046.806082591145,
            "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71401.31925410032,
            "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60499.499441733584,
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
