from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR
from fmu.pem.pem_utilities.import_config import read_pem_config
from src.fmu.pem.pem_utilities.import_config import find_key_first


def test_validate_new_pem_config_multizone(testdata, monkeypatch, data_dir):
    monkeypatch.chdir(data_dir / "sim2seis" / "model")
    pem_config_file_name = Path("../../sim2seis/model/pem_config_condensate_multi.yml")
    if INTERNAL_EQUINOR:
        try:
            _ = read_pem_config(pem_config_file_name)
        except Exception as e:
            pytest.fail(f"Validation failed: {e}")
    else:
        with pytest.raises(NotImplementedError):
            _ = read_pem_config(pem_config_file_name)


def test_validate_new_pem_config_condensate(testdata, monkeypatch, data_dir):
    monkeypatch.chdir(data_dir / "sim2seis" / "model")
    pem_config_file_name = Path("../../sim2seis/model/pem_config_condensate.yml")
    if INTERNAL_EQUINOR:
        try:
            _ = read_pem_config(pem_config_file_name)
        except Exception as e:
            pytest.fail(f"Validation failed: {e}")
    else:
        with pytest.raises(NotImplementedError):
            _ = read_pem_config(pem_config_file_name)


def test_validate_new_pem_config(testdata, monkeypatch, data_dir):
    monkeypatch.chdir(data_dir / "sim2seis" / "model")
    pem_config_file_name = Path("../../sim2seis/model/pem_config_no_condensate.yml")
    try:
        _ = read_pem_config(pem_config_file_name)
    except Exception as e:
        pytest.fail(f"Validation failed: {e}")


def test_find_key_top_level():
    d = {"target": 42, "other": 1}
    assert find_key_first(d, "target") == 42


def test_find_key_nested():
    d = {"a": 1, "b": {"target": 2, "c": {"target": 3}}}
    assert find_key_first(d, "target") == 2


def test_key_not_found():
    d = {"a": 1, "b": {"c": 2}}
    assert find_key_first(d, "missing") is None


@pytest.mark.parametrize("value", [None, False, 0, ""])
def test_falsy_values(value):
    d = {"a": {"target": value}}
    assert find_key_first(d, "target") is value


def test_first_occurrence_with_duplicates():
    d = {"a": {"target": 1, "b": {"target": 2}}, "target": 0}
    # Should return the top-level occurrence (0)
    assert find_key_first(d, "target") == 0


if __name__ == "__main__":  # pragma: no cover
    pytest.main()
