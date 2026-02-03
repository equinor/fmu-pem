# Effective pressure

The matrix of porous rocks will be affected by the effective stress in terms of porosity, permeability and elastic
moduli. In this context, we simplify it to regard elastic moduli to be stress sensitive, and to keep porosity
constant. `fmu-pem` does not include any modelling of permeability.

Although effective pressure is the commonly used term, it is somewhat inaccurate, and effective stress is more correct.
In the `fmu-pem` case, we simplify the stress tensor to an isotropic pressure. To estimate effective pressure, we need to
know the overburden pressure and the formation pressure at all grid cells. Formation pressure is provided by the
reservoir simulator model, but overburden pressure is not available there. The best source for overburden pressure is
provided by drilling or operational geology disciplines, and for most fields, it will be a single one-dimensional model,
or in some cases one model per structure in the field. The relationship between overburden, formation and effective
pressures is given as:

$$P_{eff} = P_{ob} - \alpha \cdot P_f$$

where $\alpha$ is the formation factor, also known as the Biot coefficient.

## Variation with time

As formation pressure is reduced by depletion, the effective pressure will vary with time. In `fmu-pem`, the effective
pressure is estimated for each time step in the reservoir simulator **.UNRST** file.

## Implementation in `fmu-pem`

Two versions of estimation of effective pressure are included in `fmu-pem`: either a constant overburden pressure at
top reservoir, or a linear depth trend. Formation factor is set to 1.0. These are the settings in the YAML config file:

```yaml
# Overburden pressure may be set to a constant, but the estimation is improved by using a depth trend
# Unit is Pa
pressure:
  type: trend
  intercept: 20.0e6
  gradient: 9174.3
#  type: constant
#  value: 50000000.0
```
