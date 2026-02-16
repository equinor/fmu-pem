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
                "--config-dir",
                "<CONFIG_DIR>",
                "--config-file",
                "<CONFIG_FILE>",
                "--global-dir",
                "<GLOBAL_DIR>",
                "--global-file",
                "<GLOBAL_FILE>",
                "--mod-date-prefix",
                "<MOD_DATE_PREFIX>",
            ],
        )

    def validate_pre_realization_run(
        self, fm_step_json: ForwardModelStepJSON
    ) -> ForwardModelStepJSON:
        return fm_step_json

    def validate_pre_experiment(self, fm_step_json: ForwardModelStepJSON) -> None:
        # Parse YAML parameter file by pydantic pre-experiment to catch errors at an
        # early stage

        args = parse_arguments(fm_step_json["argList"])

        try:
            with restore_dir(args.config_dir):
                _ = read_pem_config(args.config_file)
        except Exception as e:
            raise ForwardModelStepValidationError(f"pem validation failed:\n {str(e)}")

    @staticmethod
    def documentation() -> ForwardModelStepDocumentation | None:
        return ForwardModelStepDocumentation(
            category="modelling.reservoir",
            source_package="fmu.pem",
            source_function_name="PetroElasticModel",
            description="",
            examples="""
.. code-block:: console

  FORWARD_MODEL PEM(<CONFIG_DIR>=../../sim2seis/model, <CONFIG_FILE>=new_pem.yml, <GLOBAL_DIR>=../../fmuconfig/output, <GLOBAL_FILE>=global_variables.yml, <MOD_DATE_PREFIX>=HIST)

""",  # noqa: E501,
        )
