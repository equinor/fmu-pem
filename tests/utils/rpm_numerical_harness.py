"""Shared builders and helpers for numerical rock physics model (RPM) tests.

The wrappers in :mod:`fmu.pem.pem_functions` only access a small subset of the
full :class:`RockMatrixProperties` configuration
(``model.parameters``, ``pressure_sensitivity``, ``pressure_sensitivity_model``,
``minerals`` and ``cement``). These helpers build lightweight configuration
objects with :class:`types.SimpleNamespace` that wrap the *real* pydantic
parameter models, so the genuine ``rock_physics_open`` physics is exercised
rather than being mocked away.

The module also provides a small snapshot facility used for regression testing
of numeric output. Snapshots live next to the test data in
``tests/data/snapshots`` and are tracked in git. To (re)generate them, run the
test suite with the environment variable ``PEM_UPDATE_SNAPSHOTS=1``.
"""

import os
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
)
from fmu.pem.pem_utilities.enum_defs import MineralMixModel
from fmu.pem.pem_utilities.rpm_models import (
    FriableParams,
    KMuRegressionParams,
    MineralProperties,
    OptionalField,
    PatchyCementParams,
    PhysicsModelPressureSensitivity,
    RegressionModels,
    TMatrixParams,
    VpVsRegressionParams,
)

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "data" / "snapshots"
UPDATE_SNAPSHOTS = os.environ.get("PEM_UPDATE_SNAPSHOTS", "").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)

# Reference quartz mineral properties (Pa, Pa, kg/m3)
QUARTZ_K = 36.8e9
QUARTZ_MU = 44.0e9
QUARTZ_RHO = 2650.0


def masked(values: list[float] | np.ndarray) -> np.ma.MaskedArray:
    """Return an unmasked float ``MaskedArray`` from ``values``."""
    arr = np.asarray(values, dtype=float)
    return np.ma.array(arr, mask=np.zeros_like(arr, dtype=bool))


def make_mineral(
    bulk_modulus: np.ndarray | list[float],
    shear_modulus: np.ndarray | list[float],
    density: np.ndarray | list[float],
) -> EffectiveMineralProperties:
    """Build effective mineral properties from per-cell arrays."""
    return EffectiveMineralProperties(
        bulk_modulus=masked(bulk_modulus),
        shear_modulus=masked(shear_modulus),
        density=masked(density),
    )


def quartz_mineral(n: int) -> EffectiveMineralProperties:
    """Uniform quartz mineral over ``n`` cells."""
    return make_mineral([QUARTZ_K] * n, [QUARTZ_MU] * n, [QUARTZ_RHO] * n)


def make_fluid(
    bulk_modulus: np.ndarray | list[float],
    density: np.ndarray | list[float],
) -> EffectiveFluidProperties:
    """Build effective fluid properties from per-cell arrays."""
    return EffectiveFluidProperties(
        bulk_modulus=masked(bulk_modulus), density=masked(density)
    )


def make_pressure(
    effective: np.ndarray | list[float],
    formation: np.ndarray | list[float],
    overburden: np.ndarray | list[float],
) -> PressureProperties:
    """Build pressure properties (all in Pa) from per-cell arrays."""
    return PressureProperties(
        effective_pressure=masked(effective),
        pressure=masked(formation),
        overburden_pressure=masked(overburden),
    )


def _quartz_mineral_property() -> MineralProperties:
    return MineralProperties(
        bulk_modulus=QUARTZ_K, shear_modulus=QUARTZ_MU, density=QUARTZ_RHO
    )


def friable_matrix(
    *,
    pressure_sensitivity: bool = False,
    pressure_sensitivity_model: PhysicsModelPressureSensitivity | None = None,
    **params: float,
) -> SimpleNamespace:
    """Lightweight rock-matrix config for the friable sandstone model."""
    return SimpleNamespace(
        pressure_sensitivity=pressure_sensitivity,
        pressure_sensitivity_model=pressure_sensitivity_model,
        model=SimpleNamespace(parameters=FriableParams(**params)),
        minerals={"quartz": _quartz_mineral_property()},
        cement="quartz",
    )


def patchy_cement_matrix(
    *,
    cement_fraction: float = 0.04,
    pressure_sensitivity: bool = False,
    pressure_sensitivity_model: PhysicsModelPressureSensitivity | None = None,
    **params: float,
) -> SimpleNamespace:
    """Lightweight rock-matrix config for the patchy cement model."""
    return SimpleNamespace(
        pressure_sensitivity=pressure_sensitivity,
        pressure_sensitivity_model=pressure_sensitivity_model,
        model=SimpleNamespace(
            parameters=PatchyCementParams(cement_fraction=cement_fraction, **params)
        ),
        minerals={"quartz": _quartz_mineral_property()},
        cement="quartz",
    )


