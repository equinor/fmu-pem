from __future__ import annotations

import ert

from fmu.pem.forward_models import PetroElasticModel

PLUGIN_NAME = "pem"


@ert.plugin(name=PLUGIN_NAME)
def installable_workflow_jobs() -> dict[str, str]:
    return {}


@ert.plugin(name=PLUGIN_NAME)
def installable_forward_model_steps() -> list[ert.ForwardModelStepPlugin]:
    return [  # type: ignore
        PetroElasticModel,
    ]
