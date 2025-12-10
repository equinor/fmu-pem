import os
from datetime import date
from pathlib import Path
from typing import Any, Self

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
    DifferenceAttribute,
    DifferenceMethod,
    FluidMixModel,
    GasModels,
    MineralMixModel,
    OverburdenPressureTypes,
    RPMType,
    TemperatureMethod,
)
from .fipnum_pvtnum_utilities import (
    detect_overlaps,
    input_num_string_to_list,
)
from .rpm_models import (
    FriableRPM,
    MineralProperties,
    OptionalField,
    PatchyCementRPM,
    PhysicsModelPressureSensitivity,
    RegressionPressureSensitivity,
    RegressionRPM,
    TMatrixRPM,
)

REGEX_FIPNUM_PVTNUM = r"^(?:\*|(?:\d+(?:-\d+)?)(?:,(?:\d+(?:-\d+)?))*)$"


class EclipseFiles(BaseModel):
    rel_path_simgrid: DirectoryPath = Field(
        default=Path("../../sim2seis/input/pem"),
        description="Relative path of the simulation grid",
    )
    egrid_file: Path = Field(
        default=Path("ECLIPSE.EGRID"),
        description="Name of Eclipse EGRID file",
    )
    init_property_file: Path = Field(
        default=Path("ECLIPSE.INIT"),
        description="Name of Eclipse INIT file",
    )
    restart_property_file: Path = Field(
        default=Path("ECLIPSE.UNRST"),
        description="Name of Eclipse UNRST file",
    )

    @model_validator(mode="after")
    def check_fractions(self) -> Self:
        for sim_file in [
            self.egrid_file,
            self.init_property_file,
            self.restart_property_file,
        ]:
            full_name = self.rel_path_simgrid / sim_file
            if not full_name.exists():
                raise FileNotFoundError(f"fraction prop file is missing: {full_name}")
        return self


class FractionFiles(BaseModel):
    rel_path_fractions: DirectoryPath = Field(
        default=Path("../../sim2seis/input/pem"),
        description="Directory for volume fractions",
    )
    fractions_prop_file_names: list[Path] = Field(description="Volume fractions")
    fractions_are_mineral_fraction: bool = Field(
        default=False,
        description="Fractions can either be mineral fractions or volume fractions."
        "If they are mineral fractions,the sum of fractions and a"
        "complement is 1.0. If they are volume fractions, the sum of"
        "fractions, a complement and porosity is 1.0."
        "Default value is False.",
    )

    @model_validator(mode="after")
    def check_fractions(self) -> Self:
        for frac_prop in self.fractions_prop_file_names:
            full_fraction_prop = self.rel_path_fractions / frac_prop
            if not full_fraction_prop.exists():
                raise FileNotFoundError(
                    f"fraction prop file is missing: {full_fraction_prop}"
                )
        return self


class ZoneRegionMatrixParams(BaseModel):
    fipnum: str = Field(
        description="Each grid cell in a reservoir model is assigned a FIPNUM "
        "integer, where each FIPNUM integer represents a combination of zone and "
        "segment. `fmu-pem` reuses FIPNUM by letting you define the FIPNUM integers "
        "where a defined rock matrix should be used. Explicit definitions like "
        "`1-10,15` matches the FIPNUMs "
        "`1, 2, ..., 10, 15`. By doing it this way you can have different "
        "rock physics models for e.g. individual zones and segments. "
        "Leaving this field empty means that all zones and segments are"
        "treated as one",
        pattern=REGEX_FIPNUM_PVTNUM,
    )
    model: FriableRPM | PatchyCementRPM | TMatrixRPM | RegressionRPM = Field(
        description="Selection of rock physics model and parameter set",
    )
    pressure_sensitivity: bool = Field(
        default=True,
        description="All RPM models can be run with or without pressure sensitivity.",
    )
    pressure_sensitivity_model: (
        RegressionPressureSensitivity | PhysicsModelPressureSensitivity | OptionalField
    ) = Field(
        default=OptionalField(),
        description="For most RPM models, it is possible to choose between a "
        "regression based pressure sensitivity model from plug measurements "
        "or a theoretical one. For `T Matrix` model a calibrated model is set "
        "as default, and any model selection in this interface will be disregarded.",
    )

    @field_validator("model", mode="before")
    @classmethod
    def model_check(cls, v: dict, info: ValidationInfo) -> dict:
        if v["model_name"] not in list(RPMType):
            raise ValueError(f"unknown model: {v['model_name']}")
        return v


