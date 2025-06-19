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
    not HAVE_ERT, reason="ERT is not installed, skipping hook implementation tests."
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
        ["ert", "test_run", "run_pem_no_condensate.ert"],
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

    if INTERNAL_EQUINOR:
        truth_values = {
            "eclipse--ai--20180101.roff": 630788411550.25,
            "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
            "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
            "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
            "eclipse--dens--20180101.roff": 172763075.51013184,
            "eclipse--vp--20180101.roff": 259952157.43200684,
            "eclipse--vs--20180101.roff": 143953802.31176758,
            "pem--20180101.grdecl_vp": 259952157.50800002,
            "pem--20180101.grdecl_vs": 143953802.25890002,
            "pem--20180101.grdecl_dens": 172763075.392,
            "eclipse--si--20180101.roff": 349493495827.75,
            "eclipse--vpvs--20180101.roff": 129771.53710186481,
            "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 52972.76091531388,
            "eclipsegrid_pem--airatio--20180701_20180101.roff": 72004.72762221098,
            "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 110.55088904426911,
            "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
            "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60735.55720458542,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72082.35557192564,
            "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -5081.873579170611,
            "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 52847.784338464466,
            "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71398.03012222052,
            "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60630.96068147068,
        }
    else:
        truth_values = {
            "eclipse--ai--20180101.roff": 632325658560.5,
            "eclipse--effective_pressure--20180101.roff": 3600082.9233779907,
            "eclipse--formation_pressure--20180101.roff": 22041584.666870117,
            "eclipse--overburden_pressure--20180101.roff": 25641667.59072876,
            "eclipse--dens--20180101.roff": 172750826.32055664,
            "eclipse--vp--20180101.roff": 260600243.80358887,
            "eclipse--vs--20180101.roff": 143959122.6520996,
            "pem--20180101.grdecl_vp": 260600243.88700002,
            "pem--20180101.grdecl_vs": 143959122.58909997,
            "pem--20180101.grdecl_dens": 172750826.328,
            "eclipse--si--20180101.roff": 349482429012.5,
            "eclipse--vpvs--20180101.roff": 130103.59921741486,
            "eclipsegrid_pem--aidiffpercent--20180701_20180101.roff": 53111.275196157454,
            "eclipsegrid_pem--airatio--20180701_20180101.roff": 72006.11275684834,
            "eclipsegrid_pem--densdiffpercent--20180701_20180101.roff": 267.86967251000584,
            "eclipsegrid_pem--pressurediff--20180701_20180101.roff": -1059073.2168121338,
            "eclipsegrid_pem--sgasdiff--20180701_20180101.roff": 13.83458553818076,
            "eclipsegrid_pem--sidiffpercent--20180701_20180101.roff": 60815.17575664736,
            "eclipsegrid_pem--siratio--20180701_20180101.roff": 72083.15174680948,
            "eclipsegrid_pem--swatdiff--20180701_20180101.roff": 73.71839890442789,
            "eclipsegrid_pem--twtppdiff--20180701_20180101.roff": -5060.120633957486,
            "eclipsegrid_pem--vpdiffpercent--20180701_20180101.roff": 52826.38782819067,
            "eclipsegrid_pem--vpvsratio--20180701_20180101.roff": 71398.59781867266,
            "eclipsegrid_pem--vsdiffpercent--20180701_20180101.roff": 60551.58002056088,
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
