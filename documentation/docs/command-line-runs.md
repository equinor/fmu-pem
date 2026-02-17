# Command-line runs

PEM can be called from ERT, run as an external command in RMS, or run from command-line.
In all cases, there is a number of required call arguments that must be provided:

```shell
> # Go to top of the project structure
> cd /project/fmu/tutorial/drogon/resmod/ff/users/hfle/dev
> # Call PEM, `--help` will show all call arguments
> pem --help
> pem -c ./sim2seis/model -f new_pem_config.yml -g ../../fmuconfig/output -o global_variables.yml --mod-date-prefix HIST
