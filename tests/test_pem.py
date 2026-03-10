from pathlib import Path

import pytest

from fmu.pem import INTERNAL_EQUINOR, pem, pem_fcn
from fmu.pem.pem_utilities import (
    PemConfig,
    get_global_params_and_dates,
    read_pem_config,
)


def setup(data_dir: Path, config_file: Path) -> tuple[PemConfig, Path]:
    run_folder = data_dir
    config_dir = data_dir / "sim2seis" / "model"
    global_dir = Path("fmuconfig/output")
    global_file = Path("global_variables.yml")

    config = read_pem_config(yaml_file=config_dir / config_file)

    config.update_with_global(
        get_global_params_and_dates(
            global_config_dir=(run_folder / global_dir).resolve(),
            global_conf_file=global_file,
            mod_prefix="HIST",
            obs_prefix="HIST",
        )
    )
    return config, run_folder


def test_pem_fcn(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir)

    conf, run_dir = setup(
        data_dir=data_dir,
        config_file="pem_config_no_condensate.yml",
    )

    pem_fcn(
        config=conf,
        run_dir=run_dir,
    )


def test_pem_fcn_multi(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir)

    if not INTERNAL_EQUINOR:
        with pytest.raises((NotImplementedError, ImportError)):
            conf, config_dir = setup(
                data_dir=data_dir,
                config_file="pem_config_condensate_multi.yml",
            )
            pem_fcn(
                config=conf,
                run_dir=config_dir,
            )
    else:
        conf, config_dir = setup(
            data_dir=data_dir,
            config_file="pem_config_condensate_multi.yml",
        )
        pem_fcn(
            config=conf,
            run_dir=config_dir,
        )


def test_pem_main(data_dir, monkeypatch):
    monkeypatch.chdir(data_dir)

    if not INTERNAL_EQUINOR:
        pem(
            args_list=[
                "--config-dir",
                str((data_dir / "sim2seis" / "model").resolve()),
                "--config-file",
                "pem_config_no_condensate.yml",
                "--global-dir",
                "fmuconfig/output",
                "--global-file",
                "global_variables.yml",
                "--mod-date-prefix",
                "HIST",
            ]
        )
    else:
        pem(
            args_list=[
                "--config-dir",
                str((data_dir / "sim2seis" / "model").resolve()),
                "--config-file",
                "pem_config_condensate_multi.yml",
                "--global-dir",
                "fmuconfig/output",
                "--global-file",
                "global_variables.yml",
                "--mod-date-prefix",
                "HIST",
            ]
        )
