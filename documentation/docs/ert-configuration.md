# ERT configuration file

You can include `fmu-pem` in your ERT setup by including the following snippet:

````ert
-- Define your variables:
DEFINE <CONFIG_PATH> <RUNPATH>/sim2seis/model
DEFINE <PEM_CONFIG_FILE_NAME> <CONFIG_PATH>/pem_config.yml
DEFINE <GLOBAL_CONFIG_DIR> fmuconfig/output
DEFINE <GLOBAL_CONFIG_FILE> <GLOBAL_CONFIG_DIR>/global_variables.yml
DEFINE <MOD_PREFIX> HIST
DEFINE <VERBOSE_FLAG> true

-- Run the pre-installed ERT forward model:
FORWARD_MODEL PEM(<CONFIG_FILE>=<PEM_CONFIG_FILE_NAME>, <GLOBAL_FILE>=<GLOBAL_CONFIG_FILE>, <MOD_DATE_PREFIX>=<MOD_PREFIX>, <VERBOSE>=<VERBOSE_FLAG>)
````

On the next page you will get help on setting up your `pem_config.yml`.
