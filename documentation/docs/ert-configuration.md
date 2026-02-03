# ERT configuration file

You can include `fmu-pem` in your ERT setup by including the following snippet:

````ert
-- Define your variables:
DEFINE <CONFIG_PATH> <RUNPATH>/sim2seis/model
DEFINE <PEM_CONFIG_FILE_NAME> pem_config.yml
DEFINE <GLOBAL_CONFIG_DIR> ../../fmuconfig/output
DEFINE <GLOBAL_CONFIG_FILE> global_variables.yml
DEFINE <MODEL_PATH> /my_fmu_structure/sim2seis/model
DEFINE <MOD_PREFIX> HIST

-- Run the pre-installed ERT forward model:
FORWARD_MODEL PEM(<CONFIG_DIR>=<CONFIG_PATH>, <CONFIG_FILE>=<PEM_CONFIG_FILE_NAME>, <GLOBAL_DIR>=<GLOBAL_CONFIG_DIR>, <GLOBAL_FILE>=<GLOBAL_CONFIG_FILE>, <MODEL_DIR>=<MODEL_PATH>, <MOD_DATE_PREFIX>=<MOD_PREFIX>)
````

On the next page you will get help on setting up your `pem_config.yml`.
