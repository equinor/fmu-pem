import warnings

import numpy as np
from rock_physics_open.fluid_models import (
    brine_properties as open_brine_properties,
)
from rock_physics_open.fluid_models import (
    gas_properties as open_gas_properties,
)
from rock_physics_open.fluid_models import (
    oil_properties as open_oil_properties,
)
from rock_physics_open.fluid_models.oil_model.oil_bubble_point import (
    bp_standing as open_bp_standing,
)
from rock_physics_open.span_wagner import (
    co2_properties as open_co2_properties,
)

from fmu.pem.pem_utilities.enum_defs import GasModels

# This file acts as a compatibility layer (adapter) for proprietary rock physics models.
# It uses the proprietary implementation when available, otherwise falls back to
# open-source alternatives. Ensures consistent parameters, return types, units
# and clear error handling across all rock physics operations.
HAS_PROPRIETARY_ROCK_PHYSICS: bool
"""`True` if the proprietary rock_physics package is installed and importable
with all required modules, `False` otherwise."""

try:
    from rock_physics.fluid_models import (  # type: ignore[import]
        brine_properties as internal_brine_properties,
    )
    from rock_physics.fluid_models import (  # type: ignore[import]
        co2_properties as internal_co2_properties,
    )
    from rock_physics.fluid_models import (  # type: ignore[import]
        condensate_properties as internal_condensate_properties,
    )
    from rock_physics.fluid_models import (  # type: ignore[import]
        gas_properties as internal_gas_properties,
    )
    from rock_physics.fluid_models import (  # type: ignore[import]
        oil_properties as internal_oil_properties,
    )
    from rock_physics.fluid_models import (  # type: ignore[import]
        saturations_below_bubble_point as internal_saturations_below_bubble_point,
    )
    from rock_physics.fluid_models.oil_model.oil_bubble_point import (  # type: ignore[import]
        bp_standing as internal_bp_standing,
    )

    HAS_PROPRIETARY_ROCK_PHYSICS = True
except (ImportError, ModuleNotFoundError, NotImplementedError):
    HAS_PROPRIETARY_ROCK_PHYSICS = False


def bp_standing(
    density: np.ndarray,
    gas_oil_ratio: np.ndarray,
    gas_gravity: np.ndarray,
    temperature: np.ndarray,
) -> np.ndarray:
    """Calculate bubble point pressure with proprietary model when available.

    Otherwise, uses open-source model.
    """
    if HAS_PROPRIETARY_ROCK_PHYSICS:
        bp = internal_bp_standing(
            density=density,
            gas_oil_ratio=gas_oil_ratio,
            gas_gravity=gas_gravity,
            temperature=temperature,
        )
    else:
        bp = open_bp_standing(
            density=density,
            gas_oil_ratio=gas_oil_ratio,
            gas_gravity=gas_gravity,
            temperature=temperature,
        )
    return bp


