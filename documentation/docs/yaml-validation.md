# YAML File Validation

The entire `pem` workflow requires a significant number of parameters and constants to run. These are all gathered in
a YAML file, which is validated through a `pydantic` process. When setting up a YAML file for a project for the first time,
we recommend using the [interface](https://equinor.github.io/fmu-pem/pem-configuration.html). Once saved,
you can edit the YAML file in any standard text editor. The interface hides certain standard settings that typically
do not require modification. Example files with all options and commented standard settings can be found in the
[GitHub repository](https://github.com/equinor/fmu-pem/blob/main/tests/data/sim2seis/model/pem_config_no_condensate.yml).

There is also a global configuration file in YAML format, which is used throughout the FMU process. In this context,
the main information used is a set of dates for which the estimation is made, also the dates from which difference
seismic is estimated. The name of output grid is also read from the global config file.

## Validation Process

Entries in the YAML file are validated through `pydantic`. This validation checks that referenced files and directories exist,
that parameters are of the correct type, and to some extent that numerical values fall within expected ranges. If
`pydantic` encounters errors, messages will appear in the console or in error message files if the process is run from
`ert`. Unfortunately, the `pydantic` error messages can be cryptic, and you may need to contact an `fmu-pem` developer
or superuser to resolve the issue.
