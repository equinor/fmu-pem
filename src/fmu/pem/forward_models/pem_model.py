from __future__ import annotations

import os
from pathlib import Path

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepJSON,
    ForwardModelStepPlugin,
    ForwardModelStepValidationError,
)

from fmu.pem.pem_utilities import read_pem_config


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
                "--model-dir",
                "<MODEL_DIR>",
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

        config_file = Path(fm_step_json["argList"][3])
        model_dir = Path(fm_step_json["argList"][9])
        try:
            os.chdir(model_dir)
            _ = read_pem_config(config_file)
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

  FORWARD_MODEL PEM(<CONFIG_DIR>=../../sim2seis/model, <CONFIG_FILE>=new_pem.yml, <GLOBAL_DiR>=../../fmuconfig/output, <GLOBAL_FILE>=global_variables.yml, <MODEL_DIR>=/my_fmu_structure/sim2seis/model, <MOD_DATE_PREFIX>=HIST)

""",  # noqa: E501,
        )
