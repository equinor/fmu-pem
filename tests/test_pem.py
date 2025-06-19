from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR, pem_fcn


def test_pem_fcn(testdata, monkeypatch):
    monkeypatch.chdir(testdata)
    Path("output").mkdir(exist_ok=True)

    rel_path_pem = Path(".")
    pem_config_file_name = Path("test_pem_config_condensate.yml")

    try:
        if not INTERNAL_EQUINOR:
            with pytest.raises((NotImplementedError, ImportError)):
                pem_fcn(testdata, rel_path_pem, pem_config_file_name)
        else:
            with pytest.warns(UserWarning, match="Axis units specification is missing"):
                pem_fcn(testdata, rel_path_pem, pem_config_file_name)
    finally:
        import shutil

        shutil.rmtree("output", ignore_errors=True)
