import numpy as np
import numpy.ma as ma
import pytest

from fmu.pem.pem_functions.density import estimate_bulk_density


@pytest.fixture
def porosity():
    return ma.array(0.25)


@pytest.fixture
def fluid_density():
    return [
        ma.array(1000.0),
        ma.array(950.0),
    ]


@pytest.fixture
def mineral_density():
    return ma.array(2650.0)


def test_estimate_bulk_density_no_cement(porosity, fluid_density, mineral_density):
    result = estimate_bulk_density(
        porosity,
        fluid_density,
        mineral_density,
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(r, ma.MaskedArray) for r in result)


def test_estimate_bulk_density_with_patchy_cement(
    porosity, fluid_density, mineral_density
):
    with_cement = estimate_bulk_density(
        porosity,
        fluid_density,
        mineral_density,
        patchy_cement=True,
        cement_fraction=0.05,
        cement_density=2800.0,
    )
    no_cement = estimate_bulk_density(porosity, fluid_density, mineral_density)
    assert len(with_cement) == len(no_cement) == 2
    # Expect at least one value to differ
    assert any(a != b for a, b in zip(with_cement, no_cement))


def test_estimate_bulk_density_missing_cement_params(
    porosity, fluid_density, mineral_density
):
    with pytest.raises(ValueError):
        estimate_bulk_density(
            porosity,
            fluid_density,
            mineral_density,
            patchy_cement=True,
            cement_fraction=0.05,
            # cement_density omitted
        )


def test_estimate_bulk_density_empty_fluid_list(porosity, mineral_density):
    with pytest.raises(ValueError):
        estimate_bulk_density(
            porosity,
            [],
            mineral_density,
        )


def test_estimate_bulk_density_numeric(porosity, fluid_density, mineral_density):
    # Expected without cement:
    # rho_m = mineral_density = 2650
    # Fluid densities: 1000, 950
    # rho_b = (1 - 0.25)*rho_m + 0.25*rho_fl
    expected_no_cement = [
        0.75 * 2650 + 0.25 * 1000,  # 2237.5
        0.75 * 2650 + 0.25 * 950,  # 2225.0
    ]
    result_no_cement = estimate_bulk_density(porosity, fluid_density, mineral_density)
    assert all(
        np.isclose(float(r), e) for r, e in zip(result_no_cement, expected_no_cement)
    )

    # With patchy cement:
    # cement_fraction = 0.05, porosity = 0.25 -> rel = 0.2
    # rho_m = 0.2*2800 + 0.8*2650 = 2680
    # Bulk densities:
    expected_with_cement = [
        0.75 * 2680 + 0.25 * 1000,  # 2260.0
        0.75 * 2680 + 0.25 * 950,  # 2247.5
    ]
    result_with_cement = estimate_bulk_density(
        porosity,
        fluid_density,
        mineral_density,
        patchy_cement=True,
        cement_fraction=0.05,
        cement_density=2800.0,
    )
    assert all(
        np.isclose(float(r), e)
        for r, e in zip(result_with_cement, expected_with_cement)
    )
