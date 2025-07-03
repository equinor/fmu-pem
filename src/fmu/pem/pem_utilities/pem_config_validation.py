import os
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Self, Union

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    Field,
    field_validator,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema
from pydantic_core.core_schema import ValidationInfo

from fmu.pem import INTERNAL_EQUINOR

from .enum_defs import (
    CO2Models,
    FluidMixModel,
    GasModels,
    MineralMixModel,
    OverburdenPressureTypes,
    TemperatureMethod,
    VolumeFractions,
)
from .rpm_models import MineralProperties, PatchyCementRPM, RegressionRPM, TMatrixRPM


class NTGFraction(BaseModel):
    mode: SkipJsonSchema[Literal[VolumeFractions.NTG_SIM]]
    from_porosity: bool = Field(
        default=False,
        description="If checked, net-to-gross is estimated from porosity parameter in "
        "reservoir simulator `.INIT` file. Otherwise, net-to-gross is read "
        "from the `NTG` parameter in the `.INIT` file.",
    )


class FractionFiles(BaseModel):
    mode: SkipJsonSchema[Literal[VolumeFractions.VOL_FRAC]]
    rel_path_fractions: DirectoryPath = Field(
        default=Path("../../sim2seis/input/pem"),
        description="Directory for volume fractions",
    )
    fractions_grid_file_name: Path = Field(
        description="Grid definition of the volume fractions"
    )
    fractions_prop_file_names: list[Path] = Field(description="Volume fractions")
    fraction_is_ntg: bool = Field(
        default=True,
        description="In case of a single fraction, it can either be a real volume "
        "fraction or a net-to-gross parameter. If there is more than one fraction, "
        "they have to represent real volume fractions, and this will be ignored",
    )

    @model_validator(mode="after")
    def check_fractions(self) -> Self:
        full_fraction_grid = self.rel_path_fractions / self.fractions_grid_file_name
        if not full_fraction_grid.exists():
            raise FileNotFoundError(
                f"fraction grid file is missing: {full_fraction_grid}"
            )
        for frac_prop in self.fractions_prop_file_names:
            full_fraction_prop = self.rel_path_fractions / frac_prop
            if not full_fraction_prop.exists():
                raise FileNotFoundError(
                    f"fraction prop file is missing: {full_fraction_prop}"
                )
        return self


