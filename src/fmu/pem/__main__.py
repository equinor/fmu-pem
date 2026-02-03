# pylint: disable=missing-module-docstring
import argparse
import sys
from pathlib import Path
from typing import Any
from warnings import warn

from .pem_utilities import get_global_params_and_dates, read_pem_config, restore_dir
from .run_pem import pem_fcn


def main(args_list=None):
    if args_list is None:
        args_list = sys.argv[1:]
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-c",
        "--config-dir",
        type=Path,
        required=True,
        help="Path to config file (required)",
    )
    parser.add_argument(
        "-f",
        "--config-file",
        type=Path,
        required=True,
        help="Configuration yaml file name (required)",
    )
    parser.add_argument(
        "-g",
        "--global-dir",
        type=Path,
        required=True,
        help="Relative path to global config file (required)",
    )
    parser.add_argument(
        "-o",
        "--global-file",
        type=Path,
        required=True,
        help="Global configuration yaml file name (required)",
    )
    parser.add_argument(
        "-m",
        "--model-dir",
        type=Path,
        required=False,
        help="For ERT run: Absolute directory name for model file, pre-experiment. Not "
        "needed for command line run",
    )
    parser.add_argument(
        "-q",
        "--mod-date-prefix",
        type=str,
        required=True,
        help="Global seismic section: Prefix for seismic dates for modelled data",
    )
    args = parser.parse_args(args_list)
    cwd = args.config_dir.absolute()
    if str(cwd).endswith("sim2seis/model"):
        run_folder = cwd
    else:
        try:
            run_folder = cwd / "sim2seis" / "model"
            assert run_folder.exists() and run_folder.is_dir()
        except AssertionError as e:
            warn(f"PEM model should be run from the sim2seis/model folder. {e}")
            run_folder = cwd
    with restore_dir(run_folder):
        # Read and validate all PEM parameters
        config = read_pem_config(yaml_file=run_folder / args.config_file)

        # Read necessary part of global configurations and parameters
        config.update_with_global(
            get_global_params_and_dates(
                global_config_dir=(run_folder / args.global_dir).resolve(),
                global_conf_file=args.global_file,
                mod_prefix=args.mod_date_prefix,
            )
        )
        pem_fcn(
            config=config,
            config_dir=run_folder,
        )


if __name__ == "__main__":
    main()
