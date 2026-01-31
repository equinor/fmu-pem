"""
The INTERNAL_EQUINOR property means that fmu-pem is run within the Equinor organisation
where there is access to more elaborate fluid models and other rock physics
models.
"""

try:  # noqa: SIM105
    import init_rock_physics
except (ImportError, ModuleNotFoundError):
    INTERNAL_EQUINOR = False
else:
    INTERNAL_EQUINOR = True

from .__main__ import main as pem
from .run_pem import pem_fcn

__all__ = [
    "pem_fcn",
    "pem",
    "INTERNAL_EQUINOR",
]