class RockMatrixProperties(BaseModel):
    """Configuration for rock matrix properties.

    Contains parameters necessary for defining matrix properties for
    different rock types, including sandstones, carbonates,
    and other lithologies.
    """

    model_config = ConfigDict(title="Rock matrix properties:")

    model: Union[PatchyCementRPM, TMatrixRPM, RegressionRPM] = Field(
        description="Selection of parameter set for rock physics model",
        default_factory=PatchyCementRPM,
    )
    minerals: Dict[str, MineralProperties] = Field(
        default={
            "shale": {
                "bulk_modulus": 25.0e9,
                "shear_modulus": 12.0e9,
                "density": 2680.0,
            },
            "quartz": {
                "bulk_modulus": 36.8e9,
                "shear_modulus": 44.0e9,
                "density": 2650.0,
            },
            "calcite": {
                "bulk_modulus": 76.8e9,
                "shear_modulus": 32.0e9,
                "density": 2710.0,
            },
            "dolomite": {
                "bulk_modulus": 94.9e9,
                "shear_modulus": 45.0e9,
                "density": 2870.0,
            },
            "stevensite": {
                "bulk_modulus": 32.5e9,
                "shear_modulus": 45.0e9,
                "density": 2490.0,
            },
        },
        description="Standard values are set for `shale`, `quartz`, "
        "`calcite`, `dolomite` and `stevensite`. All settings can be "
        "changed by re-defining them in the parameter file",
    )
    volume_fractions: NTGFraction | FractionFiles = Field(
        default=NTGFraction,
        description=r"Choice of volume fractions based on `NTG` from "
        "simulator `.INIT` file or from grid property file ",
    )
    fraction_names: List[str] = Field(
        description="Fraction names must match the names in the volume fractions file",
    )
    fraction_minerals: List[str] = Field(
        description="The list of minerals matching the fractions' definition. Each "
        "mineral must be defined in the mineral properties dictionary"
    )
    shale_fractions: List[str] = Field(
        description="List the fractions that should be regarded as non-net reservoir"
    )
    complement: str = Field(
        description="For grid cells where the sum of the fractions does not add "
        "up to 1.0, the remainder is filled with the complement mineral, "
        "e.g. when using net-to-gross instead of volume fractions"
    )
    pressure_sensitivity: bool = Field(
        default=True,
        description="For the RPM models where pressure sensitivity is not part of "
        "the model, as for friable and patchy cement models, a separate "
        "pressure sensitivity model, based on plug measurements is added",
    )
    cement: str = Field(
        default="quartz",
        description="For the patchy cement model, the cement mineral must be defined, "
        "and its properties must be defined in the mineral properties' "
        "dictionary",
    )
    mineral_mix_model: MineralMixModel = Field(
        default="voigt-reuss-hill",
        description="Effective medium model selection: either "
        "`hashin-shtrikman-average` or `voigt-reuss-hill`",
    )

    @field_validator("shale_fractions", mode="before")
    @classmethod
    def shale_fraction_check(cls, v: list, info: ValidationInfo) -> list:
        for frac in v:
            if frac not in info.data["fraction_names"]:
                raise ValueError(
                    f'{__file__}: shale fraction "{frac}" not listed in volume '
                    f"fraction names"
                )
        return v

    @field_validator("complement", mode="before")
    @classmethod
    def complement_fraction_check(cls, v: list, info: ValidationInfo) -> list:
        if v not in info.data["minerals"]:
            raise ValueError(
                f'{__file__}: shale fraction mineral "{v}" not listed in fraction '
                f"minerals"
            )
        return v

    @field_validator("cement", mode="before")
    def cement_check(cls, v: list, info: ValidationInfo) -> list:
        if v not in info.data["minerals"]:
            raise ValueError(f'{__file__}: cement mineral "{v}" not listed in minerals')
        return v

    @model_validator(mode="after")
    def mineral_fraction_check(self):
        for frac_min in self.fraction_minerals:
            if frac_min not in self.minerals:
                raise ValueError(
                    f"{__file__}: volume fraction mineral {frac_min} is not defined"
                )
        return self


# Pressure
class OverburdenPressureTrend(BaseModel):
    type: SkipJsonSchema[OverburdenPressureTypes] = "trend"
    intercept: float = Field(description="Intercept in pressure depth trend")
    gradient: float = Field(description="Gradient in pressure depth trend")


class OverburdenPressureConstant(BaseModel):
    type: SkipJsonSchema[OverburdenPressureTypes] = "constant"
    value: float = Field(description="Constant pressure")


# Fluids
class Brine(BaseModel):
    salinity: float = Field(
        default=35000.0,
        gt=0.0,
        description="Salinity of brine, with unit `ppm` (parts per million)",
    )
    perc_na: float = Field(
        ge=0.0,
        le=100.0,
        default=0.0,
        description="Percentage of `NaCl in the dissolved salts in brine",
    )
    perc_ca: float = Field(
        ge=0.0,
        le=100.0,
        default=100.0,
        description="Percentage of `CaCl` in the dissolved salts in brine",
    )
    perc_k: float = Field(
        ge=0.0,
        le=100.0,
        default=0.0,
        description="Percentage of `KCl` in the dissolved salts in brine",
    )

    @model_validator(mode="after")
    def check_perc_sum(self):
        perc_sum = self.perc_na + self.perc_ca + self.perc_k
        if np.isclose(perc_sum, 100.0):
            return self

        eps = 0.1
        if abs(perc_sum - 100.0) < eps:
            # silently adjust values
            self.perc_na *= 100.0 / perc_sum
            self.perc_ca *= 100.0 / perc_sum
            self.perc_k *= 100.0 / perc_sum
            return self

        raise ValueError(
            "sum of chloride percentages "
            f"({perc_sum}%) differs from 100% by more than 10% "
            "in brine parameters"
        )


class Oil(BaseModel):
    gas_gravity: float = Field(
        default=0.7,
        ge=0.55,
        le=0.87,
        description="Gas gravity is a ratio of gas molecular weight to that air",
    )
    reference_density: float = Field(
        default=865.0,
        ge=700,
        le=950,
        description="Oil density in `kg/m³` at standard conditions, i.e. `15.6 °C`"
        "and `101 kPa`",
    )
    gor: float = Field(
        default=123.0,
        ge=0.0,
        description="Gas-oil volume ratio in `liter/liter` when the oil it brought to "
        "the surface at standard conditions. This is normally read from the "
        "simulator model restart file (Rs parameter).",
    )


