import os
from pathlib import Path

import yaml

from fmu.config.utilities import yaml_load

from .pem_config_validation import PemConfig
from .utils import restore_dir


def get_global_params_and_dates(root_dir: Path, conf_path: Path) -> dict:
    """Read global configuration parameters, simulation model dates and seismic dates
    for difference calculation

    Args:
        root_dir: start dir for PEM script run
        conf_path: path to global variables configuration file

    Returns:
        global parameter configuration dict, list of strings for simulation dates,
        list of tuples with
                strings of dates to calculate difference properties
    """
    # prediction_mode is set to empty string if HIST else to PRED. Normally set in
    # env variable
    env_flowsim = os.getenv("FLOWSIM_IS_PREDICTION", default=False)
    if env_flowsim:
        conf_file = conf_path.joinpath("global_variables_pred.yml")
        date_str = "SEISMIC_PRED_DATES"
        diff_str = "SEISMIC_PRED_DIFFDATES"
    else:
        conf_file = conf_path.joinpath("global_variables.yml")
        date_str = "SEISMIC_HIST_DATES"
        diff_str = "SEISMIC_HIST_DIFFDATES"
    with restore_dir(root_dir):
        global_config_par = yaml_load(str(conf_file))
        seismic_dates = [
            str(sdate).replace("-", "")
            for sdate in global_config_par["global"]["dates"][date_str]
        ]
        diff_dates = [
            [str(sdate).replace("-", "") for sdate in datepairs]
            for datepairs in global_config_par["global"]["dates"][diff_str]
        ]
        # Grid model name can be under different top dicts - search for it. If more
        # than one is found, and they are not equal - raise an error
        found_grid_name = False
        for key in global_config_par:
            try:
                if not found_grid_name:
                    grid_model_name = global_config_par[key]["ECLGRIDNAME_PEM"]
                    found_grid_name = True
                else:
                    if not grid_model_name == global_config_par[key]["ECLGRIDNAME_PEM"]:
                        raise ValueError(
                            f"{__file__}: inconsistent names for "
                            f"ECLGRIDNAME_PEM in global config file"
                        )
            except KeyError:
                pass
        if not found_grid_name:
            raise ValueError(
                f"{__file__}: no value for ECLGRIDNAME_PEM in global config file"
            )
        return {
            "grid_model": grid_model_name,
            "seis_dates": seismic_dates,
            "diff_dates": diff_dates,
            "global_config": global_config_par,
        }


def read_pem_config(yaml_file: Path) -> PemConfig:
    """Read PEM specific parameters

    Args:
        yaml_file: file name for PEM parameters

    Returns:
        PemConfig object with PEM parameters
    """

    def join(loader, node):
        seq = loader.construct_sequence(node)
        return "".join([str(i) for i in seq])

    # register the tag handler
    yaml.add_constructor("!join", join)

    with yaml_file.open() as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return PemConfig(**data)
