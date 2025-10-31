# python
# File: src/fmu/pem/pem_functions/pressure_sensitivity.py
from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

import numpy as np

from fmu.pem.pem_utilities.enum_defs import (
    ParameterTypes,
    PhysicsPressureModelTypes,
    RegressionPressureParameterTypes,
)
from fmu.pem.pem_utilities.pem_class_definitions import EffectiveMineralProperties
from fmu.pem.pem_utilities.rpm_models import (
    MineralProperties,
    PhysicsModelPressureSensitivity,
    RegressionPressureSensitivity,
)

_FEATURE_NAME_MAP = {
    ParameterTypes.VP.value: "VP",
    ParameterTypes.VS.value: "VSX",  # Model expects VSX for Vs
    ParameterTypes.K.value: "K",
    ParameterTypes.MU.value: "MU",
}


@runtime_checkable
class RegressionPressureModel(Protocol):
    """Protocol for regression-based pressure sensitivity models."""

    mode: RegressionPressureParameterTypes

    def predict_elastic_properties(
        self,
        prop1: np.ndarray,
        prop2: np.ndarray,
        in_situ_press: np.ndarray,
        depl_press: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]: ...


@runtime_checkable
class PhysicsPressureModel(Protocol):
    """Protocol for physics-based pressure sensitivity models."""

    model_type: PhysicsPressureModelTypes

    def predict_elastic_properties(
        self,
        k_dry: np.ndarray,
        mu_dry: np.ndarray,
        poro: np.ndarray,
        min_prop: MineralProperties,
        in_situ_press: np.ndarray,
        depl_press: np.ndarray,
        cem_prop: MineralProperties | None = None,
    ) -> tuple[np.ndarray, np.ndarray]: ...


def _validate_array_shapes(
    *arrays: np.ndarray,
    names: list[str] | None = None,
) -> None:
    """
    Validate that all arrays have the same first dimension.

    Parameters
    ----------
    *arrays : np.ndarray
        Arrays to validate.
    names : list[str] | None
        Names for error messages. If None, uses generic labels.

    Raises
    ------
    PressureSensitivityInputError
        If array shapes are inconsistent.
    """
    if not arrays:
        return

    expected_shape = arrays[0].shape[0]
    names = names or [f"array_{i}" for i in range(len(arrays))]

    for arr, name in zip(arrays, names):
        if arr.shape[0] != expected_shape:
            raise PressureSensitivityInputError(
                f"Shape mismatch for '{name}': expected {expected_shape}, "
                f"got {arr.shape[0]}"
            )


def _validate_required_keys(
    provided: dict[str, np.ndarray],
    required: set[str],
    dict_name: str,
) -> None:
    """
    Validate that all required keys exist in provided dictionary.

    Parameters
    ----------
    provided : dict[str, np.ndarray]
        Dictionary to validate.
    required : set[str]
        Required keys.
    dict_name : str
        Name for error messages.

    Raises
    ------
    PressureSensitivityInputError
        If any required key is missing.
    """
    missing = required - set(provided.keys())
    if missing:
        raise PressureSensitivityInputError(
            f"Missing keys {sorted(missing)} in {dict_name}; "
            f"required={sorted(required)}"
        )


