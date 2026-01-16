from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR, pem_fcn


def test_pem_fcn(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir / "sim2seis" / "model")

    if not INTERNAL_EQUINOR:
        with pytest.raises((NotImplementedError, ImportError)):
            pem_fcn(
                config_dir=data_dir / "sim2seis" / "model",
                pem_config_file_name=Path("pem_config_condensate.yml"),
                global_config_dir=Path("../../fmuconfig/output"),
                global_config_file=Path("global_variables.yml"),
            )
    else:
        pem_fcn(
            config_dir=data_dir / "sim2seis" / "model",
            pem_config_file_name=Path("pem_config_condensate.yml"),
            global_config_dir=Path("../../fmuconfig/output"),
            global_config_file=Path("global_variables.yml"),
        )


def test_pem_fcn_multi(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir / "sim2seis" / "model")

    if not INTERNAL_EQUINOR:
        with pytest.raises((NotImplementedError, ImportError)):
            pem_fcn(
                config_dir=data_dir / "sim2seis" / "model",
                pem_config_file_name=Path("pem_config_condensate_multi.yml"),
                global_config_dir=Path("../../fmuconfig/output"),
                global_config_file=Path("global_variables.yml"),
            )
    else:
        pem_fcn(
            config_dir=data_dir / "sim2seis" / "model",
            pem_config_file_name=Path("pem_config_condensate_multi.yml"),
            global_config_dir=Path("../../fmuconfig/output"),
            global_config_file=Path("global_variables.yml"),
        )
