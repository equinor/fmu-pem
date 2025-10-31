from unittest.mock import MagicMock

import numpy as np
import pytest

from fmu.pem.pem_functions.regression_models import run_regression_models
from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SaturatedRockProperties,
)
from fmu.pem.pem_utilities.enum_defs import MineralMixModel, PhysicsPressureModelTypes


@pytest.fixture
def setup_mineral_properties():
    return EffectiveMineralProperties(
        bulk_modulus=np.ma.array([37e9, 35e9], mask=[False, False]),
        shear_modulus=np.ma.array([44e9, 42e9], mask=[False, False]),
        density=np.ma.array([2650, 2670], mask=[False, False]),
    )


@pytest.fixture
def setup_fluid_properties():
    return [
        EffectiveFluidProperties(
            bulk_modulus=np.ma.array([2.2e9, 2.0e9], mask=[False, False]),
            density=np.ma.array([1000, 1020], mask=[False, False]),
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
def rock_matrix():
    rm = MagicMock()
    rm.pressure_sensitivity = False
    rm.mineral_mix_model = MineralMixModel.VOIGT_REUSS_HILL
    rm.pressure_sensitivity_model = None
    rm.model = MagicMock()
    sandstone = MagicMock()
    sandstone.vp_weights = [3930.0, -2267.0]
    sandstone.vs_weights = [2284.0, -779.0]
    sandstone.rho_model = False
    sandstone.mode = "vp_vs"
    rm.model.parameters = MagicMock(sandstone=sandstone, shale=sandstone)
    return rm


@pytest.fixture
def rock_matrix_pressure(rock_matrix):
    rm = MagicMock()
    rm.pressure_sensitivity = True
    rm.mineral_mix_model = MineralMixModel.VOIGT_REUSS_HILL
    rm.model = rock_matrix.model

    # Pick a valid enum member (first one)
    model_type_any = next(iter(PhysicsPressureModelTypes))
    rm.pressure_sensitivity_model = MagicMock(model_type=model_type_any)

    # Provide cement mineral only if needed
    if model_type_any == PhysicsPressureModelTypes.PATCHY_CEMENT:
        rm.cement = "cement"
        rm.minerals = {"cement": MagicMock()}
    else:
        rm.cement = None
        rm.minerals = {}

    return rm


def test_run_regression_models_with_masked_arrays(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    rock_matrix,
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
        rock_matrix,
    )
    assert isinstance(results, list)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)


def test_run_regression_models_multiple_time_steps(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    rock_matrix,
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
        rock_matrix,
        vsh=np.ma.array([0.5, 0.5], mask=[False, False]),
    )
    assert len(results) == len(setup_fluid_properties)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)


def test_run_regression_models_with_pressure_sensitivity(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    rock_matrix_pressure,
    monkeypatch,
    testdata,
):
    monkeypatch.chdir(testdata)
    porosity = np.ma.array([0.1, 0.2], mask=[False, False])

    # Spy on pressure sensitivity application (return input for simplicity)
    calls = {}

    def _mock_apply(
        model,
        initial_eff_pressure,
        depleted_eff_pressure,
        in_situ_dict,
        mineral_properties,
        cement_properties,
    ):
        calls["called"] = True
        calls["initial_eff_pressure"] = initial_eff_pressure
        calls["depleted_eff_pressure"] = depleted_eff_pressure
        return in_situ_dict

    monkeypatch.setattr(
        "fmu.pem.pem_functions.regression_models.apply_dry_rock_pressure_sensitivity_model",
        _mock_apply,
    )

    results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        rock_matrix_pressure,
        vsh=np.ma.array([0.5, 0.5], mask=[False, False]),
    )
    assert calls.get("called", False)
    assert len(results) == len(setup_fluid_properties)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)


@pytest.mark.parametrize("input_type", ["mineral", "fluid", "porosity"])
def test_run_regression_models_invalid_input_types(
    input_type,
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    rock_matrix,
    monkeypatch,
    testdata,
):
    monkeypatch.chdir(testdata)
    porosity = np.ma.array([0.1, 0.2], mask=[False, False])

    if input_type == "mineral":
        setup_mineral_properties.bulk_modulus = [37e9, 35e9]
    elif input_type == "fluid":
        setup_fluid_properties[0].bulk_modulus = [2.2e9, 2.0e9]
    elif input_type == "porosity":
        porosity = [0.1, 0.2]

    with pytest.raises(ValueError):
        run_regression_models(
            setup_mineral_properties,
            setup_fluid_properties,
            porosity,
            setup_pressure,
            rock_matrix,
        )
