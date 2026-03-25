import functools
from contextlib import ExitStack
from unittest.mock import Mock, patch

from fmu.pem.pem_utilities import rock_physics_adapter


def _patch_rock_physics_adapter(has_proprietary_rock_physics: bool):
    """Build a decorator that patches `HAS_PROPRIETARY_ROCK_PHYSICS` and all
    mock functions on the `rock_physics_adapter` module.

    When `has_proprietary` is True, internal_* attributes are created if missing
    (simulating an installed proprietary package).
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with ExitStack() as stack:
                stack.enter_context(
                    patch.object(
                        rock_physics_adapter,
                        "HAS_PROPRIETARY_ROCK_PHYSICS",
                        has_proprietary_rock_physics,
                    )
                )

                # need to patch with expected return signature
                _SINGLE = None
                _TRIPLE = (None, None, None)
                _QUAD = (None, None, None, None)

                for name, return_signature in [
                    ("open_brine_properties", _TRIPLE),
                    ("open_co2_properties", _TRIPLE),
                    ("open_bp_standing", _SINGLE),
                    ("open_gas_properties", _QUAD),
                    ("open_oil_properties", _TRIPLE),
                ]:
                    stack.enter_context(
                        patch.object(
                            rock_physics_adapter,
                            name,
                            Mock(return_value=return_signature),
                        )
                    )
                for name, return_signature in [
                    ("internal_brine_properties", _TRIPLE),
                    ("internal_co2_properties", _TRIPLE),
                    ("internal_bp_standing", _SINGLE),
                    ("internal_gas_properties", _QUAD),
                    ("internal_oil_properties", _TRIPLE),
                    ("internal_condensate_properties", _TRIPLE),
                    ("internal_saturations_below_bubble_point", _QUAD),
                ]:
                    if has_proprietary_rock_physics:
                        stack.enter_context(
                            patch.object(
                                rock_physics_adapter,
                                name,
                                Mock(return_value=return_signature),
                                create=True,
                            )
                        )
                    elif hasattr(rock_physics_adapter, name):
                        original = getattr(rock_physics_adapter, name)
                        delattr(rock_physics_adapter, name)
                        stack.callback(setattr, rock_physics_adapter, name, original)
                return func(*args, **kwargs)

        return wrapper

    return decorator


ensure_rock_physics_not_installed = _patch_rock_physics_adapter(
    has_proprietary_rock_physics=False,
)
"""Decorator: ensure the proprietary rock physics package can _not_ be used,
even if it is installed in the test environment."""

mock_installed_proprietary_rock_physics = _patch_rock_physics_adapter(
    has_proprietary_rock_physics=True
)
"""Decorator: simulate the proprietary rock physics package being installed,
adding mock implementations of adapter functions to assert paths."""
