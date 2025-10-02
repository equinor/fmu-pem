from unittest.mock import MagicMock

import numpy as np
import pytest

from fmu.pem.pem_functions.regression_models import run_regression_models
from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PressureProperties,
    SaturatedRockProperties,
)


@pytest.fixture
def setup_mineral_properties():
    return MatrixProperties(
        bulk_modulus=np.ma.array([37e9, 35e9], mask=[False, False]),
        shear_modulus=np.ma.array([44e9, 42e9], mask=[False, False]),
        dens=np.ma.array([2650, 2670], mask=[False, False]),
    )


@pytest.fixture
def setup_fluid_properties():
    return [
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([2.2e9, 2.0e9], mask=[False, False]),
            dens=np.ma.array([1000, 1020], mask=[False, False]),
        )
        for _ in range(2)
    ]


@pytest.fixture
def setup_pressure():
    overburden_pressure = np.ma.array([2000, 2100], mask=[False, False])
    formation_pressure = np.ma.array([1500, 1600], mask=[False, False])
    return [
        PressureProperties(
            overburden_pressure=overburden_pressure,
            formation_pressure=formation_pressure - i * 100,
            effective_pressure=(overburden_pressure - formation_pressure),
        )
        for i in range(2)
    ]


@pytest.fixture
def setup_config(data_dir):
    config_mock = MagicMock()
    config_mock.rock_matrix.model.parameters.sandstone.vp_weights = [3930.0, -2267.0]
    config_mock.rock_matrix.model.parameters.sandstone.vs_weights = [2284.0, -779.0]
    config_mock.rock_matrix.model.parameters.sandstone.rho_model.rho_weights = [
        2602.0,
        -2411.0,
    ]
    config_mock.rock_matrix.model.parameters.sandstone.mode = "vp_vs"
    config_mock.rock_matrix.model.parameters.sandstone.rho_regression = True
    config_mock.rock_matrix.model.parameters.shale = (
        config_mock.rock_matrix.model.parameters.sandstone
    )
    config_mock.paths.rel_path_pem = data_dir / "sim2seis/model"
    return config_mock


def test_run_regression_models_with_masked_arrays(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    setup_config,
    monkeypatch,
    testdata,
):
    # Use restore_dir to change the working directory to data directory
    monkeypatch.chdir(testdata)
    porosity = np.ma.array([0.1, 0.2], mask=[False, False])
    results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        setup_config,
    )
    assert isinstance(results, list), "Expected a list of results"
    assert all(isinstance(item, SaturatedRockProperties) for item in results), (
        "Expected all items in the list to be SaturatedRockProperties objects"
    )


def test_run_regression_models_multiple_time_steps(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    setup_config,
    monkeypatch,
    testdata,
):
    monkeypatch.chdir(testdata)
    porosity = np.ma.array([0.1, 0.2], mask=[False, False])
    results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        setup_config,
        vsh=np.ma.array([0.5, 0.5], mask=[False, False]),
    )
    assert len(results) == len(setup_fluid_properties), (
        "Expected results for each time step"
    )


@pytest.mark.parametrize("input_type", ["mineral", "fluid", "pressure", "porosity"])
def test_run_regression_models_invalid_input_types(
    input_type,
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    setup_config,
    monkeypatch,
    testdata,
):
    monkeypatch.chdir(testdata)
    # Initialize porosity with a default valid value
    porosity = np.ma.array([0.1, 0.2], mask=[False, False])

    if input_type == "mineral":
        setup_mineral_properties.bulk_modulus = [37e9, 35e9]  # Invalid type
    elif input_type == "fluid":
        setup_fluid_properties[0].bulk_modulus = [2.2e9, 2.0e9]  # Invalid type
    elif input_type == "pressure":
        setup_pressure[0].overburden_pressure = 2000  # Invalid type
    elif input_type == "porosity":
        porosity = [0.1, 0.2]  # Invalid type

    with pytest.raises(ValueError):
        run_regression_models(
            setup_mineral_properties,
            setup_fluid_properties,
            porosity,
            setup_pressure,
            setup_config,
        )
