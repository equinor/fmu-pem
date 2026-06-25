"""Numerical and snapshot tests for the rock physics models (RPMs).

These tests complement the existing structural tests (which mostly assert types
and shapes) by exercising the *real* ``rock_physics_open`` physics with
deterministic, physically realistic inputs. Three families of behaviour are
verified for every model:

1. Dry rock properties — finite, positive, bounded below the mineral moduli and
   monotonic in porosity / effective pressure.
2. Pressure dependencies — depletion stiffens the dry rock, the effect is capped
   at ``model_max_pressure`` and is suppressed when pressure sensitivity is off.
3. Saturated outputs — ``vp > vs > 0``, fluid substitution behaves correctly and
   derived properties (``ai``, ``si``, ``vpvs``) are consistent.

In addition, ``vp``/``vs``/``density`` for each saturated model are compared with
stored snapshots so that any unintended numerical change is caught. Regenerate
the snapshots with ``PEM_UPDATE_SNAPSHOTS=1``.
"""

from __future__ import annotations

import numpy as np
import pytest

from fmu.pem.pem_functions.pressure_sensitivity import (
    apply_dry_rock_pressure_sensitivity_model,
)
from fmu.pem.pem_functions.regression_models import run_regression_models
from fmu.pem.pem_functions.run_friable_model import run_friable
from fmu.pem.pem_functions.run_patchy_cement_model import run_patchy_cement
from fmu.pem.pem_functions.run_t_matrix_model import run_t_matrix_model
from fmu.pem.pem_utilities.enum_defs import ParameterTypes
from tests.utils.rpm_numerical_harness import (
    QUARTZ_K,
    QUARTZ_MU,
    QUARTZ_RHO,
    assert_snapshot,
    friable_matrix,
    friable_physics_pressure_model,
    make_fluid,
    make_pressure,
    masked,
    patchy_cement_matrix,
    patchy_cement_physics_pressure_model,
    quartz_mineral,
    regression_matrix_k_mu,
    regression_matrix_vp_vs,
    t_matrix_matrix,
)

# ---------------------------------------------------------------------------
# Standard deterministic scenario shared across the tests
# ---------------------------------------------------------------------------

POROSITY = np.array([0.05, 0.12, 0.18, 0.25, 0.32])
N_CELLS = POROSITY.size

# Pressures (Pa). Effective = overburden - formation, depletion of 10 MPa which
# is well within the 40 MPa default model cap.
OVERBURDEN = 45.0e6
FORMATION_INITIAL = 25.0e6
FORMATION_DEPLETED = 15.0e6
EFFECTIVE_INITIAL = OVERBURDEN - FORMATION_INITIAL  # 20 MPa
EFFECTIVE_DEPLETED = OVERBURDEN - FORMATION_DEPLETED  # 30 MPa

# Regression polynomials chosen to stay below the quartz mineral moduli for the
# porosity range above: K(phi) = 30 - 60*phi [GPa], Mu(phi) = 36 - 70*phi [GPa].
REG_K_WEIGHTS = [30.0e9, -60.0e9]
REG_MU_WEIGHTS = [36.0e9, -70.0e9]
# Vp/Vs regression: typical sandstone porosity trends [m/s].
REG_VP_WEIGHTS = [5800.0, -8000.0]
REG_VS_WEIGHTS = [3600.0, -5200.0]


@pytest.fixture
def porosity():
    return masked(POROSITY)


@pytest.fixture
def mineral():
    return quartz_mineral(N_CELLS)


@pytest.fixture
def cement():
    return quartz_mineral(N_CELLS)


@pytest.fixture
def brine():
    return make_fluid([2.5e9] * N_CELLS, [1050.0] * N_CELLS)


@pytest.fixture
def gas():
    return make_fluid([0.05e9] * N_CELLS, [200.0] * N_CELLS)


@pytest.fixture
def pressure_initial():
    return make_pressure(
        [EFFECTIVE_INITIAL] * N_CELLS,
        [FORMATION_INITIAL] * N_CELLS,
        [OVERBURDEN] * N_CELLS,
    )