class RockMatrixProperties(BaseModel):
    """Configuration for rock matrix properties.

    Contains parameters necessary for defining matrix properties for
    different rock types, including sandstones, carbonates,
    and other lithologies.
    """

    model_config = ConfigDict(title="Rock matrix properties:")

    zone_regions: list[ZoneRegionMatrixParams] = Field(
        description="Per-zone or -region parameters"
    )
    minerals: dict[str, MineralProperties] = Field(
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
        },
        description="Define minerals relevant for the field. Default values are set "
        "for `shale`, `quartz`, `calcite` and `dolomite` (you can't "
        "delete these minerals, but you can override their default values and/or "
        "ignore their definition).",
    )
    cement: str = Field(
        default="quartz",
        description="For the patchy cement model, the cement mineral must be defined, "
        "and its properties must be defined in the mineral properties' "
        "dictionary",
    )
    volume_fractions: FractionFiles = Field(
        description="Choice of volume fraction files. Volume fractions are defined"
        "in the geomodel, but they must be resampled to the simulator grid"
        "when used in PEM",
    )
    fraction_names: list[str] = Field(
        description="Fraction names must match the names in the volume fractions file",
    )
    fraction_minerals: list[str] = Field(
        description="The list of minerals matching the fractions' definition. Each "
        "mineral must be defined in the mineral properties dictionary"
    )
    shale_fractions: list[str] = Field(
        description="List the fractions that should be regarded as non-net reservoir"
    )
    complement: str = Field(
        description="For grid cells where the sum of the fractions does not add "
        "up to 1.0, the remainder is filled with the complement mineral, "
        "e.g. when using net-to-gross instead of volume fractions"
    )
    mineral_mix_model: MineralMixModel = Field(
        default="voigt-reuss-hill",
        description="Effective medium model selection: either "
        "`hashin-shtrikman-average` or `voigt-reuss-hill`",
    )

    @field_validator("zone_regions", mode="before")
    @classmethod
    def fipnum_check(cls, v: list[dict]) -> list[dict]:
        """
        At this point in time we don't have access to the simulator init file,
        so we just have to guess that it contains all numbers from 1 to the
        max number given in the strings. Validate that there are no overlaps.

        Validation must be made here, not under individual ZoneRegion objects
        to get the combined information in all ZoneRegion groups.

        Earlier wildcard symbol was '*'. Empty string (new wildcard) is
        changed into '*' for backward compatibility
        """
        fipnum_strings = [rock["fipnum"] for rock in v]
        # Enforce single wildcard usage
        if any(s is None or not str(s).strip() or s == "*" for s in fipnum_strings):
            if len(v) > 1:
                raise ValueError(
                    "Setting wildcard ('*' or empty string) means that "
                    "all FIPNUM should be treated as one group, no "
                    "other groups can be specified"
                )
            # Enforce old style wildcard
            v[0]["fipnum"] = "*"
            return v
        # Build temporary range to detect overlaps
        tmp_max = 1
        tmp_num_array = [1]
        for num_string in fipnum_strings:
            num_array = input_num_string_to_list(num_string, tmp_num_array)
            if tmp_max < max(num_array):
                tmp_max = max(num_array)
                tmp_num_array = list(range(1, tmp_max + 1))
        if detect_overlaps(fipnum_strings, tmp_num_array):
            raise ValueError(f"Overlaps in group definitions: {fipnum_strings}")
        return v

    @field_validator("cement", mode="before")
    def cement_check(cls, v: str, info: ValidationInfo) -> str:
        if v not in info.data["minerals"]:
            raise ValueError(f'{__file__}: cement mineral "{v}" not listed in minerals')
        return v

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
    def complement_fraction_check(cls, v: str, info: ValidationInfo) -> str:
        if v not in info.data["minerals"]:
            raise ValueError(
                f'{__file__}: shale fraction mineral "{v}" not listed in fraction '
                f"minerals"
            )
        return v

    @model_validator(mode="after")
    def _validate_rock_matrix_properties(self):
        for frac_min in self.fraction_minerals:
            if frac_min not in self.minerals:
                raise ValueError(
                    f"{__file__}: volume fraction mineral {frac_min} is not defined"
                )
        for fipnum_group in self.zone_regions:
            if fipnum_group.model.model_name != RPMType.T_MATRIX and (
                fipnum_group.pressure_sensitivity
                and not fipnum_group.pressure_sensitivity_model
            ):
                raise ValueError("a model is required when pressure sensitivity is set")
        return self


