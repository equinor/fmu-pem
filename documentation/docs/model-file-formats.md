# Model file formats

This section targets developers and rock physics specialists responsible for (re)calibrating model parameter files.

Model files are used in three contexts: (1) the pressure sensitivity model, (2) the T-Matrix EXP variant, and (3) the
T-Matrix PETEC variant. All model files are in `pickle` format. Examples can be found in the test data sets for
`fmu-pem` in the project GitHub repository under
[`test/data/sim2seis/model`](https://github.com/equinor/fmu-pem/tree/main/tests/data/sim2seis/model).

## Pressure model files

Velocity sensitivity to effective pressure is implemented in the module
[`rock-physics-open`](https://github.com/equinor/rock-physics-open/blob/main/src/rock_physics_open/equinor_utilities/machine_learning_utilities/exponential_model.py)
. As the design supports generic model wrappers, the information is split between two `.pkl` files:

* Metadata file (model descriptor): keys model_type, pointer to core parameter file (nn_mod), input feature list, label
  variable and units, optional preprocessing artefact references.
* Parameter file: numerical calibration coefficients (a_factor, b_factor), valid pressure range (model_max_pressure),
  provenance (description). Briefly define a_factor and b_factor (exponential law coefficients for pressure sensitivity
  of velocity).

```python
import os, pickle
os.chdir(r'./tests/data/sim2seis/model')

print("Metadata file:")
with open('carbonate_pressure_model_vs_exp.pkl', 'rb') as fin:
    pres_vs_dict = pickle.load(fin)
for key, value in pres_vs_dict.items():
    print(f'{key}: {value}')

print("Parameter file:")
with open('vs_exp_model.pkl', 'rb') as fin:
    vs_exp_model_dict = pickle.load(fin)
for key, value in vs_exp_model_dict.items():
    print(f'{key}: {value}')
```
**Output**:
```text
Metadata file:
model_type: Exponential
nn_mod: vs_exp_model.pkl
scaler: None
ohe: None
label_var: VSX
label_units: m/s
feature_var: ['VSX', 'PEFF_in_situ', 'PEFF_depleted']

Parameter file:
a_factor: 0.09164501
b_factor: 8.23144402
model_max_pressure: 40.0
description: plug-based calibration data
```

## T-Matrix EXP model

The `EXP` type T-Matrix optimisation contains parameters for mineral properties of carbonate and shale, as well as
geometry, connectivity and anisotropic parameters. Note that the mineral properties are given as a fraction of the upper
bound in the optimisation process (values near 1.0 indicate convergence at the imposed cap). Calibration is performed in
[`rock-physics-open`](https://github.com/equinor/rock-physics-open/blob/main/src/rock_physics_open/t_matrix_models/t_matrix_parameter_optimisation_exp.py).

Parameter definition:
* f_ani: anisotropy (crack alignment / directional weighting) factor.
* f_con: connectivity (effective fluid communication / crack network) factor.
* alpha_opt: array of pore aspect ratios (e.g. alpha_opt[0] equant / stiff, alpha_opt[1] crack-like).
* v_opt: optimised porosity (or volume fraction parameter; clarify if it is total porosity vs a specific pore system).
* k_carb, mu_carb, rho_carb, etc.: normalised carbonate bulk modulus, shear modulus, density; similarly for shale (k_sh, mu_sh, rho_sh).
* opt_vec: concatenated optimisation vector in parameter order (state vector snapshot).

```python
import os, pickle
os.chdir(r'./tests/data/sim2seis/model')

with open('t_mat_params_exp.pkl', 'rb') as fin:
    exp_params = pickle.load(fin)
for key, value in exp_params.items():
    print(f'{key}: {value}')
```
**Output**:
```text
well_name: unknown
opt_ver: exp
f_ani: 0.1931401051312247
f_con: 0.0006487365851106763
alpha_opt: [0.50024826 0.07042638]
v_opt: 0.5016505733981023
k_carb: 0.6029058965366181
mu_carb: 0.7274039302389138
rho_carb: 0.9999862334411195
k_sh: 0.9999999999999999
mu_sh: 0.9999999999999999
rho_sh: 0.9090909090909092
opt_vec: [1.93140105e-01 6.48736585e-04 5.00248264e-01 7.04263774e-02
 5.01650573e-01 6.02905897e-01 7.27403930e-01 9.99986233e-01
 1.00000000e+00 1.00000000e+00 9.09090909e-01]
```

## T-Matrix PETEC model

The `PETEC` model type of T-Matrix contains fewer parameters than the `EXP` model, as in an appraisal or production
phase, more detailed information about minerals and fluids is available, and can be  applied directly in the modelling.
Optimisation code is located in
[`rock-physics-open`](https://github.com/equinor/rock-physics-open/blob/main/src/rock_physics_open/t_matrix_models/t_matrix_parameter_optimisation_min.py).

```python
import os, pickle
os.chdir(r'./tests/data/sim2seis/model')

with open('t_mat_params_petec.pkl', 'rb') as fin:
    exp_params = pickle.load(fin)
for key, value in exp_params.items():
    print(f'{key}: {value}')
```
**Output**:
```text
well_name: unknown
opt_ver: min
f_ani: 0.11140201779907752
f_con: 0.9999999998567579
alpha_opt: [0.5        0.06980489]
v_opt: 0.5000000000000977
opt_vec: [0.11140202 1.         0.5        0.06980489 0.5       ]
```
