# ruff: noqa: E501
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
    monkeypatch.chdir(data_dir / "sim2seis" / "model")
    pem_output_path = data_dir / "sim2seis/output/pem"
    share_output_path = data_dir / "share/results/grids"

    subprocess.run(
        ["ert", "test_run", "../../ert/model/run_pem_no_condensate.ert"],
        check=True,
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
            "eclipse--effective_pressure--20180101.roff": 360008292337.79907,
            "eclipse--formation_pressure--20180101.roff": 2204158466687.0117,
            "eclipse--overburden_pressure--20180101.roff": 2564166759072.876,
            "eclipse--density--20180101.roff": 169814178.1279297,
            "eclipse--vp--20180101.roff": 275354659.3679199,
            "eclipse--vs--20180101.roff": 163355426.4251709,
            "pem--20180101.grdecl_vp": 275354659.318,
            "pem--20180101.grdecl_vs": 163355426.415,
            "pem--20180101.grdecl_dens": 169814178.144,
            "eclipsegrid_pem--sidiff--20180701_20180101.roff": 3304694686.2208695,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60577.2778733396,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72080.7727842927,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -4968.309265971911,
        }
    else:
        truth_values = {
            "eclipse--effective_pressure--20180101.roff": 360008292337.79907,
            "eclipse--formation_pressure--20180101.roff": 2204158466687.0117,
            "eclipse--overburden_pressure--20180101.roff": 2564166759072.876,
            "eclipse--density--20180101.roff": 169808254.21887207,
            "eclipse--vp--20180101.roff": 275240395.46398926,
            "eclipse--vs--20180101.roff": 163357944.64318848,
            "pem--20180101.grdecl_vp": 275240395.545,
            "pem--20180101.grdecl_vs": 163357944.544,
            "pem--20180101.grdecl_dens": 169808254.146,
            "eclipsegrid_pem--sidiff--20180701_20180101.roff": 3308368685.2021656,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60665.77006227111,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72081.65769129992,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -4955.763309726441,
        }

    estimated_values = {
        "eclipse--effective_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--effective_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--formation_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--formation_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--overburden_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--overburden_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--density--20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipse--density--20180101.roff", grid=grid
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
            pem_output_path / "pem--20180101.grdecl", name="DENSITY", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path
            / "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--sidiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--sidiff--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--siratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--siratio--20180701_20180101.roff",
            grid=grid,
        ).values.sum(),
        "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            share_output_path / "eclipsegrid_pem--twtppdiff--20180701_20180101.roff",
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
