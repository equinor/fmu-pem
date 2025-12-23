from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from fmu.pem.pem_functions.regression_models import run_regression_models
from fmu.pem.pem_utilities import (
    DryRockProperties,
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
    results, dry_results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        rock_matrix,
    )
    assert isinstance(results, list)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)
    assert isinstance(dry_results, list)
    assert all(isinstance(item, DryRockProperties) for item in dry_results)


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
    results, dry_results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        rock_matrix,
        vsh=np.ma.array([0.5, 0.5], mask=[False, False]),
    )
    assert len(results) == len(setup_fluid_properties)
    assert all(isinstance(item, SaturatedRockProperties) for item in results)
    assert all(np.sum(np.isnan(item.vp)) == 0 for item in results)
    assert all(np.sum(np.isnan(item.bulk_modulus)) == 0 for item in dry_results)


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

    results, dry_results = run_regression_models(
        setup_mineral_properties,
        setup_fluid_properties,
        porosity,
        setup_pressure,
        rock_matrix_pressure,
        vsh=np.ma.array([0.5, 0.5], mask=[False, False]),
    )
    results_shear_modulus = [item.vs**2 * item.density for item in results]
    assert all(
        np.all(np.isclose(dry.shear_modulus, sat))
        for dry, sat in zip(dry_results, results_shear_modulus)
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


def test_effective_media_models_parameter_passing_and_numerical_results(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    monkeypatch,
    testdata,
):
    """Test that effective media models are called with correct parameters and produce
    expected results.

    This test verifies:
    1. The numerical correctness of effective media model calculations
    2. That mixing models receive parameters in the correct order
        (k1, mu1, k2, mu2, f/f1)
    3. Both Hashin-Shtrikman and Voigt-Reuss-Hill mixing models work correctly

    This is a regression test for issue #79 where parameters were passed in wrong order.
    """
    monkeypatch.chdir(testdata)

    # Set up test data with known values for reproducible results
    porosity = np.ma.array([0.15, 0.25], mask=[False, False])
    vsh = np.ma.array([0.3, 0.4], mask=[False, False])  # Volume of shale

    # Test both mixing models
    test_cases = [
        (MineralMixModel.HASHIN_SHTRIKMAN, "hashin_shtrikman_average"),
        (MineralMixModel.VOIGT_REUSS_HILL, "voigt_reuss_hill"),
    ]

    for mix_model, function_name in test_cases:
        # Create rock matrix with specific mixing model
        rock_matrix = MagicMock()
        rock_matrix.pressure_sensitivity = False
        rock_matrix.mineral_mix_model = mix_model
        rock_matrix.pressure_sensitivity_model = None
        rock_matrix.model = MagicMock()

        # Set up sandstone and shale parameters with known weights
        sandstone = MagicMock()
        sandstone.vp_weights = [4000.0, -1500.0]  # Vp = 4000 - 1500*porosity
        sandstone.vs_weights = [2400.0, -800.0]  # Vs = 2400 - 800*porosity
        sandstone.rho_model = False
        sandstone.mode = "vp_vs"

        shale = MagicMock()
        shale.vp_weights = [3500.0, -1200.0]  # Different weights for shale
        shale.vs_weights = [2000.0, -600.0]
        shale.rho_model = False
        shale.mode = "vp_vs"

        rock_matrix.model.parameters = MagicMock(sandstone=sandstone, shale=shale)

        # Patch the effective media function to spy on parameter calls
        with patch(
            f"fmu.pem.pem_functions.regression_models.{function_name}"
        ) as mock_func:
            # Set realistic return values (bulk and shear moduli)
            mock_func.return_value = (15e9, 8e9)  # k_dry, mu in Pa

            # Run the regression model
            _ = run_regression_models(
                setup_mineral_properties,
                setup_fluid_properties,
                porosity,
                setup_pressure,
                rock_matrix,
                vsh=vsh,
            )

            # Verify the function was called
            assert mock_func.called, f"{function_name} should have been called"

            # Check that the function was called with keyword arguments in correct order
            call_args = mock_func.call_args
            assert call_args is not None, f"No call arguments found for {function_name}"

            # Verify keyword arguments are used (not positional)
            kwargs = call_args.kwargs
            assert len(kwargs) > 0, "Function should be called with keyword arguments"

            # Check that all required parameters are present
            if function_name == "hashin_shtrikman_average":
                required_params = ["k1", "mu1", "k2", "mu2", "f"]
            else:  # voigt_reuss_hill
                required_params = ["k1", "mu1", "k2", "mu2", "f1"]

            for param in required_params:
                assert param in kwargs, (
                    f"Parameter {param} missing from {function_name} call"
                )

            # Verify parameter values are reasonable (sandstone vs shale properties)
            assert np.all(kwargs["k1"] > 0), (
                "k1 (sandstone bulk modulus) should be positive"
            )
            assert np.all(kwargs["mu1"] > 0), (
                "mu1 (sandstone shear modulus) should be positive"
            )
            assert np.all(kwargs["k2"] > 0), (
                "k2 (shale bulk modulus) should be positive"
            )
            assert np.all(kwargs["mu2"] > 0), (
                "mu2 (shale shear modulus) should be positive"
            )

            # Verify the fraction parameter
            fraction_param = (
                "f" if function_name == "hashin_shtrikman_average" else "f1"
            )
            fraction_values = kwargs[fraction_param]
            assert np.all((fraction_values >= 0) & (fraction_values <= 1)), (
                f"{fraction_param} should be between 0 and 1"
            )

            # For our test case, fraction should be (1 - vsh) = sandstone fraction
            expected_fraction = 1.0 - vsh[~vsh.mask]  # Remove masked values
            np.testing.assert_allclose(fraction_values, expected_fraction, rtol=1e-10)


def test_effective_media_numerical_consistency(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    monkeypatch,
    testdata,
):
    """Test numerical consistency of effective media calculations without mocking.

    This test verifies that the actual calculations produce reasonable and consistent
    results.
    """
    monkeypatch.chdir(testdata)

    # Use simple test data - match the dimensions of setup fixtures
    porosity = np.ma.array([0.2, 0.2], mask=[False, False])
    vsh = np.ma.array([0.5, 0.5], mask=[False, False])  # 50% shale

    # Test with both mixing models using same input data
    results_hs = []
    results_vrh = []

    for mix_model, results_list in [
        (MineralMixModel.HASHIN_SHTRIKMAN, results_hs),
        (MineralMixModel.VOIGT_REUSS_HILL, results_vrh),
    ]:
        rock_matrix = MagicMock()
        rock_matrix.pressure_sensitivity = False
        rock_matrix.mineral_mix_model = mix_model
        rock_matrix.pressure_sensitivity_model = None
        rock_matrix.model = MagicMock()

        # Use identical parameters for both tests
        sandstone = MagicMock()
        sandstone.vp_weights = [4000.0, -1000.0]
        sandstone.vs_weights = [2300.0, -500.0]
        sandstone.rho_model = False
        sandstone.mode = "vp_vs"

        shale = MagicMock()
        shale.vp_weights = [3000.0, -800.0]
        shale.vs_weights = [1800.0, -400.0]
        shale.rho_model = False
        shale.mode = "vp_vs"

        rock_matrix.model.parameters = MagicMock(sandstone=sandstone, shale=shale)

        result, _ = run_regression_models(
            setup_mineral_properties,
            setup_fluid_properties,
            porosity,
            setup_pressure,
            rock_matrix,
            vsh=vsh,
        )

        results_list.append(result[0])  # Store just the first time step result

    # Both should produce valid results (one result per time step)
    assert len(results_hs) == 1
    assert len(results_vrh) == 1

    # Check that results are physically reasonable
    for result_set, model_name in [
        (results_hs, "Hashin-Shtrikman"),
        (results_vrh, "Voigt-Reuss-Hill"),
    ]:
        result = result_set[0]  # First (and only) time step

        # Vp should be positive and reasonable for rock (> 1500 m/s, < 8000 m/s)
        assert np.all(result.vp > 1500), f"{model_name}: Vp too low"
        assert np.all(result.vp < 8000), f"{model_name}: Vp too high"

        # Vs should be positive and less than Vp
        assert np.all(result.vs > 0), f"{model_name}: Vs should be positive"
        assert np.all(result.vs < result.vp), f"{model_name}: Vs should be less than Vp"

        # Density should be reasonable for rock (> 1500 kg/m3, < 3500 kg/m3)
        assert np.all(result.density > 1500), f"{model_name}: Density too low"
        assert np.all(result.density < 3500), f"{model_name}: Density too high"

    # Results should be different between mixing models (they use different averaging
    # schemes) but within reasonable range of each other
    vp_diff = np.abs(results_hs[0].vp - results_vrh[0].vp)
    vs_diff = np.abs(results_hs[0].vs - results_vrh[0].vs)

    # Differences should be non-zero (or at least allow for very small differences)
    # The exact magnitude depends on the contrast between sand and shale properties
    assert np.any(vp_diff > 0.01) or np.any(vs_diff > 0.01), (
        "Mixing models should produce at least slightly different results"
    )

    # Differences should not be huge (less than 20% difference)
    assert np.all(vp_diff < 0.2 * np.minimum(results_hs[0].vp, results_vrh[0].vp)), (
        "Vp difference too large between mixing models"
    )
    assert np.all(vs_diff < 0.2 * np.minimum(results_hs[0].vs, results_vrh[0].vs)), (
        "Vs difference too large between mixing models"
    )


def test_single_lithology_no_mixing_model_calls(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    monkeypatch,
    testdata,
):
    """Test mixing models aren't called for single lithology (no vsh parameter)."""
    monkeypatch.chdir(testdata)

    porosity = np.ma.array([0.15, 0.25], mask=[False, False])
    # No vsh parameter = single lithology

    rock_matrix = MagicMock()
    rock_matrix.pressure_sensitivity = False
    rock_matrix.mineral_mix_model = MineralMixModel.HASHIN_SHTRIKMAN
    rock_matrix.pressure_sensitivity_model = None
    rock_matrix.model = MagicMock()

    sandstone = MagicMock()
    sandstone.vp_weights = [4000.0, -1500.0]
    sandstone.vs_weights = [2400.0, -800.0]
    sandstone.rho_model = False
    sandstone.mode = "vp_vs"

    rock_matrix.model.parameters = MagicMock(sandstone=sandstone)

    # Patch both mixing functions to ensure they're not called
    with (
        patch(
            "fmu.pem.pem_functions.regression_models.hashin_shtrikman_average"
        ) as mock_hs,
        patch("fmu.pem.pem_functions.regression_models.voigt_reuss_hill") as mock_vrh,
    ):
        results, _ = run_regression_models(
            setup_mineral_properties,
            setup_fluid_properties,
            porosity,
            setup_pressure,
            rock_matrix,
            # vsh=None  # Single lithology
        )

        # Verify neither mixing function was called
        assert not mock_hs.called, (
            "Hashin-Shtrikman should not be called for single lithology"
        )
        assert not mock_vrh.called, (
            "Voigt-Reuss-Hill should not be called for single lithology"
        )

        # Should still produce valid results
        assert isinstance(results, list)
        assert all(isinstance(item, SaturatedRockProperties) for item in results)


def test_effective_media_regression_values_bug_79(
    setup_mineral_properties,
    setup_fluid_properties,
    setup_pressure,
    monkeypatch,
    testdata,
):
    """Regression test for bug #79 - verify specific numerical outputs.

    This test ensures that the fix for the parameter ordering bug
    produces the expected numerical results and prevents regression.
    The test uses specific values and checks against expected outputs.
    """
    monkeypatch.chdir(testdata)

    # Use controlled input values for reproducible results
    porosity = np.ma.array([0.2], mask=[False])
    vsh = np.ma.array([0.4], mask=[False])  # 40% shale

    # Test both mixing models with known parameters
    for mix_model, expected_vp_range in [
        (MineralMixModel.HASHIN_SHTRIKMAN, (3700, 3900)),
        (MineralMixModel.VOIGT_REUSS_HILL, (3700, 3900)),
    ]:
        rock_matrix = MagicMock()
        rock_matrix.pressure_sensitivity = False
        rock_matrix.mineral_mix_model = mix_model
        rock_matrix.pressure_sensitivity_model = None
        rock_matrix.model = MagicMock()

        # Use specific regression parameters
        sandstone = MagicMock()
        sandstone.vp_weights = [4200.0, -1200.0]  # Vp = 4200 - 1200*phi
        sandstone.vs_weights = [2400.0, -600.0]  # Vs = 2400 - 600*phi
        sandstone.rho_model = False
        sandstone.mode = "vp_vs"

        shale = MagicMock()
        shale.vp_weights = [3800.0, -1000.0]  # Vp = 3800 - 1000*phi
        shale.vs_weights = [2000.0, -500.0]  # Vs = 2000 - 500*phi
        shale.rho_model = False
        shale.mode = "vp_vs"

        rock_matrix.model.parameters = MagicMock(sandstone=sandstone, shale=shale)

        # Reduce input to single point to match single output
        min_props = EffectiveMineralProperties(
            bulk_modulus=np.ma.array([37e9], mask=[False]),
            shear_modulus=np.ma.array([44e9], mask=[False]),
            density=np.ma.array([2650], mask=[False]),
        )

        fluid_props = [
            EffectiveFluidProperties(
                bulk_modulus=np.ma.array([2.2e9], mask=[False]),
                density=np.ma.array([1000], mask=[False]),
            )
        ]

        pressure_props = [
            PressureProperties(
                overburden_pressure=np.ma.array([2000], mask=[False]),
                formation_pressure=np.ma.array([1500], mask=[False]),
                effective_pressure=np.ma.array([500], mask=[False]),
            )
        ]

        results, _ = run_regression_models(
            min_props, fluid_props, porosity, pressure_props, rock_matrix, vsh=vsh
        )

        assert len(results) == 1, "Should have one result per time step"
        result = results[0]

        # Check that results are in expected ranges
        # (exact values depend on mineral mixing and Gassmann substitution)
        assert expected_vp_range[0] <= result.vp[0] <= expected_vp_range[1], (
            f"{mix_model.value}: Vp {result.vp[0]} outside expected range"
        )

        # Vs should be positive and less than Vp
        assert 0 < result.vs[0] < result.vp[0], (
            f"{mix_model.value}: Invalid Vs/Vp relationship"
        )

        # Density should be reasonable
        assert 2000 < result.density[0] < 2800, (
            f"{mix_model.value}: Density {result.density[0]} outside reasonable range"
        )
