
# Why and How Petro-elastic Modelling - PEM

The FMU `pem` workflow calculates elastic parameters based on input from reservoir simulator results, model selections
and constant parameters. `pem` is an important step in the FMU `sim2seis` workflow, see [sim2seis documentation](https://equinor.github.io/fmu-sim2seis/).

Whilst `pem` can be run as an independent tool, its primary use is as part of the `sim2seis` workflow. This is described in a chapter below.

`pem` performs of the following tasks:

1. [Read and validate parameter file in `YAML` format](./yaml-validation.md)
2. [Import reservoir simulator results](import-sim-results.md)
3. [Estimate effective mineral properties](./effective-mineral-properties.md)
4. [Estimate effective fluid properties for each date](./fluid_properties.md)
5. [Estimate effective pressure for each date](effective-pressure.md)
6. [Estimate effective properties for saturated rock](./saturated-rock.md)
7. [(Optional) estimate difference properties](./difference-properties.md)
8. [Save intermediate (optional) and final estimates](./save-results.md)

Each step is described in some detail in the links.

## As a general user of FMU, how much do I need to know?

Calibration of a petro-elastic model is considered to be a specialist task, but it should be carried out in close
cooperation with asset teams who has the detailed field knowledge. Without interaction with most disciplines
from the asset, it is highly likely that wrong assumptions are made. The main responsibility lies with geophysics.
[Table 1](#table-1-discipline-topics) below shows topics that must be coordinated with other disciplines.

| Topic                      | Discipline(s) Involved                                      | Description                                                             |
|----------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------|
| Reservoir properties       | Reservoir Engineering                                       | Input on static and dynamic reservoir properties                        |
| Mineralogy                 | Geology, Petrophysics                                       | Data on mineral composition and volume fractions                        |
| Fluid properties           | Petrophysics, Reservoir Engineering, Production Engineering | Details on fluid types, composition, properties, and phase behavior     |
| Pressure and stress regime | Geomechanics, Operation Geology                             | Information on in-situ stresses and pressure changes                    |
| Seismic data calibration   | Geophysics                                                  | Alignment of model outputs with seismic observations, wavelet selection |
| Well data integration      | Petrophysics                                                | Selection of well logs for model calibration                            |
| Production history         | Reservoir Engineering, Production Engineering               | Historical production data for model validation                         |

<span id="table-1-discipline-topics"><strong>Table 1:</strong> Topics that should be coordinated between disciplines during PEM calibration.</span>

## Command-line runs

PEM can be called from ERT, run as an external command in RMS, or run from command-line.
In all cases, there is a number of required call arguments that must be provided:

```shell
> # Go to top of the project structure
> cd /project/fmu/tutorial/drogon/resmod/ff/users/hfle/dev
> # Call PEM, `--help` will show all call arguments
> pem --help
> pem -c ./sim2seis/model -f new_pem_config.yml -g ../../fmuconfig/output -o global_variables.yml -m ./sim2seis/model --mod-date-prefix HIST
