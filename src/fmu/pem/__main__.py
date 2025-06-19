# pylint: disable=missing-module-docstring
import argparse
from pathlib import Path
from warnings import warn

from .pem_utilities import restore_dir
from .run_pem import pem_fcn


def main():
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-s",
        "--startdir",
        type=Path,
        required=True,
        help="Start directory for running script (required)",
    )
    parser.add_argument(
        "-c",
        "--configdir",
        type=Path,
        required=True,
        help="Path to config file (required)",
    )
    parser.add_argument(
        "-f",
        "--configfile",
        type=Path,
        required=True,
        help="Configuration yaml file name (required)",
    )
    args = parser.parse_args()
    cwd = args.startdir
    if str(cwd).endswith("rms/model"):
        run_folder = cwd
    else:
        try:
            run_folder = cwd.joinpath("rms/model")
            assert run_folder.exists() and run_folder.is_dir()
        except AssertionError as e:
            warn(f"PEM model should be run from the rms/model folder. {e}")
            run_folder = cwd
    with restore_dir(run_folder):
        pem_fcn(
            start_dir=args.startdir,
            rel_path_pem=args.configdir,
            pem_config_file_name=args.configfile,
        )


if __name__ == "__main__":
    main()
