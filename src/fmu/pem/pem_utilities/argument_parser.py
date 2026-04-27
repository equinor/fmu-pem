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
        f"Invalid boolean value: {value!r}. Expected true/false."
    )


def parse_arguments(
    arguments: list[str],
) -> argparse.Namespace:
    """
    Uses argparse to parse arguments as expected from command line invocation
    """
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-c",
        "--config-dir",
        type=Path,
        required=True,
        help=(
            "Path to config directory (required), normally the 'sim2seis/model' "
            "directory under the FMU top direectory."
        ),
    )
    parser.add_argument(
        "-f",
        "--config-file",
        type=Path,
        required=True,
        help="Configuration yaml file name",
    )
    parser.add_argument(
        "-g",
        "--global-dir",
        type=Path,
        required=True,
        help=(
            "Path to global config directory (required) relative to the FMU top "
            "directory"
        ),
    )
    parser.add_argument(
        "-o",
        "--global-file",
        type=Path,
        required=True,
        help="Global configuration yaml file name (required)",
    )
    parser.add_argument(
        "-q",
        "--mod-date-prefix",
        type=str,
        required=True,
        help="Global seismic section: Prefix for seismic dates for modelled data",
    )
    parser.add_argument(
        "-m",
        "--model-dir",
        type=Path,
        required=False,
        help=(
            "Only required for ERT runs: pointer to the project area's "
            "`sim2seis/model` folder"
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=_str2bool,
        required=False,
        default=False,
        help="Select verbose or minimal output",
    )
    return parser.parse_args(arguments)
