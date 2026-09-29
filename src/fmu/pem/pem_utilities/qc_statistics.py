"""Build and export a statistics table for difference properties flagged for QC.

Properties are grouped by the discrete EQLNUM and FIPZON regions, mirroring the
grouping used by the legacy RMS ``QCProperties``-based export script, but computed
directly from the in-memory grid arrays instead of re-reading named grid/log data.
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from fmu.dataio import ExportData

from .pem_class_definitions import SimInitProperties
from .utils import filter_and_one_dim, pem_log

# Discrete regions statistics are grouped by, in fixed output column order
# ToDo: evaluate if _SELECTORS should be input parameters
_SELECTORS = ["EQLNUM", "FIPZON"]

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


def _selector_combinations(selectors: list[str]) -> list[list[str]]:
    """All non-empty subsets of selectors, largest first, plus the empty subset.

    Used to compute statistics for every selector combination (e.g. per EQLNUM
    across all FIPZON) as well as a grand total across all selectors.
    """
    combos = [
        list(combo)
        for size in range(len(selectors), 0, -1)
        for combo in combinations(selectors, size)
    ]
    combos.append([])
    return combos


def build_qc_statistics_table(
    qc_table_props: dict[str, np.ma.MaskedArray],
    init_props: SimInitProperties,
) -> pd.DataFrame:
    """Build a long-format statistics table for the selected difference properties.

    In addition to statistics per (PROPERTY, EQLNUM, FIPZON) combination, "Total"
    rows are added for each selector subset (e.g. per EQLNUM summed over all
    FIPZON) and a grand total across all EQLNUM and FIPZON, mirroring the
    behaviour of fmu-tools' QCProperties with selector_combos enabled.

    Args:
        qc_table_props: difference properties flagged for QC export, keyed by a
            name that identifies property, difference method and date pair
        init_props: reservoir simulation INIT properties, providing the EQLNUM and
            FIPZON region properties used to group the statistics

    Returns:
        Dataframe with one row per (PROPERTY, EQLNUM, FIPZON) statistics group,
        where EQLNUM and/or FIPZON is "Total" for the aggregated rows
    """
    if init_props.eqlnum is None or init_props.fipzon is None:
        raise ValueError(
            f"{__file__}: EQLNUM and FIPZON must be available in the reservoir "
            f"simulation INIT properties to group QC statistics"
        )

    # Discard masked (inactive) cells and flatten all inputs to 1D before building
    # the dataframe, since only active-cell values should contribute to statistics
    _, eqlnum, fipzon, *values = filter_and_one_dim(
        init_props.eqlnum, init_props.fipzon, *qc_table_props.values()
    )
    wide_table = pd.DataFrame(
        {"EQLNUM": eqlnum, "FIPZON": fipzon}
        | dict(zip(qc_table_props.keys(), values, strict=True))
    )

    # Reshape to long format so all difference properties can be aggregated with a
    # single groupby, then compute statistics per property/region combination
    long_table = wide_table.melt(
        id_vars=_SELECTORS, var_name="PROPERTY", value_name="VALUE"
    )
    tables = [
        long_table.groupby(["PROPERTY", *combo])["VALUE"]
        .agg(**_STATISTICS)
        .reset_index()
        for combo in _selector_combinations(_SELECTORS)
    ]
    # Selectors missing from a given combo (e.g. FIPZON when grouping by EQLNUM
    # only) become NaN on concat; label those aggregated rows "Total"
    result = pd.concat(tables, ignore_index=True)
    result[_SELECTORS] = result[_SELECTORS].fillna("Total")
    # Concat with NaN upcasts the selector columns to float; restore plain ints
    # for the actual region codes so e.g. "1" isn't shown as "1.0" in the CSV
    for selector in _SELECTORS:
        result[selector] = result[selector].apply(
            lambda v: v if v == "Total" else int(v)
        )
    return result[["PROPERTY", *_SELECTORS, *_STATISTICS]]


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
        table_index=["PROPERTY", *_SELECTORS],
    )
    out_path = export_data.export(qc_dataframe)
    pem_log(f"QC statistics table exported to {out_path}")
