"""
Define enumerated strings
"""

from enum import Enum, IntFlag
from typing import Literal


class _OptionsMixin:
    """Mixin providing a comma-separated list of valid values for error messages."""

    @classmethod
    def options(cls) -> str:
        return ", ".join(m.value for m in cls)


class PhaseSystem(IntFlag):
    """Eclipse 100 and OPM Flow phase system as encoded in INTEHEAD item 15 of the
      UNRST file.

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


class OverburdenPressureTypes(_OptionsMixin, str, Enum):
    CONSTANT = "constant"
    TREND = "trend"


class MineralMixModel(_OptionsMixin, str, Enum):
    VOIGT_REUSS_HILL = "voigt-reuss-hill"
    HASHIN_SHTRIKMAN = "hashin-shtrikman-average"


class FluidMixModel(_OptionsMixin, str, Enum):
    WOOD = "wood"
    BRIE = "brie"


class CO2Models(_OptionsMixin, str, Enum):
    FLAG = "flag"
    SPAN_WAGNER = "span_wagner"


class RPMType(_OptionsMixin, str, Enum):
    PATCHY_CEMENT = "patchy_cement"
    FRIABLE = "friable"
    T_MATRIX = "t_matrix"
    REGRESSION = "regression"


class GasModels(_OptionsMixin, str, Enum):
    GLOBAL = "Global"
    LIGHT = "Light"
    HC2016 = "HC2016"


# class CoordinationNumberFunction(str, Enum):
#     PORBASED = "PorBased"
#     CONSTANT = "ConstVal"
CoordinationNumberFunction = Literal["PorBased", "ConstVal"]


class TemperatureMethod(_OptionsMixin, str, Enum):
    CONSTANT = "constant"
    FROMSIM = "from_sim"


class DifferenceMethod(_OptionsMixin, str, Enum):
    DIFF = "diff"
    DIFFPERCENT = "diffpercent"
    RATIO = "ratio"


class DifferenceAttribute(_OptionsMixin, str, Enum):
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
    EFFECTIVE_PRESSURE = "effective_pressure"
    OVERBURDEN_PRESSURE = "overburden_pressure"


class PhysicsPressureModelTypes(_OptionsMixin, str, Enum):
    FRIABLE = "friable"
    PATCHY_CEMENT = "patchy_cement"


class ParameterTypes(_OptionsMixin, str, Enum):
    VP = "vp"
    VS = "vs"
    K = "k"
    MU = "mu"
    RHO = "rho"
    POROSITY = "poro"


class Sim2SeisRequiredParams(_OptionsMixin, str, Enum):
    VP = "vp"
    VS = "vs"
    DENSITY = "density"


class SaveTypes(_OptionsMixin, str, Enum):
    INTERMEDIATE_PROPERTIES = "intermediate"
    ELASTIC_PROPERTIES = "elastic"
    DIFFERENCE_PROPERTIES = "difference"
    GRID = "grid"
    ALL = "all"
