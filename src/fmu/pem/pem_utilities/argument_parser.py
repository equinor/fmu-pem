import argparse
from pathlib import Path


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
            "Path to config directory (required). This can be the 'sim2seis/model' "
            "directory itself or a parent directory containing it."
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
        help="Relative path to global config directory (required)",
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
    return parser.parse_args(arguments)
