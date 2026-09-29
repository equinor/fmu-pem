import numpy as np
import pandas as pd
import pytest

from fmu.pem.pem_utilities.pem_class_definitions import SimInitProperties
from fmu.pem.pem_utilities.qc_statistics import build_qc_statistics_table


def _masked(values: list[float], mask: list[bool] | None = None) -> np.ma.MaskedArray:
    return np.ma.MaskedArray(
        np.array(values, dtype=float), mask=mask or [False] * len(values)
    )


def _init_props(
    eqlnum: list[int], fipzon: list[int], mask: list[bool] | None = None
) -> SimInitProperties:
    # poro/depth are required but unused by build_qc_statistics_table
    dummy = _masked([0.0] * len(eqlnum))
    return SimInitProperties(
        poro=dummy,
        depth=dummy,
        eqlnum=_masked(eqlnum, mask),
        fipzon=_masked(fipzon, mask),
    )


def test_build_qc_statistics_table_computes_expected_statistics():
    # A 2x2 EQLNUM/FIPZON grid with one value per cell: 1, 2, 3, 4
    init_props = _init_props(eqlnum=[1, 1, 2, 2], fipzon=[1, 2, 1, 2])
    qc_table_props = {"PORODIFF_20200101_20180101": _masked([1.0, 2.0, 3.0, 4.0])}

    result = build_qc_statistics_table(qc_table_props, init_props)

    def row(eqlnum, fipzon, avg, stddev, p10, p90, vmin, vmax, count):
        return {
            "PROPERTY": "PORODIFF_20200101_20180101",
            "EQLNUM": eqlnum,
            "FIPZON": fipzon,
            "AVG": avg,
            "STDDEV": stddev,
            "P10": p10,
            "P90": p90,
            "MIN": vmin,
            "MAX": vmax,
            "COUNT": count,
        }

    expected = pd.DataFrame(
        [
            # full (EQLNUM, FIPZON) split: one value per group
            row(1, 1, 1.0, np.nan, 1.0, 1.0, 1.0, 1.0, 1),
            row(1, 2, 2.0, np.nan, 2.0, 2.0, 2.0, 2.0, 1),
            row(2, 1, 3.0, np.nan, 3.0, 3.0, 3.0, 3.0, 1),
            row(2, 2, 4.0, np.nan, 4.0, 4.0, 4.0, 4.0, 1),
            # per-EQLNUM totals (summed over FIPZON)
            row(1, "Total", 1.5, 0.7071067811865476, 1.1, 1.9, 1.0, 2.0, 2),
            row(2, "Total", 3.5, 0.7071067811865476, 3.1, 3.9, 3.0, 4.0, 2),
            # per-FIPZON totals (summed over EQLNUM)
            row("Total", 1, 2.0, 1.4142135623730951, 1.2, 2.8, 1.0, 3.0, 2),
            row("Total", 2, 3.0, 1.4142135623730951, 2.2, 3.8, 2.0, 4.0, 2),
            # grand total across all EQLNUM and FIPZON
            row("Total", "Total", 2.5, 1.2909944487358056, 1.3, 3.7, 1.0, 4.0, 4),
        ]
    )

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected.reset_index(drop=True)
    )


def test_build_qc_statistics_table_excludes_masked_cells():
    init_props = _init_props(eqlnum=[1, 1, 2, 2], fipzon=[1, 2, 1, 2])
    # Mask the (EQLNUM=2, FIPZON=2) cell out of the difference property only;
    # filter_and_one_dim combines masks across all inputs, so it is still dropped
    qc_table_props = {
        "PORODIFF": _masked([1.0, 2.0, 3.0, 4.0], mask=[False, False, False, True])
    }

    result = build_qc_statistics_table(qc_table_props, init_props)

    # The masked cell's group must be absent entirely
    assert not ((result["EQLNUM"] == 2) & (result["FIPZON"] == 2)).any()

    grand_total = result[(result["EQLNUM"] == "Total") & (result["FIPZON"] == "Total")]
    assert grand_total["COUNT"].iloc[0] == 3
    assert grand_total["AVG"].iloc[0] == pytest.approx(2.0)

    eqlnum_2_total = result[(result["EQLNUM"] == 2) & (result["FIPZON"] == "Total")]
    assert eqlnum_2_total["COUNT"].iloc[0] == 1
    assert eqlnum_2_total["AVG"].iloc[0] == pytest.approx(3.0)


def test_build_qc_statistics_table_keeps_separate_date_pair_properties():
    init_props = _init_props(eqlnum=[1, 2], fipzon=[1, 1])
    # Two difference properties for different date pairs must not overwrite
    # each other, even though they cover the same EQLNUM/FIPZON cells
    qc_table_props = {
        "AIRATIO_20190101_20180101": _masked([10.0, 20.0]),
        "AIRATIO_20200101_20180101": _masked([100.0, 200.0]),
    }

    result = build_qc_statistics_table(qc_table_props, init_props)

    assert set(result["PROPERTY"]) == set(qc_table_props)
    first = result[
        (result["PROPERTY"] == "AIRATIO_20190101_20180101")
        & (result["EQLNUM"] == "Total")
        & (result["FIPZON"] == "Total")
    ]
    second = result[
        (result["PROPERTY"] == "AIRATIO_20200101_20180101")
        & (result["EQLNUM"] == "Total")
        & (result["FIPZON"] == "Total")
    ]
    assert first["AVG"].iloc[0] == pytest.approx(15.0)
    assert second["AVG"].iloc[0] == pytest.approx(150.0)


@pytest.mark.parametrize("missing", ["eqlnum", "fipzon"])
def test_build_qc_statistics_table_requires_eqlnum_and_fipzon(missing):
    init_props = _init_props(eqlnum=[1, 2], fipzon=[1, 2])
    setattr(init_props, missing, None)
    qc_table_props = {"PORODIFF": _masked([1.0, 2.0])}

    with pytest.raises(ValueError, match="EQLNUM and FIPZON"):
        build_qc_statistics_table(qc_table_props, init_props)
