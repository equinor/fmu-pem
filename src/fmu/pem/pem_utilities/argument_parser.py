import argparse
from pathlib import Path

from fmu.pem.pem_utilities.enum_defs import SaveTypes


def _str2bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(
        f"Argument parser: Invalid boolean value: {value!r}. Expected true/false."
    )


def parse_arguments(
    arguments: list[str],
) -> argparse.Namespace:
    """
    Uses argparse to parse arguments as expected from command line invocation for pem
    """
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-f",
        "--config-file",
        type=Path,
        required=True,
        help="Configuration yaml path name",
    )
    parser.add_argument(
        "-g",
        "--global-file",
        type=Path,
        required=True,
        help="Global configuration yaml path name",
    )
    parser.add_argument(
        "-m",
        "--mod-date-prefix",
        type=str,
        required=True,
        help="Global seismic section: Prefix for seismic dates for modelled data",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=_str2bool,
        required=False,
        default=False,
        help="Select verbose or minimal output",
    )
    # Split config and global path into directory and file name, as this is
    # required in the PEM
    args = parser.parse_args(arguments)
    args.config_dir = Path(args.config_file.parent)
    args.config_file = Path(args.config_file.name)
    args.global_dir = Path(args.global_file.parent)
    args.global_file = Path(args.global_file.name)

    return args


def parse_cleanup(
    arguments: list[str],
) -> argparse.Namespace:
    """
    Uses argparse to parse arguments as expected from command line invocation for
    pem_cleanup
    """
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-g",
        "--grid_dir",
        type=Path,
        required=True,
        help="Path name of the directory with grid files from PEM run",
    )
    parser.add_argument(
        "-s",
        "--save_type_list",
        nargs="+",
        type=str,
        choices=[t.value for t in SaveTypes],
        required=True,
        help="List of save batches: 'all', 'intermediate', 'difference', 'elastic'",
    )
    parser.add_argument(
        "-i",
        "--is_ensemble",
        type=_str2bool,
        required=False,
        default=False,
        help="Delete all grids in an ensemble run, default=False",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="simgrid",
        required=False,
        help="Prefix in grid file names, default='simgrid'",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default=".roff",
        required=False,
        help="Grid file name extension, default='.roff'",
    )
    return parser.parse_args(arguments)