@pytest.fixture
def pressure_depleted():
    return make_pressure(
        [EFFECTIVE_DEPLETED] * N_CELLS,
        [FORMATION_DEPLETED] * N_CELLS,
        [OVERBURDEN] * N_CELLS,
    )


def _is_strictly_decreasing(values: np.ndarray) -> bool:
    return bool(np.all(np.diff(values) < 0))


# ---------------------------------------------------------------------------
# Dry rock property tests
# ---------------------------------------------------------------------------


def test_friable_dry_rock_physical_bounds(mineral, brine, porosity, pressure_initial):
    """Friable dry rock moduli are finite, bounded and monotone in porosity."""
    _, dry = run_friable(mineral, brine, porosity, pressure_initial, friable_matrix())
    k_dry = dry[0].bulk_modulus.data
    mu_dry = dry[0].shear_modulus.data
    rho_dry = dry[0].density.data

    assert np.all(np.isfinite(k_dry))
    assert np.all(np.isfinite(mu_dry))
    assert np.all(k_dry > 0)
    assert np.all(mu_dry > 0)
    # Dry rock is softer than the solid mineral
    assert np.all(k_dry < QUARTZ_K)
    assert np.all(mu_dry < QUARTZ_MU)
    # Density is the solid framework only
    assert np.allclose(rho_dry, (1.0 - POROSITY) * QUARTZ_RHO)
    # Stiffness falls as porosity rises
    assert _is_strictly_decreasing(k_dry)
    assert _is_strictly_decreasing(mu_dry)


def test_patchy_cement_dry_rock_physical_bounds(
    mineral, cement, brine, porosity, pressure_initial
):
    """Patchy cement dry rock is bounded, monotone and stiffer than friable."""
    _, dry_pc = run_patchy_cement(
        mineral, brine, cement, porosity, pressure_initial, patchy_cement_matrix()
    )
    _, dry_fr = run_friable(
        mineral, brine, porosity, pressure_initial, friable_matrix()
    )
    k_pc = dry_pc[0].bulk_modulus.data
    mu_pc = dry_pc[0].shear_modulus.data

    assert np.all(np.isfinite(k_pc))
    assert np.all(k_pc > 0)
    assert np.all(mu_pc > 0)
    assert np.all(k_pc < QUARTZ_K)
    assert np.all(mu_pc < QUARTZ_MU)
    assert _is_strictly_decreasing(k_pc)
    # A small amount of cement stiffens the rock relative to the friable model
    assert np.all(k_pc > dry_fr[0].bulk_modulus.data)
    assert np.all(mu_pc > dry_fr[0].shear_modulus.data)


def test_regression_dry_rock_matches_polynomial(
    mineral, brine, porosity, pressure_initial
):
    """K/Mu regression dry rock equals the configured porosity polynomial."""
    matrix = regression_matrix_k_mu(k_weights=REG_K_WEIGHTS, mu_weights=REG_MU_WEIGHTS)
    _, dry = run_regression_models(
        mineral, [brine], porosity, [pressure_initial], matrix
    )
    expected_k = REG_K_WEIGHTS[0] + REG_K_WEIGHTS[1] * POROSITY
    expected_mu = REG_MU_WEIGHTS[0] + REG_MU_WEIGHTS[1] * POROSITY

    assert np.allclose(dry[0].bulk_modulus.data, expected_k)
    assert np.allclose(dry[0].shear_modulus.data, expected_mu)
    assert np.allclose(dry[0].density.data, (1.0 - POROSITY) * QUARTZ_RHO)


@pytest.mark.parametrize("model", ["friable", "patchy_cement"])
def test_dry_rock_increases_with_effective_pressure(
    model, mineral, cement, brine, porosity
):
    """Higher effective pressure stiffens the dry rock framework."""
    low = make_pressure([15.0e6] * N_CELLS, [30.0e6] * N_CELLS, [45.0e6] * N_CELLS)
    high = make_pressure([35.0e6] * N_CELLS, [10.0e6] * N_CELLS, [45.0e6] * N_CELLS)

    if model == "friable":
        _, dry_low = run_friable(mineral, brine, porosity, low, friable_matrix())
        _, dry_high = run_friable(mineral, brine, porosity, high, friable_matrix())
    else:
        _, dry_low = run_patchy_cement(
            mineral, brine, cement, porosity, low, patchy_cement_matrix()
        )
        _, dry_high = run_patchy_cement(
            mineral, brine, cement, porosity, high, patchy_cement_matrix()
        )

    assert np.all(dry_high[0].bulk_modulus.data > dry_low[0].bulk_modulus.data)
    assert np.all(dry_high[0].shear_modulus.data > dry_low[0].shear_modulus.data)


