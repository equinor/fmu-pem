# ruff: noqa: E501
import os
import shutil
import subprocess
from pathlib import Path

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
    not HAVE_ERT or not INTERNAL_EQUINOR,
    reason="ERT is not installed or INTERNAL is False, skipping hook implementation tests.",
)
def test_pem_through_ert(testdata, monkeypatch, tmp_path):
    # Copy only specified files to temp directory
    files_to_copy = [
        "export_grid.roff",
        "export_prop.roff",
        "t_mat_params_petec.pkl",
        "run_pem_no_condensate.ert",
        "run_pem_condensate.ert",
        "test_pem_config_condensate.yml",
        "test_pem_config_no_condensate.yml",
        "global_variables.yml",
        "ECLIPSE.EGRID",
        "ECLIPSE.INIT",
        "ECLIPSE.UNRST",
        "simgrid--ntg_pem.roff",
        "carbonate_pressure_model_vp_exp.pkl",
        "carbonate_pressure_model_vs_exp.pkl",
        "vp_exp_model.pkl",
        "vs_exp_model.pkl",
    ]

    for filename in files_to_copy:
        shutil.copy2(Path(testdata) / filename, tmp_path / filename)

    # Create output directory and run test in temp location
    output_path = tmp_path / "output"
    output_path.mkdir(exist_ok=True)
    monkeypatch.chdir(tmp_path)
    subprocess.run(
        ["ert", "test_run", "run_pem_condensate.ert"],
        env={**os.environ, "PEM_MODEL_DIR": str(tmp_path)},
    )

    grid = xtgeo.grid_from_file("output/eclipsegrid_pem.roff")
    actnum = xtgeo.gridproperty_from_file(
        "output/eclipsegrid_pem.grdecl", name="ACTNUM", grid=grid
    ).values

    # Files that are produced are too large for snapshot test.
    # Instead, we make sure sums of values do not change.
    assert actnum.shape == (46, 73, 32)
    assert actnum.sum() == 71475
    assert (grid.actnum_array == actnum).all()

    truth_values = {
        "eclipse--ai--20180101.roff": 630788431819.0,
        "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
        "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
        "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
        "eclipse--dens--20180101.roff": 172765053.8428955,
        "eclipse--vp--20180101.roff": 259949317.82312012,
        "eclipse--vs--20180101.roff": 143952902.5687256,
        "pem--20180101.grdecl_vp": 259949317.90100002,
        "pem--20180101.grdecl_vs": 143952902.5029,
        "pem--20180101.grdecl_dens": 172765053.753,
        "eclipse--si--20180101.roff": 349495431124.0,
        "eclipse--vpvs--20180101.roff": 129770.80256259441,
        "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 52957.09408336784,
        "eclipsegrid_pem--airatio--20180701_20180101.roff": 72004.57095557451,
        "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 91.13803302832936,
        "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
        "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
        "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60725.80493979718,
        "eclipsegrid_pem--siratio--20180701_20180101.roff": 72082.25804978609,
        "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
        "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -5082.683667002098,
        "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 52851.62043007883,
        "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71397.97143810987,
        "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60640.697142426354,
    }

    estimated_values = {
        "eclipse--ai--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--ai--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--effective_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--effective_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--formation_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--formation_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--overburden_pressure--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--overburden_pressure--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--dens--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--dens--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vp--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--vp--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vs--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--vs--20180101.roff", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vp": xtgeo.gridproperty_from_file(
            "output/pem--20180101.grdecl", name="VP", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_vs": xtgeo.gridproperty_from_file(
            "output/pem--20180101.grdecl", name="VS", grid=grid
        ).values.sum(),
        "pem--20180101.grdecl_dens": xtgeo.gridproperty_from_file(
            "output/pem--20180101.grdecl", name="DENS", grid=grid
        ).values.sum(),
        "eclipse--si--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--si--20180101.roff", grid=grid
        ).values.sum(),
        "eclipse--vpvs--20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipse--vpvs--20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--aidiffpercent--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--airatio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--airatio--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--densdiffpercent--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--pressurediff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--pressurediff--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--sgasdiff--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--sidiffpercent--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--siratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--siratio--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--swatdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--swatdiff--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--twtppdiff--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--vpvsratio--20180701_20180101.roff", grid=grid
        ).values.sum(),
        "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": xtgeo.gridproperty_from_file(
            "output/eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff", grid=grid
        ).values.sum(),
    }
    if truth_values != estimated_values:
        for key, value in truth_values.items():
            if value != estimated_values[key]:
                print(
                    f"test mismatch for {key}: estimated {estimated_values[key]}, "
                    f"stored value {value}"
                )
    assert truth_values == estimated_values
