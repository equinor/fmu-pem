from pathlib import Path

import numpy as np
import pytest
import xtgeo

from fmu.pem.pem_utilities import (
    DryRockProperties,
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SaturatedRockProperties,
    save_results,
)

GRID_DIMENSION = (2, 1, 1)
SEIS_DATES = ["20180101"]
GRID_NAME = "simgrid"

PRESSURE_FILES = [
    "simgrid--pressure--20180101.roff",
    "simgrid--effective_pressure--20180101.roff",
    "simgrid--overburden_pressure--20180101.roff",
]
SATURATED_FILES = [
    "simgrid--vp--20180101.roff",
    "simgrid--vs--20180101.roff",
    "simgrid--density--20180101.roff",
]


def _masked(value: float) -> np.ma.MaskedArray:
    return np.ma.array(
        np.full(GRID_DIMENSION, value, dtype=float),
        mask=np.zeros(GRID_DIMENSION, dtype=bool),
    )


@pytest.fixture
def save_results_kwargs(tmp_path: Path) -> dict:
    mandatory_path = Path("share/results/grids")
    pem_output_path = Path("sim2seis/output/pem")
    (tmp_path / mandatory_path).mkdir(parents=True, exist_ok=True)
    (tmp_path / pem_output_path).mkdir(parents=True, exist_ok=True)

    return {
        "config_dir": tmp_path,
        "sim_grid": xtgeo.create_box_grid(dimension=GRID_DIMENSION),
        "grid_name": GRID_NAME,
        "seis_dates": SEIS_DATES,
        "mandatory_path": mandatory_path,
        "pem_output_path": pem_output_path,
        "eff_pres_props": [
            PressureProperties(
                pressure=_masked(1.5e7),
                effective_pressure=_masked(5.0e6),
                overburden_pressure=_masked(2.0e7),
            )
        ],
        "sat_rock_props": [
            SaturatedRockProperties(
                vp=_masked(3000.0),
                vs=_masked(1500.0),
                density=_masked(2200.0),
            )
        ],
        "difference_props": None,
        "difference_date_strs": None,
        "matrix_props": EffectiveMineralProperties(
            bulk_modulus=_masked(37e9),
            shear_modulus=_masked(44e9),
            density=_masked(2650.0),
        ),
        "fluid_props": [
            EffectiveFluidProperties(
                bulk_modulus=_masked(2.2e9),
                density=_masked(1000.0),
            )
        ],
        "bubble_point_grids": [{"below_bubble_point": _masked(0.0)}],
        "dry_rock_props": [
            DryRockProperties(
                bulk_modulus=_masked(20e9),
                shear_modulus=_masked(15e9),
                density=_masked(2200.0),
            )
        ],
        "modified_porosity": None,
    }


@pytest.mark.parametrize(
    "save_to_disk, save_intermediate",
    [
        (True, False),
        (False, True),
        (True, True),
        (False, False),
    ],
)
def test_pressure_output_follows_save_intermediate(
    save_results_kwargs: dict, save_to_disk: bool, save_intermediate: bool
) -> None:
    """Pressure files are controlled by ``save_intermediate`` and saturated rock
    files by ``save_to_disk``, independently of each other."""
    save_results(
        save_to_disk=save_to_disk,
        save_intermediate=save_intermediate,
        **save_results_kwargs,
    )

    output_dir = (
        save_results_kwargs["config_dir"] / save_results_kwargs["pem_output_path"]
    )

    for file_name in PRESSURE_FILES:
        assert (output_dir / file_name).exists() is save_intermediate

    for file_name in SATURATED_FILES:
        assert (output_dir / file_name).exists() is save_to_disk