# ---------------------------------------------------------------------------
# Pressure dependency tests
# ---------------------------------------------------------------------------


def test_pressure_sensitivity_off_keeps_dry_rock_constant(
    mineral, brine, gas, porosity, pressure_initial, pressure_depleted
):
    """With pressure sensitivity disabled the dry rock is identical over time."""
    _, dry = run_friable(
        mineral,
        [brine, gas],
        porosity,
        [pressure_initial, pressure_depleted],
        friable_matrix(pressure_sensitivity=False),
    )
    assert np.allclose(dry[0].bulk_modulus.data, dry[1].bulk_modulus.data)
    assert np.allclose(dry[0].shear_modulus.data, dry[1].shear_modulus.data)
    assert np.allclose(dry[0].density.data, dry[1].density.data)


@pytest.mark.parametrize("model", ["friable", "patchy_cement"])
def test_pressure_sensitivity_depletion_stiffens_dry_rock(
    model, mineral, cement, brine, porosity, pressure_initial, pressure_depleted
):
    """Depletion (rising effective pressure) increases the dry rock moduli."""
    pressures = [pressure_initial, pressure_depleted]

    if model == "friable":
        _, dry = run_friable(
            mineral,
            [brine, brine],
            porosity,
            pressures,
            friable_matrix(
                pressure_sensitivity=True,
                pressure_sensitivity_model=friable_physics_pressure_model(),
            ),
        )
    else:
        _, dry = run_patchy_cement(
            mineral,
            [brine, brine],
            cement,
            porosity,
            pressures,
            patchy_cement_matrix(
                pressure_sensitivity=True,
                pressure_sensitivity_model=patchy_cement_physics_pressure_model(),
            ),
        )

    assert np.all(dry[1].bulk_modulus.data > dry[0].bulk_modulus.data)
    assert np.all(dry[1].shear_modulus.data > dry[0].shear_modulus.data)


def test_pressure_sensitivity_is_capped(mineral, brine, porosity, pressure_initial):
    """Depletion beyond ``model_max_pressure`` produces the same result as the cap."""
    psm = friable_physics_pressure_model(model_max_pressure=40.0)
    matrix = friable_matrix(pressure_sensitivity=True, pressure_sensitivity_model=psm)
    # Initial effective pressure is 20 MPa; the cap is 40 MPa of depletion.
    # Keep each PressureProperties internally consistent: effective = overburden
    # - formation, with a fixed 5 MPa formation pressure.
    at_cap = make_pressure([60.0e6] * N_CELLS, [5.0e6] * N_CELLS, [65.0e6] * N_CELLS)
    beyond_cap = make_pressure(
        [200.0e6] * N_CELLS, [5.0e6] * N_CELLS, [205.0e6] * N_CELLS
    )

    _, dry_cap = run_friable(
        mineral, [brine, brine], porosity, [pressure_initial, at_cap], matrix
    )
    _, dry_beyond = run_friable(
        mineral, [brine, brine], porosity, [pressure_initial, beyond_cap], matrix
    )
    assert np.allclose(dry_cap[1].bulk_modulus.data, dry_beyond[1].bulk_modulus.data)
    assert np.allclose(dry_cap[1].shear_modulus.data, dry_beyond[1].shear_modulus.data)


