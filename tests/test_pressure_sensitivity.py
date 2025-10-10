"""Tests for pressure sensitivity functionality.

Focus:
- RegressionPressureSensitivity (exponential & polynomial) for both VP/VS and K/MU modes
- PhysicsModelPressureSensitivity (friable & patchy cement) via monkeypatched underlying
    RPM functions
- Conversion between velocity <-> moduli paths
- Depletion capping to model_max_pressure
- Error and edge cases (missing keys, invalid inputs, missing cement, shape mismatch)

Each test keeps code brief and readable while checking numeric truths against
explicit formulas replicated from the model implementations.
"""

from __future__ import annotations

import numpy as np
import pytest  # restored import for pytest.raises usage

from fmu.pem.pem_functions.pressure_sensitivity import (
    PressureSensitivityInputError,
    _compute_all_elastic_properties,
    _extract_input_properties,
    _validate_array_shapes,
    apply_dry_rock_pressure_sensitivity_model,
)
from fmu.pem.pem_utilities.enum_defs import (
    ParameterTypes,
    PhysicsPressureModelTypes,
    RegressionPressureModelTypes,
    RegressionPressureParameterTypes,
)
from fmu.pem.pem_utilities.pem_class_definitions import MatrixProperties
from fmu.pem.pem_utilities.rpm_models import (
    ExpParams,
    FriableParams,
    MineralProperties,
    PatchyCementParams,
    PhysicsModelPressureSensitivity,
    PolyParams,
    RegressionPressureSensitivity,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mk_in_situ_dict(
    *,
    vp: np.ndarray | None = None,
    vs: np.ndarray | None = None,
    k: np.ndarray | None = None,
    mu: np.ndarray | None = None,
    rho: np.ndarray,
    poro: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    d: dict[str, np.ndarray] = {ParameterTypes.RHO.value: rho}
    if vp is not None:
        d[ParameterTypes.VP.value] = vp
    if vs is not None:
        d[ParameterTypes.VS.value] = vs
    if k is not None:
        d[ParameterTypes.K.value] = k
    if mu is not None:
        d[ParameterTypes.MU.value] = mu
    if poro is not None:
        d[ParameterTypes.POROSITY.value] = poro
    return d


# ---------------------------------------------------------------------------
# Regression model tests
# ---------------------------------------------------------------------------


def test_regression_exponential_vp_vs_numeric_truth():
    """Exponential regression VP/VS: verify depleted velocities match formula.

    Formula from ExponentialPressureModel:
        v_depl = v0 * (1 - a*exp(-p_depl/b)) / (1 - a*exp(-p_in_situ/b))
    """
    n = 4
    vp0 = np.array([3000.0, 3100.0, 3200.0, 3300.0])
    vs0 = vp0 * 0.55
    rho = np.full(n, 2500.0)
    p_in = np.full(n, 5.0e6)  # Pa
    p_depl = np.full(n, 15.0e6)  # Pa

    a_vp, b_vp = 0.08, 9.0e6
    a_vs, b_vs = 0.10, 8.0e6

    model = RegressionPressureSensitivity(
        model_type=RegressionPressureModelTypes.EXPONENTIAL,
        mode=RegressionPressureParameterTypes.VP_VS,
        parameters={
            ParameterTypes.VP: ExpParams(a_factor=a_vp, b_factor=b_vp),
            ParameterTypes.VS: ExpParams(a_factor=a_vs, b_factor=b_vs),
        },
    )

    in_situ_dict = _mk_in_situ_dict(vp=vp0, vs=vs0, rho=rho)

    res = apply_dry_rock_pressure_sensitivity_model(
        model=model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ_dict,
    )

    # Expected velocities according to formula
    exp_vp = (
        vp0 * (1 - a_vp * np.exp(-p_depl / b_vp)) / (1 - a_vp * np.exp(-p_in / b_vp))
    )
    exp_vs = (
        vs0 * (1 - a_vs * np.exp(-p_depl / b_vs)) / (1 - a_vs * np.exp(-p_in / b_vs))
    )

    assert np.allclose(res[ParameterTypes.VP.value], exp_vp, rtol=1e-10)
    assert np.allclose(res[ParameterTypes.VS.value], exp_vs, rtol=1e-10)
    # Back-calculated moduli must be positive
    assert np.all(res[ParameterTypes.K.value] > 0)
    assert np.all(res[ParameterTypes.MU.value] > 0)


def test_regression_polynomial_k_mu_numeric_truth_and_cap():
    """Polynomial regression K/MU: verify depletion formula & capping.

    PolynomialPressureModel:
        prop_depl = prop_in * P(p_depl_cap) / P(p_in)
    where P(p)=w0 + w1*p + ...; depletion is capped by model_max_pressure.
    """
    n = 3
    k0 = np.array([20e9, 21e9, 22e9])
    mu0 = k0 * 0.6
    rho = np.full(n, 2600.0)
    p_in = np.array([5e6, 6e6, 7e6])
    # Large depletion difference to trigger cap
    p_depl_target = p_in + 50e6  # unrealistically high to force cap
    cap_mpa = 10.0  # MPa
    cap_pa = cap_mpa * 1.0e6

    weights = [1.0, 1.0e-7]  # P(p) = 1 + 1e-7 * p

    model = RegressionPressureSensitivity(
        model_type=RegressionPressureModelTypes.POLYNOMIAL,
        mode=RegressionPressureParameterTypes.K_MU,
        parameters={
            ParameterTypes.K: PolyParams(weights=weights, model_max_pressure=cap_mpa),
            ParameterTypes.MU: PolyParams(weights=weights, model_max_pressure=cap_mpa),
        },
    )

    # in_situ dict with moduli only (mode matches)
    in_situ_dict = _mk_in_situ_dict(k=k0, mu=mu0, rho=rho)

    res = apply_dry_rock_pressure_sensitivity_model(
        model=model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl_target,
        in_situ_dict=in_situ_dict,
    )

    # Effective capped depleted pressure: p_in + min(delta, cap)
    p_depl_cap = p_in + np.minimum(p_depl_target - p_in, cap_pa)

    def poly(p: np.ndarray) -> np.ndarray:  # small helper for readability
        return weights[0] + weights[1] * p

    exp_k = k0 * poly(p_depl_cap) / poly(p_in)
    exp_mu = mu0 * poly(p_depl_cap) / poly(p_in)

    assert np.allclose(res[ParameterTypes.K.value], exp_k, rtol=1e-12)
    assert np.allclose(res[ParameterTypes.MU.value], exp_mu, rtol=1e-12)


def test_regression_vp_vs_from_moduli_conversion():
    """Mode VP/VS but only moduli provided: verify conversion path works."""
    n = 5
    k0 = np.linspace(18e9, 22e9, n)
    mu0 = k0 * 0.5
    rho = np.full(n, 2550.0)
    p_in = np.full(n, 8e6)
    p_depl = np.full(n, 12e6)

    # Simple exponential weights for test (small effect)
    a_vp, b_vp = 0.05, 5e6
    a_vs, b_vs = 0.04, 6e6
    model = RegressionPressureSensitivity(
        model_type=RegressionPressureModelTypes.EXPONENTIAL,
        mode=RegressionPressureParameterTypes.VP_VS,
        parameters={
            ParameterTypes.VP: ExpParams(a_factor=a_vp, b_factor=b_vp),
            ParameterTypes.VS: ExpParams(a_factor=a_vs, b_factor=b_vs),
        },
    )

    in_situ_dict = _mk_in_situ_dict(k=k0, mu=mu0, rho=rho)
    res = apply_dry_rock_pressure_sensitivity_model(
        model=model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ_dict,
    )
    # Just sanity: velocities increase with pressure in this parametrisation
    # (depending on a,b)
    assert res[ParameterTypes.VP.value].shape == (n,)
    assert res[ParameterTypes.VS.value].shape == (n,)
    assert np.all(res[ParameterTypes.VP.value] > 0)
    assert np.all(res[ParameterTypes.VS.value] > 0)


# ---------------------------------------------------------------------------
# Physics model tests (monkeypatched underlying RPM functions for determinism)
# ---------------------------------------------------------------------------


def test_physics_friable_pressure_adjustment_monkeypatch(monkeypatch):
    """Friable physics model: verify scaling k_dry, mu_dry by ratio (k_depl/k_in_situ).

    Monkeypatch rpm_models.friable_model_dry to deterministic linear response:
        k(p) = k_min * (1 + alpha * p)
        mu(p) = mu_min * (1 + beta * p)
    """
    n = 3
    alpha, beta = 1e-8, 2e-8
    p_in = np.array([5e6, 6e6, 7e6])
    p_depl = np.array([10e6, 11e6, 12e6])

    k_dry0 = np.array([20e9, 21e9, 22e9])
    mu_dry0 = k_dry0 * 0.6
    poro = np.array([0.2, 0.22, 0.25])
    rho = np.full(n, 2600.0)

    mineral = MatrixProperties(
        bulk_modulus=np.full(n, 36.8e9),
        shear_modulus=np.full(n, 44e9),
        density=np.full(n, 2650.0),
    )

    # Monkeypatch imported friable_model_dry in the sandstone_models namespace
    def fake_friable_model_dry(
        k_min, mu_min, phi, p_eff, phi_c, coord_num_func, n, shear_red
    ):
        k = k_min * (1.0 + alpha * p_eff)
        mu = mu_min * (1.0 + beta * p_eff)
        return k, mu

    # Patch where function is referenced
    import fmu.pem.pem_utilities.rpm_models as rpm_mod

    monkeypatch.setattr(rpm_mod, "friable_model_dry", fake_friable_model_dry)

    model = PhysicsModelPressureSensitivity(
        model_type=PhysicsPressureModelTypes.FRIABLE,
        parameters=FriableParams(
            critical_porosity=0.45,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=40.0,
        ),
    )

    in_situ_dict = _mk_in_situ_dict(k=k_dry0, mu=mu_dry0, poro=poro, rho=rho)
    res = apply_dry_rock_pressure_sensitivity_model(
        model=model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ_dict,
        mineral_properties=mineral,
    )

    # Expected scaling
    k_in = mineral.bulk_modulus * (1 + alpha * p_in)
    k_depl = mineral.bulk_modulus * (1 + alpha * p_depl)
    mu_in = mineral.shear_modulus * (1 + beta * p_in)
    mu_depl = mineral.shear_modulus * (1 + beta * p_depl)
    exp_k = k_dry0 * (k_depl / k_in)
    exp_mu = mu_dry0 * (mu_depl / mu_in)

    assert np.allclose(res[ParameterTypes.K.value], exp_k, rtol=1e-12)
    assert np.allclose(res[ParameterTypes.MU.value], exp_mu, rtol=1e-12)


def test_physics_patchy_cement_pressure_adjustment_monkeypatch(monkeypatch):
    """Patchy cement physics model deterministic scaling test.

    Monkeypatch rpm_models.patchy_cement_model_dry to:
        k = k_min + frac_cem * k_cem + alpha * p
        mu = mu_min + frac_cem * mu_cem + beta * p
    """
    n = 4
    alpha, beta = 5e-9, 7e-9
    p_in = np.full(n, 6e6)
    p_depl = np.full(n, 9e6)
    frac_cem = 0.04

    k_dry0 = np.linspace(18e9, 21e9, n)
    mu_dry0 = k_dry0 * 0.55
    poro = np.linspace(0.18, 0.24, n)
    rho = np.full(n, 2550.0)

    mineral = MatrixProperties(
        bulk_modulus=np.full(n, 36.8e9),
        shear_modulus=np.full(n, 44e9),
        density=np.full(n, 2650.0),
    )
    cement = MineralProperties(
        bulk_modulus=10e9,
        shear_modulus=15e9,
        density=2550.0,
    )

    def fake_patchy_cement_model_dry(
        k_min,
        mu_min,
        rho_min,
        k_cem,
        mu_cem,
        rho_cem,
        phi,
        p_eff,
        frac_cem,
        phi_c,
        coord_num_func,
        n,
        shear_red,
    ):
        k = k_min + frac_cem * k_cem + alpha * p_eff
        mu = mu_min + frac_cem * mu_cem + beta * p_eff
        rho = rho_min  # unchanged for this test
        return k, mu, rho

    import fmu.pem.pem_utilities.rpm_models as rpm_mod

    monkeypatch.setattr(
        rpm_mod, "patchy_cement_model_dry", fake_patchy_cement_model_dry
    )

    model = PhysicsModelPressureSensitivity(
        model_type=PhysicsPressureModelTypes.PATCHY_CEMENT,
        parameters=PatchyCementParams(
            cement_fraction=frac_cem,
            critical_porosity=0.45,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=40.0,
        ),
    )

    # in-situ dry properties taken at initial pressure (k_dry0, mu_dry0)
    in_situ_dict = _mk_in_situ_dict(k=k_dry0, mu=mu_dry0, poro=poro, rho=rho)
    res = apply_dry_rock_pressure_sensitivity_model(
        model=model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ_dict,
        mineral_properties=mineral,
        cement_properties=cement,
    )

    k_in = mineral.bulk_modulus + frac_cem * cement.bulk_modulus + alpha * p_in
    k_depl = mineral.bulk_modulus + frac_cem * cement.bulk_modulus + alpha * p_depl
    mu_in = mineral.shear_modulus + frac_cem * cement.shear_modulus + beta * p_in
    mu_depl = mineral.shear_modulus + frac_cem * cement.shear_modulus + beta * p_depl
    exp_k = k_dry0 * (k_depl / k_in)
    exp_mu = mu_dry0 * (mu_depl / mu_in)

    assert np.allclose(res[ParameterTypes.K.value], exp_k, rtol=1e-12)
    assert np.allclose(res[ParameterTypes.MU.value], exp_mu, rtol=1e-12)


# ---------------------------------------------------------------------------
# Error & edge case tests
# ---------------------------------------------------------------------------


def test_missing_rho_raises():
    """Missing required 'rho' key should raise PressureSensitivityInputError."""
    model = RegressionPressureSensitivity(
        model_type=RegressionPressureModelTypes.EXPONENTIAL,
        mode=RegressionPressureParameterTypes.VP_VS,
        parameters={
            ParameterTypes.VP: ExpParams(a_factor=0.1, b_factor=1e6),
            ParameterTypes.VS: ExpParams(a_factor=0.1, b_factor=1e6),
        },
    )
    in_situ = {ParameterTypes.VP.value: np.array([3000.0])}
    with pytest.raises(PressureSensitivityInputError):
        apply_dry_rock_pressure_sensitivity_model(
            model=model,
            initial_eff_pressure=np.array([1e6]),
            depleted_eff_pressure=np.array([2e6]),
            in_situ_dict=in_situ,
        )


def test_physics_missing_mineral_properties_raises():
    """Physics model without mineral_properties should raise error."""
    model = PhysicsModelPressureSensitivity(
        model_type=PhysicsPressureModelTypes.FRIABLE,
        parameters=FriableParams(
            critical_porosity=0.45,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=40.0,
        ),
    )
    in_situ = _mk_in_situ_dict(
        k=np.array([20e9]),
        mu=np.array([12e9]),
        poro=np.array([0.2]),
        rho=np.array([2600.0]),
    )
    with pytest.raises(PressureSensitivityInputError):
        apply_dry_rock_pressure_sensitivity_model(
            model=model,
            initial_eff_pressure=np.array([5e6]),
            depleted_eff_pressure=np.array([6e6]),
            in_situ_dict=in_situ,
        )


def test_patchy_cement_missing_cement_properties_raises(monkeypatch):
    """Patchy cement physics model without cement_properties should raise ValueError."""
    # Monkeypatch underlying function to avoid complexity
    import fmu.pem.pem_utilities.rpm_models as rpm_mod

    monkeypatch.setattr(
        rpm_mod,
        "patchy_cement_model_dry",
        lambda *a, **k: (np.array([1.0]), np.array([1.0]), np.array([1.0])),
    )
    model = PhysicsModelPressureSensitivity(
        model_type=PhysicsPressureModelTypes.PATCHY_CEMENT,
        parameters=PatchyCementParams(
            cement_fraction=0.04,
            critical_porosity=0.45,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=40.0,
        ),
    )
    in_situ = _mk_in_situ_dict(
        k=np.array([20e9]),
        mu=np.array([12e9]),
        poro=np.array([0.2]),
        rho=np.array([2600.0]),
    )
    mineral = MatrixProperties(
        bulk_modulus=np.array([36.8e9]),
        shear_modulus=np.array([44e9]),
        density=np.array([2650.0]),
    )
    with pytest.raises(ValueError):
        apply_dry_rock_pressure_sensitivity_model(
            model=model,
            initial_eff_pressure=np.array([5e6]),
            depleted_eff_pressure=np.array([6e6]),
            in_situ_dict=in_situ,
            mineral_properties=mineral,
            cement_properties=None,
        )


def test_invalid_model_type_raises():
    """Passing unsupported model object should raise TypeError."""

    class Dummy:  # minimal dummy model
        pass

    in_situ = _mk_in_situ_dict(
        vp=np.array([3000.0]), vs=np.array([1500.0]), rho=np.array([2500.0])
    )
    with pytest.raises(TypeError):
        apply_dry_rock_pressure_sensitivity_model(
            model=Dummy(),  # type: ignore
            initial_eff_pressure=np.array([5e6]),
            depleted_eff_pressure=np.array([6e6]),
            in_situ_dict=in_situ,
        )


def test_validate_array_shapes_mismatch():
    """Shape mismatch should raise PressureSensitivityInputError."""
    a = np.zeros((5,))
    b = np.zeros((4,))
    with pytest.raises(PressureSensitivityInputError):
        _validate_array_shapes(a, b, names=["a", "b"])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Internal utility path tests
# ---------------------------------------------------------------------------


def test_extract_input_properties_velocity_to_moduli_round_trip():
    """Round-trip: provide velocities for K_MU mode and ensure conversions succeed."""
    n = 6
    vp = np.linspace(3000.0, 3300.0, n)
    vs = vp * 0.55
    rho = np.full(n, 2500.0)
    in_situ = _mk_in_situ_dict(vp=vp, vs=vs, rho=rho)
    k, mu = _extract_input_properties(
        in_situ_dict=in_situ,
        mode=RegressionPressureParameterTypes.K_MU,
        rho=rho,
    )
    # Back compute velocities to ensure consistency
    props = _compute_all_elastic_properties(
        k, mu, rho, RegressionPressureParameterTypes.K_MU
    )
    assert np.allclose(props[ParameterTypes.VP.value], vp, rtol=1e-12)
    assert np.allclose(props[ParameterTypes.VS.value], vs, rtol=1e-12)


def test_extract_input_properties_moduli_to_velocity_round_trip():
    """Provide moduli for VP_VS mode and verify conversions back to moduli."""
    n = 5
    k = np.linspace(18e9, 22e9, n)
    mu = k * 0.6
    rho = np.full(n, 2550.0)
    in_situ = _mk_in_situ_dict(k=k, mu=mu, rho=rho)
    vp, vs = _extract_input_properties(
        in_situ_dict=in_situ,
        mode=RegressionPressureParameterTypes.VP_VS,
        rho=rho,
    )
    # Recompute moduli
    props = _compute_all_elastic_properties(
        vp, vs, rho, RegressionPressureParameterTypes.VP_VS
    )
    assert np.allclose(props[ParameterTypes.K.value], k, rtol=1e-12)
    assert np.allclose(props[ParameterTypes.MU.value], mu, rtol=1e-12)


# ---------------------------------------------------------------------------
# Parameter range validation (Pydantic constraints)
# ---------------------------------------------------------------------------


def test_mineral_properties_out_of_range():
    """MineralProperties should raise validation error for out-of-range values."""
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        MineralProperties(bulk_modulus=5e8, shear_modulus=2e9, density=2000.0)  # type: ignore[arg-type]


def test_patchy_cement_params_cement_fraction_range():
    """PatchyCementParams cement_fraction must be >0 and <=0.1."""
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        PatchyCementParams(
            cement_fraction=0.2,  # invalid
            critical_porosity=0.4,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=30.0,
        )


# ---------------------------------------------------------------------------
# Smoke test combining regression + physics sequentially (conceptual)
# ---------------------------------------------------------------------------


def test_sequential_regression_then_physics_chain(monkeypatch):
    """Apply regression result then feed into physics model to ensure composability."""
    # Regression step (exponential VP/VS) -> get moduli
    vp0 = np.array([3000.0, 3050.0])
    vs0 = vp0 * 0.55
    rho = np.array([2500.0, 2500.0])
    p_in = np.array([5e6, 5e6])
    p_depl = np.array([8e6, 9e6])
    reg_model = RegressionPressureSensitivity(
        model_type=RegressionPressureModelTypes.EXPONENTIAL,
        mode=RegressionPressureParameterTypes.VP_VS,
        parameters={
            ParameterTypes.VP: ExpParams(a_factor=0.05, b_factor=6e6),
            ParameterTypes.VS: ExpParams(a_factor=0.06, b_factor=7e6),
        },
    )
    reg_dict = _mk_in_situ_dict(vp=vp0, vs=vs0, rho=rho)
    reg_res = apply_dry_rock_pressure_sensitivity_model(
        model=reg_model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=reg_dict,
    )

    # Monkeypatch friable model
    import fmu.pem.pem_utilities.rpm_models as rpm_mod

    monkeypatch.setattr(
        rpm_mod,
        "friable_model_dry",
        lambda k_min, mu_min, phi, p_eff, phi_c, coord_num_func, n, shear_red: (
            k_min * (1 + 1e-8 * p_eff),
            mu_min * (1 + 2e-8 * p_eff),
        ),
    )

    phys_model = PhysicsModelPressureSensitivity(
        model_type=PhysicsPressureModelTypes.FRIABLE,
        parameters=FriableParams(
            critical_porosity=0.45,
            coordination_number_function="PorBased",
            coord_num=9.0,
            shear_reduction=0.5,
            model_max_pressure=40.0,
        ),
    )

    # Use regression depleted moduli as starting dry rock
    in_situ_phys = _mk_in_situ_dict(
        k=reg_res[ParameterTypes.K.value],
        mu=reg_res[ParameterTypes.MU.value],
        poro=np.array([0.2, 0.25]),
        rho=reg_res[ParameterTypes.RHO.value],
    )
    phys_res = apply_dry_rock_pressure_sensitivity_model(
        model=phys_model,
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ_phys,
        mineral_properties=MatrixProperties(
            bulk_modulus=np.array([36.8e9, 36.8e9]),
            shear_modulus=np.array([44e9, 44e9]),
            density=np.array([2650.0, 2650.0]),
        ),
    )
    # Basic assertions
    assert phys_res[ParameterTypes.K.value].shape == (2,)
    assert phys_res[ParameterTypes.MU.value].shape == (2,)
    assert np.all(phys_res[ParameterTypes.K.value] > 0)
    assert np.all(phys_res[ParameterTypes.MU.value] > 0)


if __name__ == "__main__":  # pragma: no cover
    # Allow running this file directly for quick debugging
    import pytest

    raise SystemExit(pytest.main([__file__, "-vv"]))
