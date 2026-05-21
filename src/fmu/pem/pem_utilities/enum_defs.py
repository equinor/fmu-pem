"""
Define enumerated strings
"""

from enum import Enum, IntFlag
from typing import Literal


class PhaseSystem(IntFlag):
    """Eclipse phase system as encoded in INTEHEAD item 15 of the UNRST file.

    The Eclipse convention treats item 15 as a bitmask:
    ``1 = oil``, ``2 = water``, ``4 = gas``. Combined values therefore
    enumerate as:

    ===== =======================
    Value Phases present
    ===== =======================
    1     oil
    2     water
    3     oil + water
    4     gas
    5     oil + gas
    6     water + gas
    7     oil + water + gas
    ===== =======================
    """

    OIL = 1
    WATER = 2
    GAS = 4

    @property
    def is_multiphase(self) -> bool:
        """True if at least two phases are present."""
        return bin(int(self)).count("1") >= 2


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
