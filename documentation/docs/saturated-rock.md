# Estimation of properties for saturated rocks

Estimating the elastic properties of saturated rocks is the final stage in rock physics modelling within `fmu-pem`.
Several models are available. Historically, PEM workflows for clastic rocks separated the task into (1) estimating dry
frame properties and (2) applying fluid substitution. `fmu-pem` is extended to carbonate rocks, and the inclusion-based
T-Matrix model performs both steps in a single calculation; for consistency the workflow ensures both dry and
saturated responses are produced for every selected model. For regression-based and patchy or friable cement models, the
dry frame and saturation steps remain sequential. Both steps are executed automatically when either model is selected,
using Gassmann fluid substitution for the saturation step (fluid substitution).

As fluid saturation and pore pressure change during production, it is necessary to calculate the properties of
saturated rocks for all selected time steps in the reservoir simulator.

## Model calibration
This section applies to internal use of `fmu-pem` within Equinor.

It is recommended to calibrate rock physics models in RokDoc. Both `RokDoc-plugins` and `fmu-pem` use the same
rock physics libraries, so parameters determined in RokDoc can be applied directly in `fmu-pem`. Calibration is
performed using available well log data, and RokDoc’s interactive features and graphics assist users in selecting
suitable parameters for each case.

## Regression models

Where a reasonable trend exists between porosity and elastic properties—either Vp and Vs, or bulk and shear modulus (K
and Mu)—the modelling of **dry rock properties** for each lithology can be simplified using a polynomial function:

$$
V_p = a_1 + a_2 \phi + a_3 \phi^2 + a_4 \phi^3 + ... + a_n \phi^(n-1)
$$

In the current version of `fmu-pem`, regression models are limited to two phases/minerals: sand and shale. Users may
choose regression models for Vp and Vs, or for K and Mu. Density is typically determined by volume fractions and the
mineral density of each fraction, but it can also be estimated using a polynomial function. The polynomial coefficients
must be provided by the user for each regression model. The degree of the polynomial is determined by the number of
coefficients; for example, <span>[a_1, a_2]</span> produces a first-degree polynomial. Pressure sensitivity is not
directly included in the regression model. A separate pressure sensitivity model for dry rocks is applied prior to
the fluid substitution or saturation step.

## Patchy cement model and friable model

Patchy cement and friable models are contact theory models for clastic rocks, typically used for sandstones. Both
describe the rock as a collection of grains in contact. If grain contacts are cemented, the framework becomes stiffer
and the friable model is no longer valid. A fully cemented model, where all grain contacts are cemented, is
theoretically insensitive to pressure changes. In most sandstones with hydrocarbon accumulations, some sensitivity to
pressure changes remains, even if in situ temperature is high enough for quartz dissolution and precipitation. In such
cases, the patchy cement model is appropriate, covering scenarios where some grain contacts are cemented and others are
not. Calibration to observed logs determines the degree of cementation and, consequently, the sensitivity to pressure
changes. Further documentation is available in the references below.

[1] Mavko, G., Mukerji, T., & Dvorkin, J. (2020). *The Rock Physics Handbook* (3rd ed.). Cambridge University Press.

[2] Avseth, P., Mukerji, T., & Mavko, G. (2005). *Quantitative Seismic Interpretation*. Cambridge University Press.

[3] Avseth, P. & Skjei, N. (). *Rock physics modeling of static and dynamic reservoir properties - A heuristic
approach for cemented sandstone reservoirs*. The Leading Edge, January 2011.

### Parameters for patchy cement model

Parameters for the friable model are a subset of those used in the patchy cement model. Most parameters have default
values, which may not be suitable for all cases. The example below shows default values. In the `fmu-pem` user interface,
each parameter is described.

```yaml
cement_fraction: 0.04  # must be lower than the upper bound cement fraction (0.1)
critical_porosity: 0.4  # porosity when the sand grains fall out of suspension
shear_reduction: 0.5  # parameter that affects the tangential friction between grains
coordination_number_function: PorBased  # coordination number is the number of grain contacts per grain, assumed
                                        # to be inversely correlated to porosity
```

