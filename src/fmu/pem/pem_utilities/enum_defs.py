"""
Define enumerated strings
"""

from enum import Enum
from typing import Literal


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


# class CoordinationNumberFunction(str, Enum):
#     PORBASED = "PorBased"
#     CONSTANT = "ConstVal"
CoordinationNumberFunction = Literal["PorBased", "ConstVal"]


class TemperatureMethod(str, Enum):
    CONSTANT = "constant"
    FROMSIM = "from_sim"


class DifferenceMethod(str, Enum):
    DIFF = "diff"
    DIFFPERCENT = "diffpercent"
    RATIO = "ratio"


class DifferenceAttribute(str, Enum):
    AI = "ai"
    VPVS = "vpvs"
    SI = "si"
    VP = "vp"
    VS = "vs"
    DENS = "dens"
    TWT = "twt"
    SGAS = "sgas"
    SWAT = "swat"
    SOIL = "soil"
    RS = "rs"
    RV = "rv"
    PRESSURE = "pressure"
    SALT = "salt"
    TEMP = "temp"
    TWTPP = "twtpp"
    TWTSS = "twtss"
    TWTPS = "twtps"
    FORMATION_PRESSURE = "formation_pressure"
    EFFECTIVE_PRESSURE = "effective_pressure"
    OVERBURDEN_PRESSURE = "overburden_pressure"


class RegressionPressureModelTypes(str, Enum):
    EXPONENTIAL = "exponential"
    POLYNOMIAL = "polynomial"


class PhysicsPressureModelTypes(str, Enum):
    FRIABLE = "friable"
    PATCHY_CEMENT = "patchy_cement"


class RegressionPressureParameterTypes(str, Enum):
    VP_VS = "vp_vs"
    K_MU = "k_mu"


class ParameterTypes(str, Enum):
    VP = "vp"
    VS = "vs"
    K = "k"
    MU = "mu"
    RHO = "rho"
    POROSITY = "poro"


class Sim2SeisRequiredParams(str, Enum):
    VP = "vp"
    VS = "vs"
    DENSITY = "density"