# Pressure
class OverburdenPressureTrend(BaseModel):
    type: SkipJsonSchema[OverburdenPressureTypes] = "trend"
    fipnum: str = Field(
        description="Each grid cell in a reservoir model is assigned a FIPNUM "
        "integer. `fmu-pem` reuses FIPNUM by letting you define the FIPNUM "
        "integers where a given overburden pressure should be used. Explicit "
        "definitions like `1-10,15` matches the PVTNUMs `1, 2, ..., 10, 15`. "
        "Leaving this field empty means that all zones and segments are"
        "treated as one",
        pattern=REGEX_FIPNUM_PVTNUM,
    )
    intercept: float = Field(description="Intercept in pressure depth trend")
    gradient: float = Field(description="Gradient in pressure depth trend")


class OverburdenPressureConstant(BaseModel):
    type: SkipJsonSchema[OverburdenPressureTypes] = "constant"
    fipnum: str = Field(
        description="Each grid cell in a reservoir model is assigned a FIPNUM "
        "integer. `fmu-pem` reuses FIPNUM by letting you define the FIPNUM "
        "integers where a given overburden pressure should be used. Explicit "
        "definitions like `1-10,15` matches the FIPNUMs `1, 2, ..., 10, 15`. "
        "Leaving this field empty means that all zones and segments are"
        "treated as one",
        pattern=REGEX_FIPNUM_PVTNUM,
    )
    value: float = Field(description="Constant pressure")


