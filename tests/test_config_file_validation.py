from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR
from fmu.pem.pem_utilities.import_config import read_pem_config


def test_validate_new_pem_config_multizone(testdata, monkeypatch, data_dir):
    monkeypatch.chdir(data_dir / "rms/model")
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
    monkeypatch.chdir(data_dir / "rms/model")
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
    monkeypatch.chdir(data_dir / "rms/model")
    pem_config_file_name = Path("../../sim2seis/model/pem_config_no_condensate.yml")
    try:
        _ = read_pem_config(pem_config_file_name)
    except Exception as e:
        pytest.fail(f"Validation failed: {e}")


if __name__ == "__main__":  # pragma: no cover
    pytest.main()
