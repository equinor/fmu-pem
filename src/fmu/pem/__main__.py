import os
import sys
from pathlib import Path

from .pem_utilities import (
    get_global_params_and_dates,
    parse_arguments,
    read_pem_config,
    restore_dir,
)
from .run_pem import pem_fcn


def _resolve_fmu_rootpath(config_dir: Path) -> Path:
    # First: establish if we run from ERT, if so use the RUNPATH
    if os.environ.get("_ERT_RUNPATH", None):
        return Path(os.environ.get("_ERT_RUNPATH"))

    # Ensure config_dir is absolute before computing the FMU root to avoid
    # depending on the current working directory (common in CLI entrypoints).
    resolved_config_dir = (
        config_dir if config_dir.is_absolute() else config_dir.resolve()
    )

    # The sim2seis config directory is expected to be at ./sim2seis/model
    # relative to the FMU root, so we move up two levels. Use parents[1]
    # instead of appending "../.." to avoid mis-resolution of relative paths.
    try:
        return resolved_config_dir.parents[1]
    except IndexError:
        # If this is the case, the argument for config_dir must be wrong, and
        # it's better to raise an error than to continue
        raise ValueError(
            f"unable to find fmu rootpath from config_dir: {resolved_config_dir}"
        )


def main(args_list=None):
    if args_list is None:
        args_list = sys.argv[1:]
    args = parse_arguments(args_list)

    config_dir = args.config_dir.absolute()
    run_folder = _resolve_fmu_rootpath(config_dir=config_dir)

    with restore_dir(run_folder):
        # Read and validate all PEM parameters
        config = read_pem_config(yaml_file=config_dir / args.config_file)

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
            run_dir=run_folder,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