# Fluids
class Brine(BaseModel):
    salinity: float = Field(
        default=35000.0,
        gt=0.0,
        description="Salinity of brine, with unit `ppm` (parts per million)."
        "The composition (NaCl, CaCl2, KCl) is of secondary"
        " importance, unless the salinity is extremely high.",
    )
    perc_na: float = Field(
        ge=0.0,
        le=100.0,
        default=100.0,
        description="Percentage of `NaCl` in the dissolved salts in brine",
    )
    perc_ca: float = Field(
        ge=0.0,
        le=100.0,
        default=0.0,
        description="Percentage of `CaCl2` in the dissolved salts in brine",
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
    method: FluidMixModel = "wood"


class MixModelBrie(BaseModel):
    method: FluidMixModel = "brie"
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


class SalinityFromSim(BaseModel):
    enabled: bool = False

    def __bool__(self):
        return self.enabled

    model_config = ConfigDict(title="Salinity from SIM")


class PVTZone(BaseModel):
    pvtnum: str = Field(
        description="Each grid cell in a reservoir model is assigned a PVTNUM "
        "integer. `fmu-pem` reuses PVTNUM by letting you define the PVTNUM "
        "integers where a given fluid definition should be used. Explicit "
        "definitions like `1-10,15` matches the PVTNUMs `1, 2, ..., 10, 15`. "
        "Leaving this field empty means that all PVTNUM zones are treated as one",
        pattern=REGEX_FIPNUM_PVTNUM,
    )
    brine: Brine = Field(
        description="Brine model parameters.",
    )
    oil: Oil = Field(
        description="Oil model parameters. Note that GOR (gas-oil ratio) is read from"
        " eclipse restart file"
    )
    # Note that CO2 does not require a separate definition here, as it's properties only
    # depend on temperature and pressure
    gas: Gas = Field(description="Gas model parameters")
    condensate: OptionalField | Oil = Field(
        title="Condensate properties",
        description="Condensate model requires a similar set of parameters as"
        "the oil model, this is an optional setting for condensate"
        " cases",
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
    # Temperature may be set per zone
    temperature: ConstantTemperature | TemperatureFromSim = Field(
        description="In most cases it is sufficient with a constant temperature "
        "setting for the reservoir. If temperature is modelled in the "
        "simulation model, it is preferred to use that"
    )

    @model_validator(mode="after")
    def check_fluid_type(self) -> Self:
        if self.calculate_condensate and not INTERNAL_EQUINOR:
            raise NotImplementedError(
                "Missing model for condensate, proprietary model required"
            )
        return self


class Fluids(BaseModel):
    pvt_zones: list[PVTZone] = Field(
        description="Define fluid parameters for each phase in each PVT zone "
        "or group of PVT zones"
    )
    fluid_mix_method: MixModelWood | MixModelBrie = Field(
        default_factory=MixModelWood,
        description="Selection between Wood's or Brie model. Wood's model gives more "
        "radical response to adding small amounts of gas in brine or oil",
    )
    # Handling of salinity will be a common factor, not zone-based
    salinity_from_sim: SalinityFromSim = Field(
        default_factory=SalinityFromSim,
        description="In most cases it is sufficient with a constant salinity "
        "setting for the reservoir, unless there is large contrast"
        "between formation water and injected water. If salinity is "
        "modelled in the simulation model, it is preferred to use that",
    )
    co2_model: CO2Models = Field(
        default="span_wagner",
        description="Selection of model for CO₂ properties, `span_wagner` equation "
        "of state model or `flag`. Note that access to flag model depends "
        "on licence",
    )

    @field_validator("pvt_zones", mode="before")
    @classmethod
    def pvtnum_check(cls, v: list[dict]) -> list[dict]:
        """
        At this point in time we don't have access to the simulator init file,
        so we just have to guess that it contains all numbers from 1 to the
        max number given in the strings. Validate that there are no overlaps.

        Validation must be made here, not under individual PVTZone objects
        to get the combined information in all PVTZone groups.

        Earlier wildcard symbol was '*'. Empty string (new wildcard) is
        changed into '*' for backward compatibility
        """
        pvtnum_strings = [zone["pvtnum"] for zone in v]
        # Enforce single wildcard usage
        if any(s is None or not str(s).strip() or s == "*" for s in pvtnum_strings):
            if len(v) > 1:
                raise ValueError(
                    "Setting wildcard ('*' or empty string) means that "
                    "all PVTNUM should be treated as one group, no "
                    "other groups can be specified"
                )
            # Enforce old style wildcard
            v[0]["pvtnum"] = "*"
            return v
        # Build temporary range to detect overlaps
        tmp_max = 1
        tmp_num_array = [1]
        for num_string in pvtnum_strings:
            nums = input_num_string_to_list(num_string, tmp_num_array)
            m = max(nums)
            if m > tmp_max:
                tmp_max = m
                tmp_num_array = list(range(1, tmp_max + 1))
        if detect_overlaps(pvtnum_strings, tmp_num_array):
            raise ValueError(f"Overlaps in PVT zone definitions: {pvtnum_strings}")
        return v


def possible_date_string(date_strings: list[str]) -> bool:
    """
    Validate a list of date strings in YYYYMMDD format.

    Args:
        date_strings: list of strings to validate

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
    seis_dates: list[str]
    diff_dates: list[list[str]]
    global_config: dict[str, Any]

    @field_validator("seis_dates", mode="before")
    def check_date_string(cls, v: list[str]) -> list[str]:
        possible_date_string(v)
        return v

    @field_validator("diff_dates", mode="before")
    def check_diffdate_string(cls, v: list[list[str]]) -> list[list[str]]:
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
    eclipse_files: EclipseFiles
    rock_matrix: RockMatrixProperties = Field(
        description="Settings related to effective mineral properties and rock "
        "physics model",
    )
    alternative_fipnum_name: SkipJsonSchema[str] = Field(
        default="fipnum".upper(),  # Should be upper case
        description="If it is needed to deviate from Equinor standard to use "
        "FIPNUM for zone/region class indicator",
    )
    fluids: Fluids = Field(
        description="Values for brine, oil and gas are required, but only the fluid "
        "phases that are present in the simulation model will in practice be used in "
        "calculation of effective fluid properties. You can have multiple fluid PVT "
        "definitions, representing e.g. different regions and/or zones in your model.",
    )
    pressure: list[OverburdenPressureTrend | OverburdenPressureConstant] = Field(
        default_factory=OverburdenPressureTrend,
        description="Definition of overburden pressure model - constant or trend",
    )
    results: Results = Field(
        description="Flags for saving results of the PEM",
    )
    diff_calculation: dict[DifferenceAttribute, list[DifferenceMethod]] = Field(
        description="Difference properties of the PEM can be calculated for the dates "
        "in the Eclipse `.UNRST` file. The settings decide which parameters "
        "difference properties will be generated for, and what kind of "
        "difference calculation is run - normal difference (`diff`), percent "
        "difference (`diffperc`) or ratio (`ratio`). Multiple kinds of differences "
        "can be estimated for each parameter"
    )
    global_params: SkipJsonSchema[FromGlobal | None] = Field(
        default=None,
    )

    @field_validator("paths", mode="before")
    def check_and_create_directories(cls, v: dict, info: ValidationInfo):
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
    def to_list(cls, v: dict) -> dict:
        v_keys = [key.lower() for key in v]
        v_val = list(v.values())
        for i, val_item in enumerate(v_val):
            if not isinstance(val_item, list):
                v_val[i] = [
                    val_item,
                ]
            v_val[i] = [v.lower() for v in v_val[i]]
        return dict(zip(v_keys, v_val))

    # Add global parameters used in the PEM
    def update_with_global(self, global_params: dict):
        self.global_params = FromGlobal(**global_params)
        return self
