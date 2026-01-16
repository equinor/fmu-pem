# pylint: disable=missing-module-docstring
import argparse
from pathlib import Path
from warnings import warn

from .pem_utilities import restore_dir
from .run_pem import pem_fcn


def main():
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
    args = parser.parse_args()
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
        pem_fcn(
            config_dir=run_folder,
            pem_config_file_name=args.config_file,
            global_config_dir=args.global_dir,
            global_config_file=args.global_file,
        )


if __name__ == "__main__":
    main()
