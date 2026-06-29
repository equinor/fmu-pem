from __future__ import annotations

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepJSON,
    ForwardModelStepPlugin,
)


class PemCleanup(ForwardModelStepPlugin):
    def __init__(self) -> None:
        super().__init__(
            name="PEM_CLEANUP",
            command=[
                "pem_cleanup",
                "--grid_dir",
                "<GRID_DIR>",
                "--save_type_list",
                "<SAVE_TYPE_LIST>",
                "--is_ensemble",
                "<IS_ENSEMBLE>",
                "--prefix",
                "<PREFIX>",
                "--extension",
                "<EXTENSION>",
            ],
        )

    def validate_pre_realization_run(
        self, fm_step_json: ForwardModelStepJSON
    ) -> ForwardModelStepJSON:
        return fm_step_json

    def validate_pre_experiment(self, _fm_step_json: ForwardModelStepJSON) -> None:
        pass

    @staticmethod
    def documentation() -> ForwardModelStepDocumentation | None:
        return ForwardModelStepDocumentation(
            category="modelling.reservoir",
            source_package="fmu.pem",
            source_function_name="PemCleanup",
            description="",
            examples="""
.. code-block:: console

  FORWARD_MODEL PEM_CLEANUP(<GRID_DIR>=<RUNPATH>/share/results/grids, <SAVE_TYPE_LIST>=intermediate, <IS_ENSEMBLE>=false, <PREFIX>=simgrid, <EXTENSION>=.roff)

""",  # noqa: E501
        )
