"""
Define enumerated strings
"""

from enum import Enum


class OverburdenPressureTypes(str, Enum):
    CONSTANT = "constant"
    TREND = "trend"


class Lithology(str, Enum):
    SILICICLASTICS = "siliciclastics"
    CARBONATE = "carbonate"


class MineralMixModel(str, Enum):
    VOIGT_REUSS_HILL = "voigt-reuss-hill"
    HASHIN_SHTRIKMAN = "hashin-shtrikman-average"


class FluidMixModel(str, Enum):
    WOOD = "wood"
    BRIE = "brie"


class SaveTypes(str, Enum):
    SAVE_TO_RMS = "save_results_to_rms"
    SAVE_TO_DISK = "save_results_to_disk"
    SAVE_INTERMEDIATE_RESULTS = "save_intermediate_results"
    SAVE_RESULTS_TO_CSV = "save_results_to_csv"


class CO2Models(str, Enum):
    FLAG = "flag"
    SPAN_WAGNER = "span_wagner"


class RegressionModelLithologies(str, Enum):
    SANDSTONE = "sandstone"
    SHALE = "shale"


class RPMType(str, Enum):
    PATCHY_CEMENT = "patchy_cement"
    FRIABLE = "friable"
    T_MATRIX = "t_matrix"
    REGRESSION = "regression"


class GasModels(str, Enum):
    GLOBAL = "Global"
    LIGHT = "Light"
    HC2016 = "HC2016"


class CoordinationNumberFunction(str, Enum):
    PORBASED = "PorBased"
    CONSTANT = "ConstVal"


class TemperatureMethod(str, Enum):
    CONSTANT = "constant"
    FROMSIM = "from_sim"