class Gas(BaseModel):
    gas_gravity: float = Field(
        default=0.7,
        ge=0.55,
        le=0.87,
        description="Gas gravity is a ratio of gas molecular weight to that air",
    )
    model: SkipJsonSchema[GasModels] = Field(
        default="HC2016",
        description="Gas model is one of `Global`, `Light`, or `HC2016` (default)",
    )


class MixModelWood(BaseModel):
    method: SkipJsonSchema[FluidMixModel] = "wood"


class MixModelBrie(BaseModel):
    method: SkipJsonSchema[FluidMixModel] = "brie"
    brie_exponent: float = Field(
        default=3.0,
        description="Brie exponent selects the mixing curve shape, from linear mix "
        "(exponent = 2.0) to approximate harmonic mean for high values "
        "(exponent > 10.0). Default value is 3.0.",
    )


class ConstantTemperature(BaseModel):
    type: SkipJsonSchema[TemperatureMethod] = "constant"
    temperature_value: float


class TemperatureFromSim(BaseModel):
    type: SkipJsonSchema[TemperatureMethod] = "from_sim"


# Note that CO2 does not require a separate definition here, as it's properties only
# depend on temperature and pressure
class Fluids(BaseModel):
    brine: Brine = Field(
        description="Brine model parameters",
    )
    oil: Oil = Field(description="Oil model parameters")
    gas: Gas = Field(description="Gas model parameters")
    condensate: Oil | None = Field(
        default=None,
        title="Condensate properties",
        description="Condensate is defined by the same set of parameters as oil, "
        "optional setting for condensate cases",
    )
    fluid_mix_method: MixModelBrie | MixModelWood = Field(
        default=MixModelBrie,
        description="Selection between Wood's or Brie model. Wood's model gives more "
        "radical response to adding small amounts of gas in brine or oil",
    )
    temperature: ConstantTemperature | TemperatureFromSim = Field(
        description="In most cases it is sufficient with a constant temperature "
        "setting for the reservoir. If temperature is modelled in the "
        "simulation model, it is preferred to use that"
    )
    salinity_from_sim: bool = Field(
        default=False,
        description="In most cases it is sufficient with a constant salinity "
        "setting for the reservoir, unless there is large contrast"
        "between formation water and injected water. If salinity is "
        "modelled in the simulation model, it is preferred to use that",
    )
    gas_saturation_is_co2: bool = Field(
        default=False,
        description="Eclipse model only provides one parameter for gas saturation, "
        "this flag sets the gas type to be CO₂ instead of hydrocarbon gas",
    )
    calculate_condensate: bool = Field(
        default=False,
        description="Flag to control if gas should be modelled with condensate model, "
        "in which case `RV` parameter must be present in the Eclipse model",
    )
    gas_z_factor: float = Field(
        default=1.0,
        description="Factor for deviation from an ideal gas in terms of volume change "
        "as a function of temperature and pressure",
    )
    co2_model: CO2Models = Field(
        default="span_wagner",
        description="Selection of model for CO₂ properties, `span_wagner` equation "
        "of state model or `flag`. Note that access to flag model depends "
        "on licence",
    )

    @model_validator(mode="after")
    def check_fluid_type(self) -> Self:
        if self.calculate_condensate and not INTERNAL_EQUINOR:
            raise NotImplementedError(
                "Missing model for condensate, proprietary model required"
            )
        return self


def possible_date_string(date_strings: List[str]) -> bool:
    """
    Validate a list of date strings in YYYYMMDD format.

    Args:
        date_strings: List of strings to validate

    Returns:
        bool: True if all strings are valid dates

    Raises:
        ValueError: If any string is not a valid date in YYYYMMDD format
    """
    for date_string in date_strings:
        if len(date_string) != 8:
            raise ValueError(
                f"Invalid date format: '{date_string}' must be exactly 8 characters"
            )
        try:
            date(
                year=int(date_string[0:4]),
                month=int(date_string[4:6]),
                day=int(date_string[6:]),
            )
        except ValueError:
            raise ValueError(
                f"Invalid date: '{date_string}' must be a valid date in YYYYMMDD format"
            )
    return True


