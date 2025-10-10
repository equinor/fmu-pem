from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

from fmu.pem.pem_functions.run_t_matrix_model import (
    run_t_matrix_model,
)
from fmu.pem.pem_utilities import restore_dir
from fmu.pem.pem_utilities.pem_class_definitions import (
    DryRockProperties,
    EffectiveFluidProperties,
    PressureProperties,
    SaturatedRockProperties,
)


@pytest.fixture
def valid_mineral_properties():
    return DryRockProperties(
        bulk_modulus=np.ma.array([37e9, 38e9], mask=[False, False]),
        shear_modulus=np.ma.array([44e9, 45e9], mask=[False, False]),
        density=np.ma.array([2650.0, 2660.0], mask=[False, False]),
    )


@pytest.fixture
def valid_fluid_properties():
    return [
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([2.2e9, 2.3e9], mask=[False, False]),
            density=np.ma.array([1000.0, 1010.0], mask=[False, False]),
        ),
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([1.8e9, 1.9e9], mask=[False, False]),
            density=np.ma.array([950.0, 960.0], mask=[False, False]),
        ),
    ]


@pytest.fixture
def valid_porosity():
    return np.ma.array([0.2, 0.25], mask=[False, False])


@pytest.fixture
def valid_vsh():
    return np.ma.array([0.1, 0.15], mask=[False, False])


@pytest.fixture
def valid_pressure():
    return [
        PressureProperties(
            overburden_pressure=np.ma.array([200, 250], mask=[False, False]),
            effective_pressure=np.ma.array([100, 150], mask=[False, False]),
            formation_pressure=np.ma.array([50, 75], mask=[False, False]),
        ),
        PressureProperties(
            overburden_pressure=np.ma.array([300, 350], mask=[False, False]),
            effective_pressure=np.ma.array([200, 250], mask=[False, False]),
            formation_pressure=np.ma.array([150, 175], mask=[False, False]),
        ),
    ]


@pytest.fixture
def valid_config_mock(data_dir):
    config_mock = MagicMock()
    config_mock.rock_matrix.model.parameters = MagicMock(
        t_mat_model_version="PETEC", angle=30, perm=200, visco=0.001, tau=2, freq=25
    )
    config_mock.paths = MagicMock(rel_path_pem=data_dir / "sim2seis/model")
    return config_mock


@pytest.fixture
def list_fluid_properties():
    return [
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([2.2e9, 2.3e9], mask=[False, False]),
            density=np.ma.array([1000.0, 1010.0], mask=[False, False]),
        ),
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([1.5e9, 1.6e9], mask=[False, False]),
            density=np.ma.array([900.0, 910.0], mask=[False, False]),
        ),
    ]


@pytest.fixture
def list_pressure():
    return [
        PressureProperties(
            overburden_pressure=np.ma.array([200, 250], mask=[False, False]),
            effective_pressure=np.ma.array([100, 150], mask=[False, False]),
            formation_pressure=np.ma.array([50, 75], mask=[False, False]),
        ),
        PressureProperties(
            overburden_pressure=np.ma.array([300, 350], mask=[False, False]),
            effective_pressure=np.ma.array([200, 250], mask=[False, False]),
            formation_pressure=np.ma.array([150, 175], mask=[False, False]),
        ),
    ]


def test_run_t_matrix_and_pressure_models_valid_input(
    valid_mineral_properties,
    valid_fluid_properties,
    valid_porosity,
    valid_vsh,
    valid_pressure,
    valid_config_mock,
):
    """Test run_t_matrix_and_pressure_models with valid inputs."""
    results = run_t_matrix_model(
        valid_mineral_properties,
        valid_fluid_properties,
        valid_porosity,
        valid_vsh,
        valid_pressure,
        valid_config_mock,
        pres_model_vp=Path("carbonate_pressure_model_vp_exp.pkl"),
        pres_model_vs=Path("carbonate_pressure_model_vs_exp.pkl"),
    )
    assert isinstance(results, list)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)


def test_run_t_matrix_and_pressure_models_invalid_input_type(
    valid_mineral_properties,
    valid_porosity,
    valid_vsh,
    valid_pressure,
    valid_config_mock,
):
    """Test run_t_matrix_and_pressure_models with invalid input
    types to ensure it raises a ValueError."""
    with pytest.raises(ValueError):
        run_t_matrix_model(
            valid_mineral_properties,
            "invalid_fluid_type",  # type: ignore
            valid_porosity,
            valid_vsh,
            valid_pressure,
            valid_config_mock,
            pres_model_vp=Path("carbonate_pressure_model_vp_exp.pkl"),
            pres_model_vs=Path("carbonate_pressure_model_vs_exp.pkl"),
        )


def test_run_t_matrix_and_pressure_models_invalid_masked_array(
    valid_mineral_properties,
    valid_porosity,
    valid_vsh,
    valid_pressure,
    valid_config_mock,
):
    """Test run_t_matrix_and_pressure_models with non-masked array
    inputs to ensure it raises a ValueError."""
    invalid_fluid_properties = EffectiveFluidProperties(
        bulk_modulus=np.array([2.2e9]),  # type: ignore
        density=np.array([1000]),  # type: ignore
    )
    with pytest.raises(ValueError), restore_dir(valid_config_mock.paths.rel_path_pem):
        run_t_matrix_model(
            valid_mineral_properties,
            invalid_fluid_properties,
            valid_porosity,
            valid_vsh,
            valid_pressure,
            valid_config_mock,
            pres_model_vp=Path("carbonate_pressure_model_vp_exp.pkl"),
            pres_model_vs=Path("carbonate_pressure_model_vs_exp.pkl"),
        )


def test_run_t_matrix_and_pressure_models_with_list_inputs(
    valid_mineral_properties,
    list_fluid_properties,
    valid_porosity,
    valid_vsh,
    list_pressure,
    valid_config_mock,
):
    """Test run_t_matrix_and_pressure_models with lists of
    EffectiveFluidProperties and PressureProperties."""
    results = run_t_matrix_model(
        valid_mineral_properties,
        list_fluid_properties,
        valid_porosity,
        valid_vsh,
        list_pressure,
        valid_config_mock,
        pres_model_vp=Path("carbonate_pressure_model_vp_exp.pkl"),
        pres_model_vs=Path("carbonate_pressure_model_vs_exp.pkl"),
    )
    assert isinstance(results, list)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)
