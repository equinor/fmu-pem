import pytest
from pydantic import ValidationError

from fmu.pem.pem_utilities.enum_defs import Lithology
from fmu.pem.pem_utilities.pem_config_validation import (
    MineralMixModel,
    MineralProperties,
    RockMatrixProperties,
)


def test_dryrock_missing_rpm_model():
    """Test RockMatrixProperties instantiation with minimal valid data."""
    valid_data = {
        "model": {
            "model_name": None,
            "parameters": {
                "upper_bound_cement_fraction": 0.1,
                "cement_fraction": 0.04,
                "critical_porosity": 0.4,
                "shear_reduction": 0.5,
                "coord_num_function": "ConstVal",
                "coordination_number": 9.0,
            },
        },
        "minerals": {
            "quartz": MineralProperties(
                bulk_modulus=37.0e9, shear_modulus=44.0e9, density=2.65e3
            ),
            "clay": MineralProperties(
                bulk_modulus=15.0e9, shear_modulus=6.0e9, density=2.58e3
            ),
        },
        "fraction_names": ["quartz", "clay"],
        "fraction_minerals": ["quartz", "clay"],
        "shale_fractions": ["clay"],
        "complement": "quartz",
        "ntg_calculation_flag": True,
        "ntg_from_porosity": False,
        "pressure_sensitivity": True,
        "cement": "quartz",
        "mineral_mix_model": MineralMixModel.VOIGT_REUSS_HILL,
    }

    with pytest.raises(
        ValidationError,
        match=(r"Input should be <RPMType\.PATCHY_CEMENT: 'patchy_cement'>"),
    ):
        RockMatrixProperties(**valid_data)
