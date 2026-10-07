from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import fmu.pem.pem_utilities.qc_statistics as qc_mod
from fmu.pem.pem_utilities.qc_statistics import (
    _get_groupby_selector,
    build_qc_statistics_table,
)


def _masked(values: list[float], mask: list[bool] | None = None) -> np.ma.MaskedArray:
    return np.ma.MaskedArray(
        np.array(values, dtype=float), mask=mask or [False] * len(values)
    )


def _codes(values: list[int], mask: list[bool] | None = None) -> np.ma.MaskedArray:
    return np.ma.MaskedArray(
        np.array(values, dtype=int), mask=mask or [False] * len(values)
    )


def _patch_selector(monkeypatch, selector_values, selector_names) -> None:
    # build_qc_statistics_table reads the region selector from grid files via
    # _get_groupby_selector; replace it with fixed arrays to test aggregation only
    monkeypatch.setattr(
        qc_mod,
        "_get_groupby_selector",
        lambda config: (selector_values, selector_names),
    )


def test_build_qc_statistics_table_computes_expected_statistics(monkeypatch):
    # Two regions of two cells each, labelled by name via the code -> name mapping
    _patch_selector(monkeypatch, _codes([1, 1, 2, 2]), {1: "RegionA", 2: "RegionB"})
    qc_table_props = {"PORODIFF_20200101_20180101": _masked([1.0, 2.0, 3.0, 4.0])}

    result = build_qc_statistics_table(qc_table_props, config=None)

    def row(selector, avg, stddev, p10, p90, vmin, vmax, count):
        return {
            "PROPERTY": "PORODIFF_20200101_20180101",
            "SELECTOR": selector,
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
            row("RegionA", 1.5, 0.7071067811865476, 1.1, 1.9, 1.0, 2.0, 2),
            row("RegionB", 3.5, 0.7071067811865476, 3.1, 3.9, 3.0, 4.0, 2),
            row("Total", 2.5, 1.2909944487358056, 1.3, 3.7, 1.0, 4.0, 4),
        ]
    )

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected, check_dtype=False
    )


def test_build_qc_statistics_table_excludes_masked_cells(monkeypatch):
    _patch_selector(monkeypatch, _codes([1, 1, 2, 2]), {1: "RegionA", 2: "RegionB"})
    # Mask the last cell (RegionB) on the property; that cell must be dropped
    qc_table_props = {
        "PORODIFF": _masked([1.0, 2.0, 3.0, 4.0], mask=[False, False, False, True])
    }

    result = build_qc_statistics_table(qc_table_props, config=None)

    total = result[result["SELECTOR"] == "Total"]
    assert total["COUNT"].iloc[0] == 3
    assert total["AVG"].iloc[0] == pytest.approx(2.0)

    region_b = result[result["SELECTOR"] == "RegionB"]
    assert region_b["COUNT"].iloc[0] == 1
    assert region_b["AVG"].iloc[0] == pytest.approx(3.0)


def test_build_qc_statistics_table_masks_each_property_independently(monkeypatch):
    _patch_selector(monkeypatch, _codes([1, 2]), {1: "RegionA", 2: "RegionB"})
    # A cell masked only in one property must not be dropped from the other
    # property's statistics
    qc_table_props = {
        "A": _masked([1.0, 2.0], mask=[False, True]),
        "B": _masked([10.0, 20.0]),
    }

    result = build_qc_statistics_table(qc_table_props, config=None)

    a_total = result[(result["PROPERTY"] == "A") & (result["SELECTOR"] == "Total")]
    b_total = result[(result["PROPERTY"] == "B") & (result["SELECTOR"] == "Total")]
    # A loses its masked cell, B keeps both cells
    assert a_total["COUNT"].iloc[0] == 1
    assert b_total["COUNT"].iloc[0] == 2
    assert b_total["AVG"].iloc[0] == pytest.approx(15.0)


def test_build_qc_statistics_table_keeps_separate_date_pair_properties(monkeypatch):
    _patch_selector(monkeypatch, _codes([1, 2]), {1: "RegionA", 2: "RegionB"})
    # Two difference properties for different date pairs must each get their own
    # rows and not overwrite one another
    qc_table_props = {
        "AIRATIO_20190101_20180101": _masked([10.0, 20.0]),
        "AIRATIO_20200101_20180101": _masked([100.0, 200.0]),
    }

    result = build_qc_statistics_table(qc_table_props, config=None)

    assert set(result["PROPERTY"]) == set(qc_table_props)
    first = result[
        (result["PROPERTY"] == "AIRATIO_20190101_20180101")
        & (result["SELECTOR"] == "Total")
    ]
    second = result[
        (result["PROPERTY"] == "AIRATIO_20200101_20180101")
        & (result["SELECTOR"] == "Total")
    ]
    assert first["AVG"].iloc[0] == pytest.approx(15.0)
    assert second["AVG"].iloc[0] == pytest.approx(150.0)


def test_build_qc_statistics_table_labels_rows_with_selector_names(monkeypatch):
    _patch_selector(monkeypatch, _codes([5, 5, 7]), {5: "North", 7: "South"})
    qc_table_props = {"PORODIFF": _masked([1.0, 3.0, 9.0])}

    result = build_qc_statistics_table(qc_table_props, config=None)

    assert list(result["SELECTOR"]) == ["North", "South", "Total"]


def test_get_groupby_selector_reads_fipnum_from_grid_files(monkeypatch):
    # Exercise the default "fipnum" branch that reads EGRID/INIT data from disk;
    # all other tests patch _get_groupby_selector, so this branch is otherwise
    # never covered and could regress unnoticed.
    fipnum_values = _codes([1, 1, 2])
    fipnum_codes = {1: "FIP1", 2: "FIP2"}

    config = SimpleNamespace(
        difference_properties=SimpleNamespace(group_statistics="fipnum"),
        simulator_files=SimpleNamespace(
            rel_path_simgrid=Path("sim/model"),
            egrid_file=Path("CASE.EGRID"),
            init_property_file=Path("CASE.INIT"),
        ),
        alternative_fipnum_name="FIPNUM",
    )

    grid_sentinel = object()
    captured = {}

    def fake_grid_from_file(path):
        captured["grid_path"] = path
        return grid_sentinel

    def fake_gridproperties_from_file(property_file, fformat, names, grid):
        captured["property_file"] = property_file
        captured["fformat"] = fformat
        captured["names"] = names
        captured["grid"] = grid
        prop = SimpleNamespace(values=fipnum_values, codes=fipnum_codes)
        return {config.alternative_fipnum_name: prop}

    monkeypatch.setattr(qc_mod.xtgeo, "grid_from_file", fake_grid_from_file)
    monkeypatch.setattr(
        qc_mod.xtgeo, "gridproperties_from_file", fake_gridproperties_from_file
    )

    selector_values, selector_names = _get_groupby_selector(config=config)

    np.testing.assert_array_equal(selector_values, fipnum_values)
    assert selector_names == fipnum_codes

    # The EGRID grid is read and passed to the INIT property reader, which is
    # queried for the configured FIPNUM parameter in "init" format.
    assert captured["grid_path"] == Path("sim/model/CASE.EGRID")
    assert captured["property_file"] == Path("sim/model/CASE.INIT")
    assert captured["fformat"] == "init"
    assert captured["names"] == ["FIPNUM"]
    assert captured["grid"] is grid_sentinel
