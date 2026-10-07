"""Build and export a statistics table for difference properties flagged for QC.

Properties are grouped by a discrete region selector (FIPNUM, or a region/zone
combination), with the statistics computed directly from the in-memory grid
arrays instead of re-reading named grid/log data.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import xtgeo

from fmu.dataio import ExportData

from .pem_config_validation import PemConfig
from .utils import filter_and_one_dim, pem_log

# Aggregations applied per group, named to match the statistics produced by
# fmu-tools' QCProperties
_STATISTICS = {
    "AVG": "mean",
    "STDDEV": "std",
    "P10": lambda x: np.percentile(x, 10),
    "P90": lambda x: np.percentile(x, 90),
    "MIN": "min",
    "MAX": "max",
    "COUNT": "count",
}


def build_qc_statistics_table(
    qc_table_props: dict[str, np.ma.MaskedArray],
    config: PemConfig,
) -> pd.DataFrame:
    """Build a statistics table for the selected difference properties.

    The statistics measurements (AVG, STDDEV, P10, ...) form the columns. Each row
    holds the statistics for one variable within one selector region, and every
    variable additionally gets a "Total" row aggregating all of its active cells.

    Args:
        qc_table_props: difference properties flagged for QC export, keyed by a
            name that identifies property, difference method and date pair
        config: PEM configuration providing the region selector used for grouping

    Returns:
        Dataframe with the statistics measurements as columns and one row per
        (variable, selector) group plus a (variable, "Total") row per variable
    """
    # selector_values holds one integer region code per cell; selector_names maps
    # each code to the region name used to label the output rows
    selector_values, selector_names = _get_groupby_selector(config=config)

    # Discard masked (inactive) cells and flatten all inputs to 1D, since only
    # active-cell values should contribute to the statistics
    _, selector_values, *values = filter_and_one_dim(
        selector_values, *qc_table_props.values()
    )

    # One column of region codes plus one column per QC variable
    data = pd.DataFrame(
        {"SELECTOR": selector_values}
        | dict(zip(qc_table_props.keys(), values, strict=True))
    )

    # Group once and reuse for every variable so the regions are only indexed once
    by_region = data.groupby("SELECTOR")

    tables = []
    for variable in qc_table_props:
        # Statistics per region, with the numeric code replaced by its region name
        per_region = by_region[variable].agg(**_STATISTICS)
        per_region.insert(0, "SELECTOR", per_region.index.map(selector_names))

        # A single "Total" row aggregating every active cell of the variable
        total = pd.Series(
            {name: data[variable].agg(func) for name, func in _STATISTICS.items()}
        )
        total["SELECTOR"] = "Total"

        table = pd.concat([per_region, total.to_frame().T], ignore_index=True)
        table.insert(0, "PROPERTY", variable)
        tables.append(table)

    return pd.concat(tables, ignore_index=True)


def export_qc_statistics_table(
    qc_dataframe: pd.DataFrame,
    qc_tables_file: Path,
) -> None:
    """Export the QC statistics table as a CSV file using fmu-dataio.

    fmu-dataio resolves the correct FMU run/case ``share/results/tables``
    directory automatically, so no explicit output path is needed here.

    Args:
        qc_dataframe: statistics table produced by build_qc_statistics_table
        qc_tables_file: file name (stem used as the fmu-dataio object name)
    """
    export_data = ExportData(
        name=qc_tables_file.stem,
        content="property",
        content_metadata={"attribute": "statistics"},
        table_index=["PROPERTY", "SELECTOR"],
    )
    out_path = export_data.export(qc_dataframe)
    pem_log(f"QC statistics table exported to {out_path}")


def _get_groupby_selector(
    config: PemConfig,
) -> tuple[np.ma.MaskedArray, dict[int, str]]:
    """Return per-cell region codes and a mapping from each code to a region name.

    The codes are used to group the statistics; the mapping turns the numeric code
    of each row into a human-readable region name.
    """
    if config.difference_properties.group_statistics == "fipnum":
        grid = xtgeo.grid_from_file(
            config.simulator_files.rel_path_simgrid / config.simulator_files.egrid_file
        )
        region_zone = xtgeo.gridproperties_from_file(
            property_file=(
                config.simulator_files.rel_path_simgrid
                / config.simulator_files.init_property_file
            ),
            fformat="init",
            names=["FIPNUM"],
            grid=grid,
        )
        selector_values = region_zone["FIPNUM"].values
        selector_names = region_zone["FIPNUM"].codes
    else:
        statistics_dir = config.difference_properties.statistics_grid_dir
        zones = xtgeo.gridproperty_from_file(
            statistics_dir / config.difference_properties.statistics_zone_file
        )
        zone_values = zones.values

        regions = xtgeo.gridproperty_from_file(
            statistics_dir / config.difference_properties.statistics_region_file
        )
        region_values = regions.values

        # Combine region and zone into a single code; the multiplier guarantees a
        # unique code for every (region, zone) pair
        zone_span = int(np.ma.max(zone_values)) + 1
        selector_values = region_values * zone_span + zone_values
        selector_names = {
            region_code * zone_span + zone_code: f"{region_name}_{zone_name}"
            for region_code, region_name in regions.codes.items()
            for zone_code, zone_name in zones.codes.items()
        }

    return selector_values, selector_names
