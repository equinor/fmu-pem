# Save results

The default is to save results to disk, mostly in `.roff` format. For historical reasons, the main
results from `fmu-pem` are saved in `.grdecl` format for use in `fmu-sim2seis`. For QC purposes, intermediate
results, which are effective properties for minerals and fluids, can also be saved. All `.roff` files are saved to
`share/results/grids`

```yaml
# Settings for saving results
results:
  save_results_to_disk: True
  save_intermediate_results: True
```

An example on QC of fluid properties, is comparison between effective fluid density as estimated from `fmu-pem` and
from the reservoir simulator. The estimates should be close, as shown in [Figure 1](figure-1-fluid-density)

<img src="./images/fluid_density_comparison.png">

<span id="figure-1-fluid-density"><strong>Figure 1:</strong> Estimate of fluid density from simulator model (x-axis) and PEM (y-axis) for a selected time step. With settings for
either dry gas, wet gas or a compositional model, simulator model and PEM are in agreement.</span>
<br><br>