def brine_properties(
    temperature: np.ndarray,
    pressure: np.ndarray,
    salinity: np.ndarray,
    p_nacl: np.ndarray,
    p_cacl: np.ndarray,
    p_kcl: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate brine properties with proprietary (FLAG) model when available.

    Otherwise, uses open-source (Batzle & Wang) model.

    `p_nacl`, `p_cacl`, `p_kcl` parameters are only used for the proprietary model.
    """
    if HAS_PROPRIETARY_ROCK_PHYSICS:
        vp, rho, bulk = internal_brine_properties(
            temperature=temperature,
            pressure=pressure,
            salinity=salinity,
            p_nacl=p_nacl,
            p_cacl=p_cacl,
            p_kcl=p_kcl,
        )
    else:
        vp, rho, bulk = open_brine_properties(
            temperature=temperature,
            pressure=pressure,
            salinity=salinity,
        )
    return vp, rho, bulk


def co2_properties(
    temperature: np.ndarray,
    pressure: np.ndarray,
    use_proprietary_model: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate CO2 properties with proprietary (FLAG) model when available.

    `use_proprietary_model` can be set to `False` to use open-source (Span & Wagner)
    equivalent, even when the proprietary model is available.

    Note that the Span&Wagner model is recommended, even if the FLAG model is available.
    """
    if use_proprietary_model and HAS_PROPRIETARY_ROCK_PHYSICS:
        vp, rho, bulk = internal_co2_properties(
            temperature=temperature,
            pressure=pressure,
        )
    else:
        vp, rho, bulk = open_co2_properties(
            temp=temperature,
            pres=pressure,
        )
    return vp, rho, bulk


def condensate_properties(
    temperature: np.ndarray,
    pressure: np.ndarray,
    rho0: np.ndarray,
    gas_oil_ratio: np.ndarray,
    gas_gravity: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate condensate properties with proprietary model.

    Raises error if the proprietary model is not available.
    """
    if not HAS_PROPRIETARY_ROCK_PHYSICS:
        raise RuntimeError(
            "Condensate property calculation is not possible without the proprietary "
            "rock physics package installed."
        )

    vp_c, rho_c, bulk_c = internal_condensate_properties(
        temperature=temperature,
        pressure=pressure,
        rho0=rho0,
        gas_oil_ratio=gas_oil_ratio,
        gas_gravity=gas_gravity,
    )
    return vp_c, rho_c, bulk_c


def gas_properties(
    temperature: np.ndarray,
    pressure: np.ndarray,
    gas_gravity: np.ndarray,
    model: GasModels = GasModels.HC2016,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate gas properties with proprietary (FLAG) model when available.

    Otherwise, uses open-source (Batzle & Wang) model.

    `model` parameter is only used for the proprietary model.
    """
    if HAS_PROPRIETARY_ROCK_PHYSICS:
        vp, rho, bulk, _ = internal_gas_properties(
            temperature=temperature,
            pressure=pressure,
            gas_gravity=gas_gravity,
            model=model.value,
        )
    else:
        vp, rho, bulk, _ = open_gas_properties(
            temperature=temperature,
            pressure=pressure,
            gas_gravity=gas_gravity,
        )
    return vp, rho, bulk


def oil_properties(
    temperature: np.ndarray,
    pressure: np.ndarray,
    rho0: np.ndarray,
    gas_oil_ratio: np.ndarray,
    gas_gravity: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate oil properties with proprietary (FLAG) model when available.

    Otherwise, uses open-source (Han-Batzle) model.
    """
    if HAS_PROPRIETARY_ROCK_PHYSICS:
        vp, rho, bulk = internal_oil_properties(
            temperature=temperature,
            pressure=pressure,
            rho0=rho0,
            gas_oil_ratio=gas_oil_ratio,
            gas_gravity=gas_gravity,
        )
    else:
        vp, rho, bulk = open_oil_properties(
            temperature=temperature,
            pressure=pressure,
            rho0=rho0,
            gas_oil_ratio=gas_oil_ratio,
            gas_gravity=gas_gravity,
            model_version="HB",
        )
    return vp, rho, bulk


def saturations_below_bubble_point(
    gas_saturation_init: np.ndarray,
    oil_saturation_init: np.ndarray,
    brine_saturation_init: np.ndarray,
    gor_init: np.ndarray,
    oil_gas_gravity: np.ndarray,
    free_gas_gravity: np.ndarray,
    oil_density: np.ndarray,
    z_factor: float,
    pres_depl: np.ndarray,
    temp_res: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Calculate saturations below bubble point with proprietary model when available.

    Otherwise, raises warning and returns input values back as output.
    """
    if HAS_PROPRIETARY_ROCK_PHYSICS:
        (
            gas_saturation_depleted,
            oil_saturation_depleted,
            gor_depleted,
            gas_gravity_depleted,
        ) = internal_saturations_below_bubble_point(
            gas_saturation_init=gas_saturation_init,
            oil_saturation_init=oil_saturation_init,
            brine_saturation_init=brine_saturation_init,
            gor_init=gor_init,
            oil_gas_gravity=oil_gas_gravity,
            free_gas_gravity=free_gas_gravity,
            oil_density=oil_density,
            z_factor=z_factor,
            pres_depl=pres_depl,
            temp_res=temp_res,
        )
    else:
        warnings.warn(
            "Estimation of oil properties below bubble point requires proprietary "
            "model. Estimation of oil properties below bubble point is uncertain."
        )
        # return input values back as output (do nothing)
        gas_saturation_depleted = gas_saturation_init
        oil_saturation_depleted = oil_saturation_init
        gor_depleted = gor_init
        gas_gravity_depleted = free_gas_gravity
    return (
        gas_saturation_depleted,
        oil_saturation_depleted,
        gor_depleted,
        gas_gravity_depleted,
    )
