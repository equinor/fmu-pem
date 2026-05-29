from pathlib import Path

import numpy as np
import pytest
import resfo

from fmu.pem.pem_utilities import read_phase_system
from fmu.pem.pem_utilities.enum_defs import PhaseSystem


def _write_unrst(path: Path, *, iprog: int, phase_indicator: int) -> None:
    """Write a minimal UNRST file containing a single INTEHEAD record.

    Only the two items relevant to ``read_phase_system`` (PHASE at index 14
    and IPROG at index 94) are populated; everything else stays zero.
    """
    intehead = np.zeros(411, dtype=np.int32)
    intehead[14] = phase_indicator
    intehead[94] = iprog
    resfo.write(path, [("INTEHEAD", intehead)])


def test_read_phase_system_eclipse_300_assumes_all_phases(tmp_path: Path) -> None:
    unrst = tmp_path / "ECL300.UNRST"
    # Even with a deck that only advertises oil+water (indicator = 3) in
    # INTEHEAD item 15, Eclipse 300 always carries all three phases.
    _write_unrst(unrst, iprog=300, phase_indicator=3)

    assert read_phase_system(unrst) == (
        PhaseSystem.OIL | PhaseSystem.WATER | PhaseSystem.GAS
    )


def test_read_phase_system_eclipse_300_thermal_assumes_all_phases(
    tmp_path: Path,
) -> None:
    unrst = tmp_path / "ECL300T.UNRST"
    _write_unrst(unrst, iprog=500, phase_indicator=1)

    assert read_phase_system(unrst) == (
        PhaseSystem.OIL | PhaseSystem.WATER | PhaseSystem.GAS
    )


def test_read_phase_system_eclipse_100_uses_phase_indicator(tmp_path: Path) -> None:
    unrst = tmp_path / "ECL100.UNRST"
    _write_unrst(
        unrst, iprog=100, phase_indicator=int(PhaseSystem.OIL | PhaseSystem.WATER)
    )

    assert read_phase_system(unrst) == PhaseSystem.OIL | PhaseSystem.WATER


def test_read_phase_system_invalid_indicator_raises_for_non_e300(
    tmp_path: Path,
) -> None:
    unrst = tmp_path / "BAD.UNRST"
    _write_unrst(unrst, iprog=100, phase_indicator=0)

    with pytest.raises(ValueError, match="Unexpected phase indicator"):
        read_phase_system(unrst)
