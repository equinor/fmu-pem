import os
from pathlib import Path

import yaml

from fmu.config.utilities import yaml_load

from .pem_config_validation import PemConfig
from .utils import restore_dir


def find_key_first(d: dict, key: str) -> str | None:
    """Recursively search for the first occurrence of a key in nested dicts.

    The search now prioritizes keys at the current dictionary level before
    descending into nested dictionaries, ensuring top-level occurrences win when
    duplicates exist deeper in the structure.

    Args:
        d: A potentially nested mapping structure where values may themselves be
            dictionaries. Typically a ``dict`` originating from parsed YAML/JSON.
        key: The key to search for in ``d`` and any nested dictionaries.

    Returns:
        The value associated with the first occurrence of ``key`` encountered during
        the depth-first search, or ``None`` if the key is not present.

    Example:
        >>> data = {"a": 1, "b": {"target": 2, "c": {"target": 3}}}
        >>> find_key_first(data, "target")
        2
    """
    if not isinstance(d, dict):
        return None
    if key in d:
        return d[key]
    for v in d.values():
        if isinstance(v, dict):
            result = find_key_first(v, key)
            if result is not None:
                return result
    return None


def get_global_params_and_dates(
    global_config_dir: Path,
    global_conf_file: Path,
    mod_prefix: str | None = None,
    obs_prefix: str | None = None,
) -> dict:
    """Read global configuration parameters, simulation model dates and seismic dates
    for difference calculation

    Args:
        global_config_dir: directory path for the global config file
        global_conf_file: name of the global config file

    Returns:
        global parameter configuration dict, list of strings for simulation dates,
        list of tuples with
                strings of dates to calculate difference properties
    """
    global_config_par = yaml_load(
        str(global_config_dir / global_conf_file),
    )
    grid_model_name = find_key_first(global_config_par["global"], "ECLGRIDNAME_PEM")
    if grid_model_name is None:
        raise ValueError(
            f"{__file__}: no value for ECLGRIDNAME_PEM in global config file"
        )
    # Find the correct seismic dates references
    dates_config = global_config_par["global"]["dates"]
    return_dict = {
        "global_config": global_config_par,
        "grid_model": grid_model_name,
        "seismic": global_config_par["global"]["seismic"],
    }
    if mod_prefix:
        return_dict.update(
            {
                "mod_dates": dates_config.get(f"SEISMIC_{mod_prefix}_DATES", None),
                "mod_diffdates": dates_config.get(
                    f"SEISMIC_{mod_prefix}_DIFFDATES", None
                ),
            }
        )
    if obs_prefix:
        return_dict.update(
            {
                "obs_dates": dates_config.get(f"SEISMIC_{obs_prefix}_DATES", None),
                "obs_diffdates": dates_config.get(
                    f"SEISMIC_{obs_prefix}_DIFFDATES", None
                ),
            }
        )

    return return_dict


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
