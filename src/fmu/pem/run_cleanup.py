import sys

from fmu.pem.pem_utilities.argument_parser import parse_cleanup
from fmu.pem.pem_utilities.cleanup import cleanup_pem_results


def run_pem_cleanup(args_list=None):
    if args_list is None:
        args_list = sys.argv[1:]
    args = parse_cleanup(args_list)

    cleanup_pem_results(
        directory=args.grid_dir,
        remove_categories=args.save_type_list,
        is_ensemble=args.is_ensemble,
        prefix=args.prefix,
        extension=args.extension,
    )


if __name__ == "__main__":
    run_pem_cleanup()