def test_physics_pressure_model_depletion_monotonic_real_physics():
    """Direct physics pressure model: depleted moduli exceed in-situ moduli."""
    n = N_CELLS
    k_dry0 = np.array([22e9, 18e9, 15e9, 11e9, 8e9])
    mu_dry0 = k_dry0 * 0.8
    rho = np.full(n, 2400.0)
    p_in = np.full(n, EFFECTIVE_INITIAL)
    p_depl = np.full(n, EFFECTIVE_DEPLETED)

    mineral = quartz_mineral(n)
    in_situ = {
        ParameterTypes.K.value: k_dry0,
        ParameterTypes.MU.value: mu_dry0,
        ParameterTypes.POROSITY.value: POROSITY,
        ParameterTypes.RHO.value: rho,
    }
    result = apply_dry_rock_pressure_sensitivity_model(
        model=friable_physics_pressure_model(),
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ,
        mineral_properties=mineral,
    )
    assert np.all(result[ParameterTypes.K.value] > k_dry0)
    assert np.all(result[ParameterTypes.MU.value] > mu_dry0)
    assert np.all(np.isfinite(result[ParameterTypes.VP.value]))


# ---------------------------------------------------------------------------
# Saturated model tests (physical soundness + snapshots)
# ---------------------------------------------------------------------------


def _run_model(name, fixtures):
    """Run a single saturated model for the standard two-step scenario."""
    mineral, cement, brine, gas, porosity, p0, p1 = fixtures
    fluids = [brine, gas]
    pressures = [p0, p1]
    if name == "friable":
        return run_friable(mineral, fluids, porosity, pressures, friable_matrix())
    if name == "patchy_cement":
        return run_patchy_cement(
            mineral, fluids, cement, porosity, pressures, patchy_cement_matrix()
        )
    if name == "regression_k_mu":
        return run_regression_models(
            mineral,
            fluids,
            porosity,
            pressures,
            regression_matrix_k_mu(k_weights=REG_K_WEIGHTS, mu_weights=REG_MU_WEIGHTS),
        )
    if name == "regression_vp_vs":
        return run_regression_models(
            mineral,
            fluids,
            porosity,
            pressures,
            regression_matrix_vp_vs(
                vp_weights=REG_VP_WEIGHTS, vs_weights=REG_VS_WEIGHTS
            ),
        )
    raise ValueError(f"unknown model {name}")


@pytest.fixture
def standard_fixtures(
    mineral, cement, brine, gas, porosity, pressure_initial, pressure_depleted
):
    return (mineral, cement, brine, gas, porosity, pressure_initial, pressure_depleted)


SATURATED_MODELS = [
    "friable",
    "patchy_cement",
    "regression_k_mu",
    "regression_vp_vs",
]


@pytest.mark.parametrize("name", SATURATED_MODELS)
def test_saturated_outputs_physically_sound(name, standard_fixtures):
    """Saturated velocities are positive, ordered and internally consistent."""
    sat, dry = _run_model(name, standard_fixtures)
    for time_idx, props in enumerate(sat):
        vp = props.vp.data
        vs = props.vs.data
        rho = props.density.data
        assert np.all(np.isfinite(vp))
        assert np.all(np.isfinite(vs))
        assert np.all(vp > 0)
        assert np.all(vs > 0)
        # P-waves are always faster than S-waves
        assert np.all(vp > vs)
        # Saturated rock is heavier than the dry framework
        assert np.all(rho > dry[time_idx].density.data)
        # Derived properties are consistent with the primaries
        assert np.allclose(props.ai.data, vp * rho)
        assert np.allclose(props.si.data, vs * rho)
        assert np.allclose(props.vpvs.data, vp / vs)


@pytest.mark.parametrize("name", SATURATED_MODELS)
def test_fluid_substitution_brine_stiffer_than_gas(name, standard_fixtures):
    """A stiff brine yields a higher saturated bulk modulus than a soft gas.

    The Gassmann fluid-substitution invariant is the saturated bulk modulus, not
    ``vp``: for a stiff dry frame the lower gas density can raise ``vp`` even
    though the rock is less stiff. The bulk modulus, however, always increases
    with the fluid bulk modulus.
    """
    sat, _ = _run_model(name, standard_fixtures)
    # k_sat = rho * (vp^2 - 4/3 * vs^2)
    k_sat_brine = sat[0].density.data * (
        sat[0].vp.data ** 2 - 4.0 / 3.0 * sat[0].vs.data ** 2
    )
    k_sat_gas = sat[1].density.data * (
        sat[1].vp.data ** 2 - 4.0 / 3.0 * sat[1].vs.data ** 2
    )
    assert np.all(k_sat_brine > k_sat_gas)