Two parameters are not accessible: upper_bound_cement_fraction and lower_bound_effective_pressure. The upper bound for
cement fraction ensures the model remains within a sensible range. The constant cement model, part of the patchy cement
model, is only valid within certain limits; high cement fractions yield erroneous results. For highly cemented
sandstones, an inclusion model such as T-Matrix is more appropriate. The lower bound for effective pressure is based on
experience from partially cemented cases, but is not a numerical constraint, unlike the upper bound for cement fraction.

## T-Matrix model

The T‑Matrix model is an inclusion-based effective medium approach. The rock framework is treated as a homogeneous
elastic background, while pores, fractures and softer patches are represented as ellipsoidal inclusions embedded in this
background. This formulation is appropriate for rocks with frameworks stiffer than partially cemented sandstones (e.g.
many carbonates), and has also been applied to unconventional reservoirs (e.g. organic-rich shales) and some tight
sandstones. The current implementation of T-Matrix does not include any pressure sensitivity. An additional pressure
sensitivity step is added as post-processing.

Key concepts:
* Geometry: Each inclusion is idealised as an ellipsoid defined by a single aspect ratio (shortest axis / longest axis).
A spherical pore has aspect ratio 1.0; a thin fracture may have an aspect ratio ≪ 1 (e.g. 1e-4).
* Compliance effect: Lower aspect ratios (flatter inclusions) increase the compliance (soften the aggregate response)
more than higher aspect ratios.
* Practical limits: The model becomes unreliable if a large fraction of total porosity is assigned extremely flat (very
low aspect ratio) inclusions. In practice, most porosity is assigned aspect ratios ≥ 0.5, with a controlled fraction at
lower values to capture fractures or crack-like pores.
* Parameter richness: Required inputs include background (frame) elastic moduli, inclusion aspect ratios, inclusion volume
fractions, and inclusion (or pore fluid) elastic properties. Some parameters cannot be constrained from conventional
well logs alone and may need core, CT scan, petrographic or laboratory measurements.
* Optimisation workflow: In RokDoc-plugins two usage contexts are distinguished:
  * Exploration (EXP): Sparse constraints; more parameters solved via optimisation.
  * Appraisal / production (PETEC): Better mineralogical, saturation and fluid property control; fewer free parameters.
  Resulting optimised parameter files can be supplied directly to `fmu-pem`.

In practice:
* Select parameters that can be fixed from data (e.g. mineral frame moduli, fluid properties). This is common to all
saturated rock models.
* Assign geologically plausible aspect ratio populations (fractures vs equant pores).
* Use optimisation to solve for poorly constrained fractions or aspect ratios within reasonable bounds.
* Leave truly insensitive parameters at default values after sensitivity screening.

Limitations:
* Assumes dilute or moderately interacting inclusions; extreme crack densities reduce accuracy.
* Single aspect ratio per inclusion population simplifies reality and may under-represent multimodal pore systems.
* Strong anisotropy from aligned fractures is only approximated unless explicit orientational distributions are
incorporated.

#### Literature

The theory for T-Matrix can be found in the papers and in the references therein:

[1] Agersborg, R., Jakobsen, M., Ruud, B.O. and Johansen, T. A. 2007. Effects of pore fluid pressure on the seismic
response of a fractured carbonate reservoir. Stud. Geophys. Geod., 51, 89-118.

[2] Agersborg, R., Johansen, T. A. and Ruud, B.O. 2008. Modelling reflection signatures of pore fluids and dual porosity
in carbonate reservoirs. Journal of Seismic Exploration, 17(1), 63-83.

[3] Agersborg, R., Johansen, T. A., Jakobsen, M., Sothcott, J. and Best, A. 2008. Effect of fluids and dual-pores
systems on pressure-dependent velocities and attenuation in carbonates, Geophysics, 73, No. 5, N35-N47.

[4] Agersborg, R., Johansen, T. A., and Jakobsen, M. 2009. Velocity variations in carbonate rocks due to dual porosity
and wave-induced fluid flow. Geophysical Prospecting, 57, 81-98.

All of the papers and a extended explanations of the involved equations can be found in Agersborg (2007), phd thesis:
[Agersborg (2007), PhD thesis](https://bora.uib.no/bora-xmlui/handle/1956/2422)
