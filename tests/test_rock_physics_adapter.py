import numpy as np
import pytest

import fmu.pem.pem_utilities.rock_physics_adapter as rock_physics_adapter
from tests.utils.rock_physics_adapter_mocking import (
    ensure_rock_physics_not_installed,
    mock_installed_proprietary_rock_physics,
)

INPUT_TEMPERATURE = np.array([150.0])
INPUT_PRESSURE = np.array([2.0e7])
INPUT_RHO = np.array([2650.0])
INPUT_GOR = np.array([100.0])
INPUT_Z_FACTOR = 0.99
INPUT_OIL_SAT = np.array([0.5])
INPUT_GAS_SAT = np.array([0.3])
INPUT_BRINE_SAT = np.array([0.2])
INPUT_OIL_GAS_GRAVITY = np.array([0.8])
INPUT_FREE_GAS_GRAVITY = np.array([0.7])
INPUT_OIL_DENSITY = np.array([800.0])
INPUT_PRES_DEPL = np.array([1.5e7])
INPUT_TEMP_RES = np.array([120.0])

# These tests are for ensuring the rock_physics_adapter correctly chooses
# between the proprietary and open-source implementations, and raises errors and
# warnings when necessary. It does not validate the correctness of the
# underlying rock physics calculations.


@ensure_rock_physics_not_installed
def test_mock_with_proprietary_unavailable():
    assert rock_physics_adapter.HAS_PROPRIETARY_ROCK_PHYSICS is False
    assert not hasattr(rock_physics_adapter, "internal_brine_properties")
    assert not hasattr(rock_physics_adapter, "internal_co2_properties")
    assert not hasattr(rock_physics_adapter, "internal_bp_standing")
    assert not hasattr(rock_physics_adapter, "internal_gas_properties")
    assert not hasattr(rock_physics_adapter, "internal_oil_properties")
    assert not hasattr(rock_physics_adapter, "internal_condensate_properties")
    assert not hasattr(rock_physics_adapter, "internal_saturations_below_bubble_point")


@mock_installed_proprietary_rock_physics
def test_mock_with_proprietary_available():
    assert rock_physics_adapter.HAS_PROPRIETARY_ROCK_PHYSICS is True
    assert hasattr(rock_physics_adapter, "internal_brine_properties")
    assert hasattr(rock_physics_adapter, "internal_co2_properties")
    assert hasattr(rock_physics_adapter, "internal_bp_standing")
    assert hasattr(rock_physics_adapter, "internal_gas_properties")
    assert hasattr(rock_physics_adapter, "internal_oil_properties")
    assert hasattr(rock_physics_adapter, "internal_condensate_properties")
    assert hasattr(rock_physics_adapter, "internal_saturations_below_bubble_point")


@pytest.mark.filterwarnings("error")  # fail on any unhandled/unmatched warnings
@mock_installed_proprietary_rock_physics
def test_co2_properties_uses_internal_path_when_available():
    rock_physics_adapter.co2_properties(
        INPUT_TEMPERATURE,
        INPUT_PRESSURE,
    )
    rock_physics_adapter.open_co2_properties.assert_not_called()
    rock_physics_adapter.internal_co2_properties.assert_called_once()


@pytest.mark.filterwarnings("error")
@ensure_rock_physics_not_installed
def test_co2_properties_uses_open_path_when_proprietary_unavailable():
    assert not hasattr(rock_physics_adapter, "internal_co2_properties")
    rock_physics_adapter.co2_properties(
        INPUT_TEMPERATURE,
        INPUT_PRESSURE,
    )
    rock_physics_adapter.open_co2_properties.assert_called_once()


@pytest.mark.filterwarnings("error")
@mock_installed_proprietary_rock_physics
def test_co2_properties_uses_open_path_when_opting_out_of_proprietary_model():
    rock_physics_adapter.co2_properties(
        INPUT_TEMPERATURE,
        INPUT_PRESSURE,
        use_proprietary_model=False,
    )
    rock_physics_adapter.open_co2_properties.assert_called_once()
    rock_physics_adapter.internal_co2_properties.assert_not_called()


@pytest.mark.filterwarnings("error")
@mock_installed_proprietary_rock_physics
def test_condensate_properties_uses_internal_path_when_available():
    rock_physics_adapter.condensate_properties(
        temperature=INPUT_TEMPERATURE,
        pressure=INPUT_PRESSURE,
        rho0=INPUT_RHO,
        gas_oil_ratio=INPUT_GOR,
        gas_gravity=INPUT_OIL_GAS_GRAVITY,
    )
    rock_physics_adapter.internal_condensate_properties.assert_called_once()


@pytest.mark.filterwarnings("error")
@ensure_rock_physics_not_installed
def test_condensate_properties_raises_error_when_proprietary_unavailable():
    assert not hasattr(rock_physics_adapter, "internal_condensate_properties")
    with pytest.raises(
        RuntimeError,
        match="not possible without the proprietary rock physics package",
    ):
        rock_physics_adapter.condensate_properties(
            temperature=INPUT_TEMPERATURE,
            pressure=INPUT_PRESSURE,
            rho0=INPUT_RHO,
            gas_oil_ratio=INPUT_GOR,
            gas_gravity=INPUT_OIL_GAS_GRAVITY,
        )


@pytest.mark.filterwarnings("error")
@mock_installed_proprietary_rock_physics
def test_saturations_below_bubble_point_uses_internal_path_when_available():
    rock_physics_adapter.saturations_below_bubble_point(
        gas_saturation_init=INPUT_GAS_SAT,
        oil_saturation_init=INPUT_OIL_SAT,
        brine_saturation_init=INPUT_BRINE_SAT,
        gor_init=INPUT_GOR,
        oil_gas_gravity=INPUT_OIL_GAS_GRAVITY,
        free_gas_gravity=INPUT_FREE_GAS_GRAVITY,
        oil_density=INPUT_OIL_DENSITY,
        z_factor=INPUT_Z_FACTOR,
        pres_depl=INPUT_PRES_DEPL,
        temp_res=INPUT_TEMP_RES,
    )
    rock_physics_adapter.internal_saturations_below_bubble_point.assert_called_once()


@pytest.mark.filterwarnings("error")
@ensure_rock_physics_not_installed
def test_saturations_below_bubble_point_warns_and_returns_input_when_unavailable():
    assert not hasattr(rock_physics_adapter, "internal_saturations_below_bubble_point")
    with pytest.warns(UserWarning, match="requires proprietary model"):
        gas_sat, oil_sat, gor, free_gas_gravity = (
            rock_physics_adapter.saturations_below_bubble_point(
                gas_saturation_init=INPUT_GAS_SAT,
                oil_saturation_init=INPUT_OIL_SAT,
                brine_saturation_init=INPUT_BRINE_SAT,
                gor_init=INPUT_GOR,
                oil_gas_gravity=INPUT_OIL_GAS_GRAVITY,
                free_gas_gravity=INPUT_FREE_GAS_GRAVITY,
                oil_density=INPUT_OIL_DENSITY,
                z_factor=INPUT_Z_FACTOR,
                pres_depl=INPUT_PRES_DEPL,
                temp_res=INPUT_TEMP_RES,
            )
        )
    # function should "do nothing" if proprietary model is unavailable, outputs=inputs
    assert np.array_equal(gas_sat, INPUT_GAS_SAT)
    assert np.array_equal(oil_sat, INPUT_OIL_SAT)
    assert np.array_equal(gor, INPUT_GOR)
    assert np.array_equal(free_gas_gravity, INPUT_FREE_GAS_GRAVITY)
