from dataclasses import asdict
from unittest.mock import MagicMock

import numpy as np
import pytest

from fmu.pem.pem_functions.run_patchy_cement_model import run_patchy_cement
from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    SaturatedRockProperties,
)


@pytest.fixture
def valid_mineral():
    return EffectiveMineralProperties(
        bulk_modulus=np.ma.array([37e9, 38e9], mask=[False, False]),
        shear_modulus=np.ma.array([44e9, 45e9], mask=[False, False]),
        density=np.ma.array([2650.0, 2660.0], mask=[False, False]),
    )


@pytest.fixture
def valid_fluid():
    return EffectiveFluidProperties(
        bulk_modulus=np.ma.array([2.2e9, 2.3e9], mask=[False, False]),
        density=np.ma.array([1000.0, 1010.0], mask=[False, False]),
    )


@pytest.fixture
def valid_cement():
    return EffectiveMineralProperties(
        bulk_modulus=np.ma.array([10e9, 11e9], mask=[False, False]),
        shear_modulus=np.ma.array([15e9, 16e9], mask=[False, False]),
        density=np.ma.array([2550.0, 2560.0], mask=[False, False]),
    )


@pytest.fixture
def valid_porosity():
    return np.ma.array([0.2, 0.25], mask=[False, False])


@pytest.fixture
def valid_pressure():
    overburden_pressure = np.ma.array([2000, 2100], mask=[False, False])
    formation_pressure = np.ma.array([1500, 1600], mask=[False, False])
    return PressureProperties(
        overburden_pressure=overburden_pressure,
        formation_pressure=formation_pressure,
        effective_pressure=(overburden_pressure - formation_pressure),
    )


@pytest.fixture
def valid_matrix_mock():
    matrix_mock = MagicMock(spec=EffectiveMineralProperties)
    matrix_mock.pressure_sensitivity = False
    matrix_mock.model = MagicMock()
    matrix_mock.model.parameters = MagicMock(
        cement_fraction=0.3,
        critical_porosity=0.4,
        coordination_number_function=MagicMock(fcn="PorBased"),
        coord_num=6,
        shear_reduction=0.6,
    )
    return matrix_mock


@pytest.fixture
def fluid_list():
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
def pressure_list():
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


def test_run_patchy_cement_valid_input(
    valid_mineral,
    valid_fluid,
    valid_cement,
    valid_porosity,
    valid_pressure,
    valid_matrix_mock,
):
    """Test run_patchy_cement with valid inputs."""
    results = run_patchy_cement(
        valid_mineral,
        valid_fluid,
        valid_cement,
        valid_porosity,
        valid_pressure,
        valid_matrix_mock,
    )
    assert isinstance(results, list)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)


def test_run_patchy_cement_invalid_input_type(
    valid_mineral, valid_cement, valid_porosity, valid_pressure, valid_matrix_mock
):
    """Test run_patchy_cement with invalid input types
    to ensure it raises a ValueError."""
    with pytest.raises(ValueError):
        run_patchy_cement(
            valid_mineral,
            "invalid_fluid_type",  # type: ignore
            valid_cement,
            valid_porosity,
            valid_pressure,
            valid_matrix_mock,
        )


def test_run_patchy_cement_invalid_masked_array(
    valid_mineral, valid_cement, valid_porosity, valid_pressure, valid_matrix_mock
):
    """Test run_patchy_cement with non-masked array inputs
    to ensure it raises a ValueError."""
    invalid_fluid = {"bulk_modulus": [2.2e9], "dens": [1000]}  # Not using masked arrays
    with pytest.raises(ValueError):
        run_patchy_cement(
            valid_mineral,
            invalid_fluid,  # type: ignore
            valid_cement,
            valid_porosity,
            valid_pressure,
            valid_matrix_mock,
        )


def test_run_patchy_cement_list_fluid_and_pressure(
    valid_mineral,
    fluid_list,
    valid_cement,
    valid_porosity,
    pressure_list,
    valid_matrix_mock,
):
    """Test run_patchy_cement with list of fluids and pressures."""
    results = run_patchy_cement(
        valid_mineral,
        fluid_list,
        valid_cement,
        valid_porosity,
        pressure_list,
        valid_matrix_mock,
    )
    assert isinstance(results, list)
    assert len(results) == len(fluid_list)
    for result in results:
        assert isinstance(result, SaturatedRockProperties)
        assert all(
            isinstance(asdict(result)[key], np.ndarray)
            for key in ["vp", "vs", "density", "ai", "si", "vpvs"]
        )
