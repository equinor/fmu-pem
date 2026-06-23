import argparse
from pathlib import Path


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
    Uses argparse to parse arguments as expected from command line invocation
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
