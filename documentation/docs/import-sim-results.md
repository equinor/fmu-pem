# Import reservoir simulator results

Both static and dynamic reservoir simulator results are used in the `pem`. They are complemented with some results from
the geomodel, as described below. Capital letter names below refer to the parameter names in `eclipse` models, which
is the main reservoir simulator tool within Equinor. `OPM FLOW` is an alternative, and it is compatible with `eclipse`
parameter names.

## Directory and file names for result files

The directory name for the result files from the reservoir simulator is fixed within the FMU directory structure. The
file names are also fixed, but they are links/pointers to the actual results from `eclipse`.
The directory and file names used by `pem` are shown below:

```yaml
rel_path_simgrid: ../../sim2seis/input/pem
```

```shell
> cd ../../sim2seis/input/pem
> ls -l ECLIPSE*
lrwxrwxrwx 1 hfle fmu        36 Jun 26  2024 ECLIPSE.EGRID -> ../../../eclipse/model/ECLIPSE.EGRID
lrwxrwxrwx 1 hfle fmu        35 Jun 26  2024 ECLIPSE.INIT -> ../../../eclipse/model/ECLIPSE.INIT
lrwxrwxrwx 1 hfle fmu        36 Jun 26  2024 ECLIPSE.UNRST -> ../../../eclipse/model/ECLIPSE.UNRST
>
```

## Static results

There are only two static results from the reservoir simulator model which are used in `pem`: **PORO** and **DEPTH**.
Earlier, **NTG** was also used, but we now advise using volume fractions from the geomodel. Static results are
found in the **.INIT** file of the reservoir simulator.

#### Volume fraction files

As mentioned above, `pem` is not based on using the **NTG** parameter from the reservoir simulator, as it is often
a binary parameter, and does not reflect variations in shale fraction in the Geomodel. Additionally, to capture
variations in effective mineral properties, more volume fractions may be required, such as coal or calcite in a clastic
case, and calcite, dolomite, mud etc. in a carbonate case. Volume fractions should be exported from the Geomodel with
the same grid resolution as the reservoir simulator grid, and in the **.roff** format.

```yaml
  volume_fractions:
    rel_path_fractions: ../../sim2seis/input/pem
    fractions_prop_file_names: [simgrid--vsh_pem.roff, ]
    fractions_are_mineral_fraction: False  # volume fractions, not mineral fractions are assumed by default
  fraction_names: [vsh_pem, ]  # matching the names of properties in the fractions properties file
  fraction_minerals: [shale, ] # each of the minerals must be defined with bulk modulus, shear modulus and density
  shale_fractions: [vsh_pem, ] # define the non-reservoir fraction(s)
  complement: quartz  # if not all fractions add up to 1.0
```

#### Volume fractions to mineral fractions

It is important to know the definition of volume fractions. The standard definition in petrophysics is that volume
fractions and effective porosity comprise the bulk volume. This definition is the default value in `pem`.

In a case where only VSH is defined, and we wish to calculate VSST, we do it simply by:

$$ VSST = 1.0 - VSH - POR $$

However, when effective mineral properties are calculated, the volume fractions must be transformed into mineral
fractions, i.e. fractions of the rock matrix:

$$ FRAC_SST = VSST / (1.0 - POR); FRAC_SH = VSH / (1.0 - POR) $$

**NB!** It is possible to override the volume fraction assumption by ticking **on** the option for
`fractions_are_mineral_fraction` in the parameter interface or setting it to *true* in the YAML file. In that case the
fraction of sandstone in the example above becomes:

$$ FRAC_SST = 1.0 - FRAC_SH$$

## Dynamic results

Dynamic results for each time step in the **.UNRST** file are used to calculate fluid properties and other properties
that depend on pressure.

```python
# TEMP will only be available for eclipse-300
RST_PROPS = ["SWAT", "SGAS", "SOIL", "RS", "RV", "PRESSURE", "SALT", "TEMP"]
```

Salinity may not be available in the UNRST file, and in that case, a constant value  must be set
in the YAML file. Temperature in normally also kept constant. RS (ratio of solid) and RV (ratio of vapour) are used
for calculating oil properties and condensate properties, respectively. If both are present in the UNRST file, it may
be necessary to state if the fluid model should include condensate calculation. Beware that condensate model is not
part of the open-source foundation for `pem`; a proprietary model is needed.

```yaml
  calculate_condensate: False
```
