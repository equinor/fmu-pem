from __future__ import annotations

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepJSON,
    ForwardModelStepPlugin,
    ForwardModelStepValidationError,
)


class PetroElasticModel(ForwardModelStepPlugin):
    def __init__(self) -> None:
        super().__init__(
            name="PEM",
            command=[
                "pem",
                "--startdir",
                "<START_DIR>",
                "--configdir",
                "<CONFIG_DIR>",
                "--configfile",
                "<CONFIG_FILE>",
            ],
        )

    def validate_pre_realization_run(
        self, fm_step_json: ForwardModelStepJSON
    ) -> ForwardModelStepJSON:
        return fm_step_json

    def validate_pre_experiment(self, fm_step_json: ForwardModelStepJSON) -> None:
        import os
        from pathlib import Path

        from fmu.pem.pem_utilities import read_pem_config

        model_dir_env = os.environ.get("PEM_MODEL_DIR")
        if model_dir_env is None:
            raise ValueError(
                'environment variable "PEM_MODEL_DIR" must be set to '
                "validate PEM model pre-experiment"
            )
        model_dir = Path(model_dir_env)

        runpath_config_dir = Path(fm_step_json["argList"][3])
        config_dir = (
            model_dir
            / "../.."
            / runpath_config_dir.parent.name
            / runpath_config_dir.name
        ).resolve()
        config_file = fm_step_json["argList"][5]
        try:
            os.chdir(model_dir)
            _ = read_pem_config(config_dir / config_file)
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

  FORWARD_MODEL PEM(<START_DIR>=../../rms/model, <CONFIG_DIR>=../../sim2seis/model, <CONFIG_FILE>=new_pem.yml)

""",  # noqa: E501,
        )
