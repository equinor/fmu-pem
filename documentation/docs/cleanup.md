# Cleaning up PEM results

A full PEM run can write a large number of grids to each realisation's
`share/results/grids` directory: the final elastic and difference properties, but
also – when enabled – many intermediate/QC grids (mineral, fluid, dry-rock,
pressure, adjusted-porosity, below-bubble-point, …). Once a run has been
quality-checked, most of these are no longer needed and take up considerable
disk space.

The `pem_cleanup` tool removes selected categories of result files, either from a
single run or from a whole ensemble. It is available both as a command-line
program and as a pre-installed ERT forward model (`PEM_CLEANUP`).

## What gets removed

Each grid file is classified, from its file name, into one of four categories:

| Category       | Examples                                                                 |
| -------------- | ------------------------------------------------------------------------ |
| `intermediate` | `simgrid--bulk_modulus_mineral.roff`, `simgrid--pressure--20180101.roff` |
| `elastic`      | `simgrid--vp--20180101.roff`, `simgrid--density--20180101.roff`          |
| `difference`   | `simgrid--sidiffpercent--20180701_20180101.roff`                         |
| `grid`         | `simgrid.roff` (the bare simulation grid)                                |

You select which categories to delete. The special value `all` deletes everything
that is recognised. `grid` is a *classification* only – it is not selectable on its
own (see the warning below).

::: warning Protecting the simulation grid
The bare grid (`grid`) is only removed when **everything** is removed – that is,
when you pass `all`. It cannot be selected on its own: `grid` is not a valid value
for `--save_type_list`, because the elastic/difference/intermediate parameter grids
are unusable without the grid geometry they refer to. Requesting only some property
categories therefore never deletes the grid.
Files that are not recognised as PEM output (e.g. notes, logs) are always left
untouched.
:::

## Command-line usage

```shell
> # Show all call arguments
> pem_cleanup --help
```

| Flag                     | Required | Default     | Description                                                                    |
| ------------------------ | -------- | ----------- | ------------------------------------------------------------------------------ |
| `-g`, `--grid_dir`       | yes      | –           | Directory to clean (see [Which directory](#which-directory-to-point-at) below) |
| `-s`, `--save_type_list` | yes      | –           | One or more categories: `intermediate`, `elastic`, `difference`, `all`         |
| `-i`, `--is_ensemble`    | no       | `false`     | Treat `--grid_dir` as the top of an ensemble                                   |
| `-p`, `--prefix`         | no       | `simgrid`   | Grid-name prefix of the files to consider                                      |
| `-e`, `--extension`      | no       | `.roff`     | File extension of the files to consider                                        |

```shell
> # Go to the top of the project structure
> cd /project/<my project>/resmod/ff/users/26.0.0

> # Remove only the intermediate/QC grids from one run
> pem_cleanup -g ./share/results/grids -s intermediate

> # Remove intermediate and difference grids (keeps elastic and the grid itself)
> pem_cleanup -g ./share/results/grids -s intermediate difference

> # Remove everything PEM produced, including the grid
> pem_cleanup -g ./share/results/grids -s all

> # Clean every realisation/iteration of an ensemble in one call
> # (point at the ensemble top that directly contains realization-<n>/iter-<m>)
> pem_cleanup -g /scratch/fmu/<user>/<case> -i true -s all
```

### Which directory to point at

`pem_cleanup` deliberately accepts only a small, well-defined set of locations;
no upward or recursive search is performed, so an unrelated parent directory can
never be matched.

- **Single run** (`--is_ensemble false`, the default): `--grid_dir` must be either
  - the `share/results/grids` directory itself, or
  - the FMU run root that contains it directly.
- **Ensemble** (`--is_ensemble true`): `--grid_dir` must be the top of the
  ensemble, i.e. a directory that directly contains `realization-<n>/iter-<m>`
  subdirectories. Every realisation/iteration's `share/results/grids` directory is
  then processed.

If the directory does not match the requested run type, the tool stops with an
error rather than risk deleting the wrong files.

## ERT configuration

`PEM_CLEANUP` is a pre-installed forward model and is typically added after the
`PEM` step (and after any QC steps you want to run on the intermediate grids).

````ert
-- Define your variables:
DEFINE <GRID_DIR> <RUNPATH>/share/results/grids
DEFINE <SAVE_TYPES> intermediate
DEFINE <GRID_PREFIX> simgrid
DEFINE <GRID_EXTENSION> .roff

-- Run the pre-installed ERT forward model:
FORWARD_MODEL PEM_CLEANUP(<GRID_DIR>=<GRID_DIR>, <SAVE_TYPE_LIST>=<SAVE_TYPES>, <PREFIX>=<GRID_PREFIX>, <EXTENSION>=<GRID_EXTENSION>)
````
