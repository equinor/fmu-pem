from pathlib import Path
from shutil import copytree

import pytest


@pytest.fixture(scope="session")
def testdata() -> Path:
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session", autouse=True, name="data_dir")
def setup_sim2seis_test_data(testdata, tmp_path_factory):
    config_dir = tmp_path_factory.mktemp("data")
    # Copy data directory tree
    copytree(testdata, config_dir, dirs_exist_ok=True)

    # Create output and start directories
    grid_path = config_dir / "share/results/grids"
    grid_path.mkdir(parents=True, exist_ok=True)

    pem_output_path = config_dir / "sim2seis/output/pem"
    pem_output_path.mkdir(parents=True, exist_ok=True)

    return config_dir
