# How to use fmu-pem

Petro-elastic model (PEM) for [fmu-sim2seis](https://github.com/equinor/fmu-sim2seis)
based on the [rock-physics-open](https://github.com/equinor/rock-physics-open)
library.

## Installation

To install `fmu-pem`, first activate a virtual environment, then type:

```
pip install fmu-pem
```

The PEM is controlled by parameter settings in a *yaml-file*, given as part of the
command line arguments, or by the workflow parameter if it is run as an ERT forward model.

## Calibration of rock physics models

Calibration of the rock physics models is normally carried out in
[RokDoc](https://www.ikonscience.com/rokdoc-geoprediction-software-platform/)
prior to running the PEM. Fluid and mineral properties can be found in the RokDoc project, or
from LFP logs, if they are available.

> [!NOTE]  
> The fluid models contained in this module may not cover all possible cases. Gas condensate, very heavy oil, 
> or reservoir pressure under hydrocarbon bubble point will need additional proprietary code to run.
>
> Equinor users can install additional proprietary models using
> ```bash
> pip install "git+ssh://git@github.com/equinor/rock-physics"`
> ```

## User interface

Users can visit https://equinor.github.io/fmu-pem/ in order to get help configuring the `fmu-pem` input data.

# How to develop fmu-pem

Developing the user interface can be done by:
```bash
cd ./user-interface-config
npm ci  # Install dependencies
npm run create-json-schema  # Extract JSON schema from Python code
npm run dev  # Start local development server
```
The JSON schema itself (type, title, description etc.) comes from the corresponding Pydantic models in the Python code.
