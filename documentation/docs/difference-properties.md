# Calculate difference properties

`fmu-pem` is normally used for estimating 4D seismic response, and difference between simulator model time steps
can be more important than absolute values. In `fmu-sim2seis` workflow, the difference is calculated from absolute
values in a set of `Vp`, `Vs` and `Rho` parameters, ref. [Save results](./save-results.md). Additional difference
parameters can be generated in `fmu-pem` for QC or calibration purposes.

A section in the YAML configuration file specifies which parameters are selected for difference calculation, and
what kind of difference attributes should be estimated:

```yaml
# For 4D parameters: settings for which difference parameters to calculate
difference_properties:
  group_statistics: region_zone
  diff_calculation:
    - attribute: ai
      methods: [diffpercent, ratio]
      qc_table: True
    - attribute: si
      methods: [diffpercent, ratio]
    - attribute: vpvs
      methods: [ratio]
    - attribute: twtpp
      methods: [diff]
      qc_table: True
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

## QC statistics tables

For any `diff_calculation` entry, setting `qc_table: true` (as for `ai` and `twtpp` in the example above) additionally
exports statistics for that difference attribute and its selected methods to a `.CSV` file.

Statistics (`AVG`, `STDDEV`, `P10`, `P90`, `MIN`, `MAX`, `COUNT`) are computed per active cell, grouped by a discrete
region selector chosen with `group_statistics`: either `fipnum` (regions from the `FIPNUM` parameter in the reservoir
simulator **.INIT** file, the default) or `region_zone` (regions from ROFF zone and region parameters). In addition to
the per-region groups, a "Total" row aggregating the whole grid is added for each attribute/method/date-pair.

All difference attributes flagged with `qc_table: true` are collected into a single table, with one row group per
attribute/method/date-pair combination. The output file name is set with `qc_tables_file_name` (default
`grid_property_statistics_pemgrid`), and the table is exported with `fmu-dataio` to `share/results/tables`:

```yaml
difference_properties:
  qc_tables_file_name: grid_property_statistics_pemgrid
```
