"""Tests for the optional Eclipse-PORO adjustment for non-binary NTG.

Covers both the pydantic schema (discriminated union on ``method``) and the
runtime helper :func:`fmu.pem.pem_utilities.apply_porosity_adjustment`.
"""

from pathlib import Path

import numpy as np
import pytest
import xtgeo
import yaml

from fmu.pem.pem_utilities import apply_porosity_adjustment
from fmu.pem.pem_utilities.import_routines import (
    _verify_grid_dimensions_match,
    _verify_ntg_is_non_binary,
)
from fmu.pem.pem_utilities.pem_class_definitions import SimInitProperties
from fmu.pem.pem_utilities.pem_config_validation import (
    ConstantNonNetPorosity,
    NoPorosityAdjustment,
    PorosityAdjustment,
    PreAdjustedPorosityGrid,
    RockMatrixProperties,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sim_grid() -> xtgeo.Grid:
    """Small 3x3x2 synthetic grid."""
    return xtgeo.create_box_grid(dimension=(3, 3, 2))


@pytest.fixture
def base_poro() -> np.ma.MaskedArray:
    """Fully-active 3x3x2 PORO field of 0.20."""
    return np.ma.masked_array(
        np.full((3, 3, 2), 0.20, dtype=float),
        mask=np.zeros((3, 3, 2), dtype=bool),
    )


@pytest.fixture
def sim_init(base_poro) -> SimInitProperties:
    depth = np.ma.masked_array(np.zeros_like(base_poro.data), mask=base_poro.mask)
    return SimInitProperties(poro=base_poro, depth=depth)


def _add_ntg(sim_init: SimInitProperties, values: np.ndarray) -> SimInitProperties:
    sim_init.ntg = np.ma.masked_array(values, mask=np.zeros_like(values, dtype=bool))
    return sim_init


def _make_gridprop(
    sim_grid: xtgeo.Grid, values: np.ndarray, name: str = "NTG"
) -> xtgeo.GridProperty:
    return xtgeo.GridProperty(
        ncol=sim_grid.ncol,
        nrow=sim_grid.nrow,
        nlay=sim_grid.nlay,
        values=np.ma.masked_array(values, mask=np.zeros_like(values, dtype=bool)),
        name=name,
    )


# ---------------------------------------------------------------------------
# Schema: discriminated union
# ---------------------------------------------------------------------------


def _minimal_rock_matrix_kwargs() -> dict:
    """Minimal kwargs to construct a RockMatrixProperties; we only need a
    valid stub to exercise the discriminator."""
    from fmu.pem.pem_utilities.pem_config_validation import FractionFiles

    return {
        "zone_regions": [
            {
                "fipnum": "*",
                "model": {
                    "model_name": "friable",
                    "params": {},
                },
            }
        ],
        "volume_fractions": FractionFiles.model_construct(
            rel_path_fractions=Path("."),
            fractions_prop_file_names=[Path("a.roff")],
            fractions_are_mineral_fraction=False,
        ),
        "fraction_names": ["vsh"],
        "fraction_minerals": ["shale"],
        "shale_fractions": ["vsh"],
        "complement": "quartz",
    }


def test_default_porosity_adjustment_is_none(data_dir):
    """Omitting ``porosity_adjustment`` in the config defaults to no-op."""
    config_path = data_dir / "sim2seis" / "model" / "pem_config_no_condensate.yml"
    with config_path.open() as file_handle:
        config_data = yaml.safe_load(file_handle)

    rm = RockMatrixProperties.model_validate(
        config_data["rock_matrix"],
        context={"pre_experiment": True},
    )
    assert isinstance(rm.porosity_adjustment, NoPorosityAdjustment)
    assert rm.porosity_adjustment.method == "none"


def test_discriminator_picks_constant_variant():
    parsed: PorosityAdjustment = ConstantNonNetPorosity.model_validate(
        {"method": "constant", "non_net_porosity": 0.05}
    )
    assert isinstance(parsed, ConstantNonNetPorosity)
    assert parsed.non_net_porosity == 0.05


def test_discriminator_picks_grid_file_variant(tmp_path):
    parsed = PreAdjustedPorosityGrid.model_validate(
        {
            "method": "grid_file",
            "rel_path": str(tmp_path),
            "file_name": "missing.roff",
        },
        context={"pre_experiment": True},
    )
    assert isinstance(parsed, PreAdjustedPorosityGrid)


def test_pre_adjusted_grid_file_missing_raises(tmp_path):
    with pytest.raises(Exception):
        PreAdjustedPorosityGrid.model_validate(
            {
                "method": "grid_file",
                "rel_path": str(tmp_path),
                "file_name": "missing.roff",
            }
        )


def test_pre_experiment_skips_grid_file_existence_check(tmp_path):
    PreAdjustedPorosityGrid.model_validate(
        {
            "method": "grid_file",
            "rel_path": str(tmp_path),
            "file_name": "missing.roff",
        },
        context={"pre_experiment": True},
    )


def test_constant_non_net_porosity_out_of_range():
    with pytest.raises(Exception):
        ConstantNonNetPorosity.model_validate(
            {"method": "constant", "non_net_porosity": 0.9}
        )
    with pytest.raises(Exception):
        ConstantNonNetPorosity.model_validate(
            {"method": "constant", "non_net_porosity": -0.01}
        )


# ---------------------------------------------------------------------------
# apply_porosity_adjustment: no-op
# ---------------------------------------------------------------------------


def test_no_adjustment_leaves_poro_unchanged(sim_init, sim_grid, tmp_path):
    original = sim_init.poro.copy()
    apply_porosity_adjustment(
        adjustment=NoPorosityAdjustment(),
        sim_init=sim_init,
        sim_grid=sim_grid,
        root_dir=tmp_path,
    )
    np.testing.assert_array_equal(sim_init.poro, original)


# ---------------------------------------------------------------------------
# apply_porosity_adjustment: constant non-net porosity
# ---------------------------------------------------------------------------


def test_constant_non_net_adjustment_applies_formula(sim_init, sim_grid, tmp_path):
    """``por_tot = ntg * PORO + (1 - ntg) * non_net_porosity``."""
    _add_ntg(sim_init, np.full((3, 3, 2), 0.6, dtype=float))

    apply_porosity_adjustment(
        adjustment=ConstantNonNetPorosity(non_net_porosity=0.05),
        sim_init=sim_init,
        sim_grid=sim_grid,
        root_dir=tmp_path,
    )

    expected = 0.6 * 0.20 + 0.4 * 0.05
    np.testing.assert_allclose(sim_init.poro.data, expected)


def test_constant_non_net_adjustment_raises_on_binary_ntg(sim_init, sim_grid, tmp_path):
    ntg_values = np.where(np.indices((3, 3, 2)).sum(axis=0) % 2 == 0, 1.0, 0.0).astype(
        float
    )
    _add_ntg(sim_init, ntg_values)

    with pytest.raises(ValueError, match="binary"):
        apply_porosity_adjustment(
            adjustment=ConstantNonNetPorosity(non_net_porosity=0.05),
            sim_init=sim_init,
            sim_grid=sim_grid,
            root_dir=tmp_path,
        )


def test_constant_non_net_adjustment_raises_when_ntg_absent(
    sim_init, sim_grid, tmp_path
):
    assert sim_init.ntg is None
    with pytest.raises(ImportError, match="NTG parameter is required"):
        apply_porosity_adjustment(
            adjustment=ConstantNonNetPorosity(non_net_porosity=0.05),
            sim_init=sim_init,
            sim_grid=sim_grid,
            root_dir=tmp_path,
        )


# ---------------------------------------------------------------------------
# apply_porosity_adjustment: pre-adjusted grid file
# ---------------------------------------------------------------------------


def test_pre_adjusted_grid_replaces_poro(sim_init, sim_grid, tmp_path):
    new_values = np.full((3, 3, 2), 0.31, dtype=float)
    gp = _make_gridprop(sim_grid, new_values, name="PORO_TOT")
    file_name = Path("poro_adjusted.roff")
    gp.to_file(tmp_path / file_name, fformat="roff")

    apply_porosity_adjustment(
        adjustment=PreAdjustedPorosityGrid(rel_path=tmp_path, file_name=file_name),
        sim_init=sim_init,
        sim_grid=sim_grid,
        root_dir=Path("/"),
    )

    np.testing.assert_allclose(sim_init.poro.data, 0.31)


def test_pre_adjusted_grid_dimensions_mismatch_raises(sim_init, sim_grid, tmp_path):
    other_grid = xtgeo.create_box_grid(dimension=(4, 4, 2))
    new_values = np.full((4, 4, 2), 0.31, dtype=float)
    gp = _make_gridprop(other_grid, new_values, name="PORO_TOT")
    file_name = Path("poro_wrong_dims.roff")
    gp.to_file(tmp_path / file_name, fformat="roff")

    with pytest.raises(ValueError, match="dimensions"):
        apply_porosity_adjustment(
            adjustment=PreAdjustedPorosityGrid(rel_path=tmp_path, file_name=file_name),
            sim_init=sim_init,
            sim_grid=sim_grid,
            root_dir=Path("/"),
        )


def test_pre_adjusted_grid_missing_file_raises(sim_init, sim_grid, tmp_path):
    with pytest.raises(ImportError, match="failed to import"):
        apply_porosity_adjustment(
            adjustment=PreAdjustedPorosityGrid.model_construct(
                method="grid_file",
                rel_path=Path("."),
                file_name=Path("does_not_exist.roff"),
            ),
            sim_init=sim_init,
            sim_grid=sim_grid,
            root_dir=tmp_path,
        )


def test_pre_adjusted_grid_masked_active_cells_raises(sim_init, sim_grid, tmp_path):
    values = np.full((3, 3, 2), 0.31, dtype=float)
    mask = np.zeros((3, 3, 2), dtype=bool)
    mask[0, 0, 0] = True
    gp = xtgeo.GridProperty(
        ncol=sim_grid.ncol,
        nrow=sim_grid.nrow,
        nlay=sim_grid.nlay,
        values=np.ma.masked_array(values, mask=mask),
        name="PORO_TOT",
    )
    file_name = Path("poro_mask_mismatch.roff")
    gp.to_file(tmp_path / file_name, fformat="roff")

    with pytest.raises(ValueError, match="masks active simulation cells"):
        apply_porosity_adjustment(
            adjustment=PreAdjustedPorosityGrid(rel_path=tmp_path, file_name=file_name),
            sim_init=sim_init,
            sim_grid=sim_grid,
            root_dir=Path("/"),
        )


# ---------------------------------------------------------------------------
# Internal verification helpers
# ---------------------------------------------------------------------------


def test_verify_grid_dimensions_match_accepts_matching(sim_grid):
    gp = _make_gridprop(sim_grid, np.zeros((3, 3, 2)), name="X")
    _verify_grid_dimensions_match(gp, sim_grid, Path("any"))


def test_verify_ntg_non_binary_accepts_fractional():
    arr = np.ma.masked_array(np.array([0.2, 0.5, 0.8]), mask=[False, False, False])
    _verify_ntg_is_non_binary(arr)


def test_verify_ntg_non_binary_rejects_all_zero_or_one():
    arr = np.ma.masked_array(
        np.array([0.0, 1.0, 1.0, 0.0]), mask=[False, False, False, False]
    )
    with pytest.raises(ValueError, match="binary"):
        _verify_ntg_is_non_binary(arr)
