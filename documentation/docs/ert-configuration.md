# ERT configuration file

You can include `fmu-pem` in your ERT setup by including the following snippet:

````ert
-- Define your variables:
DEFINE <JOB_STARTDIR> <RUNPATH>/rms/model
DEFINE <RELPATH_CONFIG_FILES> <RUNPATH>/sim2seis/model
DEFINE <PEM_CONFIG_FILE_NAME> pem_config.yml
DEFINE <MODEL_PATH> /my_fmu_structure/sim2seis/model

-- Run the pre-installed ERT forward model:
FORWARD_MODEL PEM(<START_DIR>=<JOB_STARTDIR>, <CONFIG_DIR>=<RELPATH_CONFIG_FILES>, <CONFIG_FILE>=<PEM_CONFIG_FILE_NAME>, <MODEL_DIR>=<MODEL_PATH>)
````

On the next page you will get help setting up your `pem_config.yml`.