@pytest.mark.parametrize("name", SATURATED_MODELS)
def test_saturated_model_snapshot(name, standard_fixtures):
    """Saturated outputs match the stored numerical snapshot."""
    sat, _ = _run_model(name, standard_fixtures)
    arrays = {}
    for time_idx, props in enumerate(sat):
        arrays[f"vp_{time_idx}"] = props.vp.data
        arrays[f"vs_{time_idx}"] = props.vs.data
        arrays[f"density_{time_idx}"] = props.density.data
    assert_snapshot(f"saturated_{name}", arrays)


def test_t_matrix_saturated_outputs_physically_sound(
    mineral, brine, gas, porosity, pressure_initial, pressure_depleted, data_dir
):
    """T-Matrix carbonate model produces sound saturated velocities."""
    model_directory = data_dir / "sim2seis" / "model"
    sat, dry = run_t_matrix_model(
        mineral,
        [brine, gas],
        porosity,
        None,
        [pressure_initial, pressure_depleted],
        t_matrix_matrix(),
        model_directory,
    )
    for props in sat:
        vp = props.vp.data
        vs = props.vs.data
        assert np.all(np.isfinite(vp))
        assert np.all(np.isfinite(vs))
        assert np.all(vp > vs)
        assert np.all(vp > 0)
        assert np.all(vs > 0)
    # T-Matrix has no intermediate dry rock step; dry props are NaN by design
    assert np.all(np.isnan(dry[0].bulk_modulus.data))


def test_t_matrix_saturated_snapshot(
    mineral, brine, gas, porosity, pressure_initial, pressure_depleted, data_dir
):
    """T-Matrix saturated outputs match the stored numerical snapshot."""
    model_directory = data_dir / "sim2seis" / "model"
    sat, _ = run_t_matrix_model(
        mineral,
        [brine, gas],
        porosity,
        None,
        [pressure_initial, pressure_depleted],
        t_matrix_matrix(),
        model_directory,
    )
    arrays = {}
    for time_idx, props in enumerate(sat):
        arrays[f"vp_{time_idx}"] = props.vp.data
        arrays[f"vs_{time_idx}"] = props.vs.data
        arrays[f"density_{time_idx}"] = props.density.data
    assert_snapshot("saturated_t_matrix", arrays)


# ---------------------------------------------------------------------------
# Pressure sensitivity model snapshots (real physics, all model families)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "label, model_factory",
    [
        ("friable", friable_physics_pressure_model),
        ("patchy_cement", patchy_cement_physics_pressure_model),
    ],
)
def test_physics_pressure_model_snapshot(label, model_factory):
    """Snapshot the depleted moduli of the physics-based pressure models."""
    n = N_CELLS
    k_dry0 = np.array([22e9, 18e9, 15e9, 11e9, 8e9])
    mu_dry0 = k_dry0 * 0.8
    rho = np.full(n, 2400.0)
    p_in = np.full(n, EFFECTIVE_INITIAL)
    p_depl = np.full(n, EFFECTIVE_DEPLETED)

    mineral = quartz_mineral(n)
    in_situ = {
        ParameterTypes.K.value: k_dry0,
        ParameterTypes.MU.value: mu_dry0,
        ParameterTypes.POROSITY.value: POROSITY,
        ParameterTypes.RHO.value: rho,
    }
    cement_props = None
    if label == "patchy_cement":
        cement_props = quartz_mineral(n)

    result = apply_dry_rock_pressure_sensitivity_model(
        model=model_factory(),
        initial_eff_pressure=p_in,
        depleted_eff_pressure=p_depl,
        in_situ_dict=in_situ,
        mineral_properties=mineral,
        cement_properties=cement_props,
    )
    assert_snapshot(
        f"pressure_physics_{label}",
        {
            "k": result[ParameterTypes.K.value],
            "mu": result[ParameterTypes.MU.value],
            "vp": result[ParameterTypes.VP.value],
            "vs": result[ParameterTypes.VS.value],
        },
    )
