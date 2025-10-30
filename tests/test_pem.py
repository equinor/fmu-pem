from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR, pem_fcn


def test_pem_fcn(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir / "rms/model")

    rel_path_pem = Path("../../sim2seis/model")
    pem_config_file_name = Path("pem_config_condensate.yml")

    if not INTERNAL_EQUINOR:
        with pytest.raises((NotImplementedError, ImportError)):
            pem_fcn(data_dir / "rms/model", rel_path_pem, pem_config_file_name)
    else:
        pem_fcn(data_dir / "rms/model", rel_path_pem, pem_config_file_name)


def test_pem_fcn_multi(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir / "rms/model")

    rel_path_pem = Path("../../sim2seis/model")
    pem_config_file_name = Path("pem_config_condensate_multi.yml")

    if not INTERNAL_EQUINOR:
        with pytest.raises((NotImplementedError, ImportError)):
            pem_fcn(data_dir / "rms/model", rel_path_pem, pem_config_file_name)
    else:
        pem_fcn(data_dir / "rms/model", rel_path_pem, pem_config_file_name)