def regression_matrix_k_mu(
    *,
    k_weights: list[float],
    mu_weights: list[float],
    pressure_sensitivity: bool = False,
    pressure_sensitivity_model: PhysicsModelPressureSensitivity | None = None,
) -> SimpleNamespace:
    """Lightweight rock-matrix config for the K/Mu regression model."""
    params = KMuRegressionParams(
        k_weights=k_weights, mu_weights=mu_weights, rho_model=OptionalField()
    )
    return SimpleNamespace(
        pressure_sensitivity=pressure_sensitivity,
        pressure_sensitivity_model=pressure_sensitivity_model,
        mineral_mix_model=MineralMixModel.VOIGT_REUSS_HILL,
        model=SimpleNamespace(
            parameters=RegressionModels(sandstone=params, shale=params)
        ),
        minerals={"quartz": _quartz_mineral_property()},
        cement="quartz",
    )


def regression_matrix_vp_vs(
    *,
    vp_weights: list[float],
    vs_weights: list[float],
    pressure_sensitivity: bool = False,
    pressure_sensitivity_model: PhysicsModelPressureSensitivity | None = None,
) -> SimpleNamespace:
    """Lightweight rock-matrix config for the Vp/Vs regression model."""
    params = VpVsRegressionParams(
        vp_weights=vp_weights, vs_weights=vs_weights, rho_model=OptionalField()
    )
    return SimpleNamespace(
        pressure_sensitivity=pressure_sensitivity,
        pressure_sensitivity_model=pressure_sensitivity_model,
        mineral_mix_model=MineralMixModel.VOIGT_REUSS_HILL,
        model=SimpleNamespace(
            parameters=RegressionModels(sandstone=params, shale=params)
        ),
        minerals={"quartz": _quartz_mineral_property()},
        cement="quartz",
    )


def t_matrix_matrix(
    *,
    pressure_sensitivity: bool = True,
    t_mat_model_version: str = "PETEC",
    **params: float,
) -> SimpleNamespace:
    """Lightweight rock-matrix config for the T-Matrix model."""
    return SimpleNamespace(
        pressure_sensitivity=pressure_sensitivity,
        model=SimpleNamespace(
            parameters=TMatrixParams(t_mat_model_version=t_mat_model_version, **params)
        ),
    )


def friable_physics_pressure_model(
    *, model_max_pressure: float = 40.0, **params: float
) -> PhysicsModelPressureSensitivity:
    """Physics-based (friable) pressure sensitivity model."""
    return PhysicsModelPressureSensitivity(
        parameters=FriableParams(model_max_pressure=model_max_pressure, **params)
    )


def patchy_cement_physics_pressure_model(
    *, cement_fraction: float = 0.04, model_max_pressure: float = 40.0, **params: float
) -> PhysicsModelPressureSensitivity:
    """Physics-based (patchy cement) pressure sensitivity model."""
    return PhysicsModelPressureSensitivity(
        parameters=PatchyCementParams(
            cement_fraction=cement_fraction,
            model_max_pressure=model_max_pressure,
            **params,
        )
    )


def assert_snapshot(
    name: str,
    arrays: dict[str, np.ndarray],
    *,
    rtol: float = 1e-6,
    atol: float = 0.0,
) -> None:
    """Compare ``arrays`` against a stored ``.npz`` snapshot.

    When ``PEM_UPDATE_SNAPSHOTS`` is set in the environment the snapshot file is
    (re)written instead of compared. When the snapshot does not yet exist an
    assertion error with regeneration instructions is raised.
    """
    snapshot_path = SNAPSHOT_DIR / f"{name}.npz"

    if UPDATE_SNAPSHOTS:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(snapshot_path, **arrays)
        return

    if not snapshot_path.exists():
        raise AssertionError(
            f"Missing snapshot '{snapshot_path}'. Regenerate snapshots by running "
            "the test suite with PEM_UPDATE_SNAPSHOTS=1."
        )

    with np.load(snapshot_path) as reference:
        ref_keys = set(reference.files)
        new_keys = set(arrays)
        assert ref_keys == new_keys, (
            f"Snapshot '{name}' keys changed: stored={sorted(ref_keys)} "
            f"current={sorted(new_keys)}"
        )
        for key, value in arrays.items():
            np.testing.assert_allclose(
                value,
                reference[key],
                rtol=rtol,
                atol=atol,
                err_msg=f"Snapshot mismatch for '{name}' array '{key}'",
            )