class FromGlobal(BaseModel):
    grid_model: str
    seis_dates: List[str]
    diff_dates: List[List[str]]
    global_config: Dict[str, Any]

    @field_validator("seis_dates", mode="before")
    def check_date_string(cls, v: List[str]) -> List[str]:
        possible_date_string(v)
        return v

    @field_validator("diff_dates", mode="before")
    def check_diffdate_string(cls, v: List[List[str]]) -> List[List[str]]:
        for ll in v:
            possible_date_string(ll)
        return v


class PemPaths(BaseModel):
    rel_path_mandatory_output: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../sim2seis/output/pem"),
        description="Directory of PEM results that will be used as input "
        "to seismic_forward",
        frozen=True,
    )
    rel_path_output: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../share/results/grids"),
        description="Directory for grid parameter results from PEM for "
        "later visualization",
        frozen=True,
    )
    rel_path_pem: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../sim2seis/model"),
        description="Relative path to the directory containing the PEM's config file",
        frozen=True,
    )
    rel_path_fmu_config: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../fmuconfig/output"),
        description="Relative path to the directory containing the global config "
        "file for the FMU workflow",
        frozen=True,
    )
    rel_ntg_grid_path: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../sim2seis/input/pem"),
        description="This is the relative path to the ntg grid file. If the "
        "ntg_calculation_flag is False, it is disregarded, cfr. fractions",
    )
    rel_path_simgrid: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../sim2seis/input/pem"),
        description="Directory for eclipse simulation grid",
    )
    rel_path_geogrid: SkipJsonSchema[DirectoryPath] = Field(
        default=Path("../../sim2seis/input/pem"),
        description="If the porosity property is read from geogrid instead of from "
        "simgrid, this directory is used. At present, porosity is expected "
        "to come from the simgrid",
    )


class Results(BaseModel):
    save_results_to_rms: bool = Field(
        default=False,
        description="When the PEM is run from RMS, the results can be saved "
        "directly to the RMS project",
    )
    save_results_to_disk: bool = Field(
        default=True,
        description="Results must be saved to disk for use in sim2seis setting etc",
    )
    save_intermediate_results: bool = Field(
        default=False,
        description="Intermediate results can be saved to a separate directory for "
        "QC. Intermediate results include effective mineral and fluid "
        "properties",
    )


class PemConfig(BaseModel):
    paths: SkipJsonSchema[PemPaths] = Field(
        default_factory=PemPaths,
        description="Default path settings exist, it is possible to override them, "
        "mostly relevant for input paths",
    )
    rock_matrix: RockMatrixProperties = Field(
        description="Settings related to effective mineral properties and rock "
        "physics model",
    )
    fluids: Fluids = Field(
        description="Settings related to fluid composition",
    )
    pressure: OverburdenPressureTrend | OverburdenPressureConstant = Field(
        default=OverburdenPressureTrend,
        description="Definition of overburden pressure model - constant or trend",
    )
    results: Results = Field(
        description="Flags for saving results of the PEM",
    )
    diff_calculation: Dict[str, List[Literal["ratio", "diff", "diffpercent"]]] = Field(
        description="Difference properties of the PEM can be calculated for the dates "
        "in the Eclipse `.UNRST` file. The settings decide which parameters "
        "difference properties will be generated for, and what kind of "
        "difference calculation is run - normal difference, percent "
        "difference or ratio"
    )
    global_params: SkipJsonSchema[FromGlobal | None] = Field(
        default=None,
    )

    @field_validator("paths", mode="before")
    def check_and_create_directories(cls, v: Dict, info: ValidationInfo):
        if v is None:
            return PemPaths()
        for key, path in v.items():
            if key == "rel_path_intermed_output" or key == "rel_path_output":
                os.makedirs(path, exist_ok=True)
            else:
                if not Path(path).exists():
                    raise ValueError(f"Directory {path} does not exist")
        return v

    @field_validator("diff_calculation", mode="before")
    def to_list(cls, v: Dict) -> Dict:
        v_keys = list(v.keys())
        v_val = list(v.values())
        for i, val_item in enumerate(v_val):
            if not isinstance(val_item, list):
                v_val[i] = [
                    val_item,
                ]
        return dict(zip(v_keys, v_val))

    # Add global parameters used in the PEM
    def update_with_global(self, global_params: dict):
        self.global_params = FromGlobal(**global_params)
        return self
