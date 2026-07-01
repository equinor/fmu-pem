# python
# File: src/fmu/pem/pem_functions/pressure_sensitivity.py
from __future__ import annotations

from typing import Literal

import numpy as np

from fmu.pem.pem_utilities.enum_defs import (
    ParameterTypes,
    PhysicsPressureModelTypes,
    RegressionPressureModelTypes,
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
    mode: Literal["vp_vs", "k_mu"],
    rho: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract or compute the two elastic properties needed for the model.

    Parameters
    ----------
    in_situ_dict : dict[str, np.ndarray]
        Dictionary with in-situ properties. Must contain either (vp, vs) or (k, mu).
    mode : Literal["vp_vs", "k_mu"]
        Model mode determining which properties are needed.
    rho : np.ndarray
        Density array for conversions.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        (prop1, prop2) matching the model mode:
        - "vp_vs" mode: (vp, vs)
        - "k_mu" mode: (k, mu)

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

    if mode == "vp_vs":
        if has_velocities:
            return in_situ_dict[vp_key], in_situ_dict[vs_key]
        raise PressureSensitivityInputError(
            f"For vp_vs mode pressure regression model, {vp_key}, "
            f"and {vs_key} are needed"
        )
    # k_mu mode
    if has_moduli:
        return in_situ_dict[k_key], in_situ_dict[mu_key]
    raise PressureSensitivityInputError(
        f"For k_mu mode pressure regression model, {k_key} and {mu_key} are needed"
    )


def _compute_all_elastic_properties(
    prop1: np.ndarray,
    prop2: np.ndarray,
    rho: np.ndarray,
    mode: Literal["vp_vs", "k_mu"],
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
    mode : Literal["vp_vs", "k_mu"]
        Model mode indicating which properties were predicted.

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing vp, vs, k, mu, and rho.
    """
    from rock_physics_open.equinor_utilities.std_functions import moduli, velocity

    if mode == "vp_vs":
        vp, vs = prop1, prop2
        k, mu = moduli(vp, vs, rho)
    else:  # k_mu mode
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
        Dictionary with 'vp', 'vs', 'k', 'mu', 'rho'.if has_moduli:
            # Convert from moduli to velocities
            vp, vs = velocity(in_situ_dict[k_key], in_situ_dict[mu_key], rho)[0:2]
            return vp, vs


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
    raise TypeError(
        f"Unsupported model type for pressure sensitivity: {type(model)}. \n"
        f"Available options for physics based models are "
        f"{PhysicsPressureModelTypes.options()} and "
        "Available options for regression based models are "
        f"{RegressionPressureModelTypes.options()}. "
    )


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
            "Physics-based pressure sensitivity models require mineral_properties"
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