def _extract_input_properties(
    in_situ_dict: dict[str, np.ndarray],
    mode: RegressionPressureParameterTypes,
    rho: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract or compute the two elastic properties needed for the model.

    Parameters
    ----------
    in_situ_dict : dict[str, np.ndarray]
        Dictionary with in-situ properties. Must contain either (vp, vs) or (k, mu).
    mode : RegressionPressureParameterTypes
        Model mode determining which properties are needed.
    rho : np.ndarray
        Density array for conversions.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (prop1, prop2) matching the model mode:
        - VP_VS mode: (vp, vs)
        - K_MU mode: (k, mu)

    Raises
    ------
    PressureSensitivityInputError
        If required properties cannot be obtained.
    """
    from rock_physics_open.equinor_utilities.std_functions import moduli, velocity

    vp_key = ParameterTypes.VP.value
    vs_key = ParameterTypes.VS.value
    k_key = ParameterTypes.K.value
    mu_key = ParameterTypes.MU.value

    has_velocities = vp_key in in_situ_dict and vs_key in in_situ_dict
    has_moduli = k_key in in_situ_dict and mu_key in in_situ_dict

    if mode == RegressionPressureParameterTypes.VP_VS:
        if has_velocities:
            return in_situ_dict[vp_key], in_situ_dict[vs_key]
        if has_moduli:
            # Convert from moduli to velocities
            vp, vs = velocity(in_situ_dict[k_key], in_situ_dict[mu_key], rho)[0:2]
            return vp, vs
        raise PressureSensitivityInputError(
            f"For VP_VS mode, need either ({vp_key}, {vs_key}) or ({k_key}, {mu_key})"
        )
    # K_MU mode
    if has_moduli:
        return in_situ_dict[k_key], in_situ_dict[mu_key]
    if has_velocities:
        # Convert from velocities to moduli
        k, mu = moduli(in_situ_dict[vp_key], in_situ_dict[vs_key], rho)
        return k, mu
    raise PressureSensitivityInputError(
        f"For K_MU mode, need either ({k_key}, {mu_key}) or ({vp_key}, {vs_key})"
    )


def _compute_all_elastic_properties(
    prop1: np.ndarray,
    prop2: np.ndarray,
    rho: np.ndarray,
    mode: RegressionPressureParameterTypes,
) -> dict[str, np.ndarray]:
    """
    Compute all four elastic properties from the two predicted ones.

    Parameters
    ----------
    prop1 : np.ndarray
        First predicted property (vp or k).
    prop2 : np.ndarray
        Second predicted property (vs or mu).
    rho : np.ndarray
        Density array.
    mode : RegressionPressureParameterTypes
        Model mode indicating which properties were predicted.

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing vp, vs, k, mu, and rho.
    """
    from rock_physics_open.equinor_utilities.std_functions import moduli, velocity

    if mode == RegressionPressureParameterTypes.VP_VS:
        vp, vs = prop1, prop2
        k, mu = moduli(vp, vs, rho)
    else:  # K_MU mode
        k, mu = prop1, prop2
        vp, vs = velocity(k, mu, rho)[0:2]

    return {
        ParameterTypes.VP.value: vp,
        ParameterTypes.VS.value: vs,
        ParameterTypes.K.value: k,
        ParameterTypes.MU.value: mu,
        ParameterTypes.RHO.value: rho,
    }


class PressureSensitivityInputError(ValueError):
    """Raised when required pressure sensitivity inputs are missing or inconsistent."""


def _validate_required(
    provided: dict[str, np.ndarray],
    required: Iterable[str],
    dict_name: str,
) -> None:
    """
    Validate that all required keys exist in a provided dictionary.

    Parameters
    ----------
    provided : dict[str, np.ndarray]
        Dictionary containing arrays for rock properties.
    required : Iterable[str]
        Keys that must be present.
    dict_name : str
        Name used in error messages.

    Raises
    ------
    PressureSensitivityInputError
        If any required key is missing.
    """
    missing = [k for k in required if k not in provided]
    if missing:
        raise PressureSensitivityInputError(
            f"Missing keys {missing} in {dict_name}; required={list(required)}"
        )


def _as_enum_mode(
    mode: RegressionPressureParameterTypes | str,
) -> RegressionPressureParameterTypes:
    """
    Normalize mode argument to RegressionPressureParameterTypes enum.

    Parameters
    ----------
    mode : RegressionPressureParameterTypes | str
        Mode specification ('vp_vs' or 'k_mu').

    Returns
    -------
    RegressionPressureParameterTypes
        Normalized enum value.

    Raises
    ------
    ValueError
        If unsupported mode supplied.
    """
    if isinstance(mode, RegressionPressureParameterTypes):
        return mode
    try:
        return RegressionPressureParameterTypes(mode)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported mode '{mode}'. Expected 'vp_vs' or 'k_mu'."
        ) from exc


def apply_dry_rock_pressure_sensitivity_model(
    model: RegressionPressureSensitivity | PhysicsModelPressureSensitivity,
    initial_eff_pressure: np.ndarray,
    depleted_eff_pressure: np.ndarray,
    in_situ_dict: dict[str, np.ndarray],
    mineral_properties: MineralProperties | EffectiveMineralProperties | None = None,
    cement_properties: MineralProperties | EffectiveMineralProperties | None = None,
) -> dict[str, np.ndarray]:
    """
    Apply pressure sensitivity model to estimate depleted elastic properties.

    Handles both regression-based and physics-based pressure sensitivity models
    with their different input requirements.

    Parameters
    ----------
    model : RegressionPressureSensitivity | PhysicsModelPressureSensitivity
        Pressure sensitivity model instance.
    initial_eff_pressure : np.ndarray
        In-situ effective (pore) pressure [Pa], shape (n,).
    depleted_eff_pressure : np.ndarray
        Depleted effective pressure [Pa], shape (n,).
    in_situ_dict : dict[str, np.ndarray]
        Dictionary with in-situ properties. Must contain 'rho'.
        For regression models: requires ('vp', 'vs') or ('k', 'mu').
        For physics models: requires ('k', 'mu', 'porosity').
    mineral_properties : MineralProperties | None
        Required for physics-based models. Mineral elastic properties.
    cement_properties : MineralProperties | None
        Required for patchy cement physics model.

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary with 'vp', 'vs', 'k', 'mu', 'rho'.

    Raises
    ------
    PressureSensitivityInputError
        If required inputs are missing or inconsistent.
    """
    # Validate common inputs
    _validate_required_keys(in_situ_dict, {ParameterTypes.RHO.value}, "in_situ_dict")
    rho = in_situ_dict[ParameterTypes.RHO.value]

    # Route to appropriate handler based on model type
    if isinstance(model, RegressionPressureSensitivity):
        return _apply_regression_model(
            model, in_situ_dict, rho, initial_eff_pressure, depleted_eff_pressure
        )
    if isinstance(model, PhysicsModelPressureSensitivity):
        return _apply_physics_model(
            model,
            in_situ_dict,
            rho,
            initial_eff_pressure,
            depleted_eff_pressure,
            mineral_properties,
            cement_properties,
        )
    raise TypeError(f"Unsupported model type: {type(model)}")


def _apply_regression_model(
    model: RegressionPressureSensitivity,
    in_situ_dict: dict[str, np.ndarray],
    rho: np.ndarray,
    pres_in_situ: np.ndarray,
    pres_depleted: np.ndarray,
) -> dict[str, np.ndarray]:
    """Apply regression-based pressure sensitivity model."""
    # Extract or compute input properties matching model mode
    prop1_in_situ, prop2_in_situ = _extract_input_properties(
        in_situ_dict, model.mode, rho
    )

    # Predict depleted properties
    prop1_depleted, prop2_depleted = model.predict_elastic_properties(
        prop1_in_situ, prop2_in_situ, pres_in_situ, pres_depleted
    )

    # Compute all elastic properties
    return _compute_all_elastic_properties(
        prop1_depleted, prop2_depleted, rho, model.mode
    )


def _apply_physics_model(
    model: PhysicsModelPressureSensitivity,
    in_situ_dict: dict[str, np.ndarray],
    rho: np.ndarray,
    pres_in_situ: np.ndarray,
    pres_depleted: np.ndarray,
    mineral_properties: MineralProperties | EffectiveMineralProperties | None,
    cement_properties: MineralProperties | EffectiveMineralProperties | None,
) -> dict[str, np.ndarray]:
    """Apply physics-based pressure sensitivity model."""
    from rock_physics_open.equinor_utilities.std_functions import velocity

    # Validate required inputs for physics models
    if mineral_properties is None:
        raise PressureSensitivityInputError(
            "Physics-based models require mineral_properties"
        )

    required_keys = {
        ParameterTypes.K.value,
        ParameterTypes.MU.value,
        ParameterTypes.POROSITY.value,
    }
    _validate_required_keys(in_situ_dict, required_keys, "in_situ_dict")

    k_dry = in_situ_dict[ParameterTypes.K.value]
    mu_dry = in_situ_dict[ParameterTypes.MU.value]
    poro = in_situ_dict[ParameterTypes.POROSITY.value]

    # Predict depleted moduli
    k_depleted, mu_depleted = model.predict_elastic_properties(
        k_dry=k_dry,
        mu_dry=mu_dry,
        poro=poro,
        min_prop=mineral_properties,
        in_situ_press=pres_in_situ,
        depl_press=pres_depleted,
        cem_prop=cement_properties,
    )

    # Convert to velocities
    vp, vs = velocity(k_depleted, mu_depleted, rho)[0:2]

    return {
        ParameterTypes.VP.value: vp,
        ParameterTypes.VS.value: vs,
        ParameterTypes.K.value: k_depleted,
        ParameterTypes.MU.value: mu_depleted,
        ParameterTypes.RHO.value: rho,
    }
