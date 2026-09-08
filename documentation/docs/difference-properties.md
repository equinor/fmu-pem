# Calculate difference properties

`fmu-pem` is normally used for estimating 4D seismic response, and difference between simulator model time steps
can be more important than absolute values. In `fmu-sim2seis` workflow, the difference is calculated from absolute
values in a set of `Vp`, `Vs` and `Rho` parameters, ref. [Save results](./save-results.md). Additional difference
parameters can be generated in `fmu-pem` for QC or calibration purposes.

A section in the YAML configuration file specifies which parameters are selected for difference calculation, and
what kind of difference attributes should be estimated:

```yaml
# For 4D parameters: settings for which difference parameters to calculate
diff_calculation:
  - attribute: ai
    methods: [diffpercent, ratio]
  - attribute: si
    methods: [diffpercent, ratio]
  - attribute: vpvs
    methods: [ratio]
  - attribute: twtpp
    methods: [diff]
  - attribute: density
    methods: [diffpercent]
  - attribute: vp
    methods: [diffpercent]
  - attribute: vs
    methods: [diffpercent]
  - attribute: swat
    methods: [diff]
  - attribute: sgas
    methods: [diff]
  - attribute: pressure
    methods: [diff]
```

For convenience, it is possible to calculate differences of input parameter, as well, as in the example above for
`SWAT` and `SGAS`. The three difference attributes that can be selected, are `diff`, `diffpercent` and `ratio`.

In the FMU directory structure, the difference estimates are stored in `share/results/grids`.
