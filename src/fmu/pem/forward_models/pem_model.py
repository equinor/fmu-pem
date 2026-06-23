from __future__ import annotations

import os
from pathlib import Path

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepJSON,
    ForwardModelStepPlugin,
    ForwardModelStepValidationError,
)

from fmu.pem.pem_utilities import parse_arguments, read_pem_config, restore_dir


class PetroElasticModel(ForwardModelStepPlugin):
    def __init__(self) -> None:
        super().__init__(
            name="PEM",
            command=[
                "pem",
                "--config-file",
                "<CONFIG_FILE>",
                "--global-file",
                "<GLOBAL_FILE>",
                "--mod-date-prefix",
                "<MOD_DATE_PREFIX>",
                "--verbose",
                "<VERBOSE>",
            ],
        )

    def validate_pre_realization_run(
        self, fm_step_json: ForwardModelStepJSON
    ) -> ForwardModelStepJSON:
        return fm_step_json

    def validate_pre_experiment(self, _fm_step_json: ForwardModelStepJSON) -> None:
        # No-op: fmu-pem depends on files created later in the ERT workflow,
        # so pre-experiment validation cannot meaningfully verify them.
        pass

    @staticmethod
    def documentation() -> ForwardModelStepDocumentation | None:
        return ForwardModelStepDocumentation(
            category="modelling.reservoir",
            source_package="fmu.pem",
            source_function_name="PetroElasticModel",
            description="",
            examples="""
.. code-block:: console

  FORWARD_MODEL PEM(<CONFIG_FILE>=./sim2seis/model/new_pem.yml, <GLOBAL_FILE>=fmuconfig/output/global_variables.yml, <MOD_DATE_PREFIX>=HIST, <VERBOSE>=true)

""",  # noqa: E501,
        )
