"""
Define RPM model types and their parameters
"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema
from typing_extensions import Annotated

from fmu.pem.pem_utilities.enum_defs import CoordinationNumberFunction, RPMType


class MineralProperties(BaseModel):
    bulk_modulus: float = Field(gt=1.0e9, lt=5.0e11, description="Unit: `Pa`")
    shear_modulus: float = Field(gt=1.0e9, lt=5.0e11, description="Unit: `Pa`")
    density: float = Field(gt=1.0e3, lt=1.0e4, description="Unit: `kg/m³`")


class CoordinationNumberPorBased(BaseModel):
    fcn: SkipJsonSchema[CoordinationNumberFunction] = Field(
        default="PorBased",
        description="Coordinate number is the number of grain-grain contacts. It is "
        "normally assumed to be a function of porosity for friable sand",
    )


class CoordinationNumberConstVal(BaseModel):
    fcn: SkipJsonSchema[CoordinationNumberFunction] = Field(
        default="ConstVal",
    )
    coordination_number: float = Field(
        default=9.0,
        gt=2.0,
        lt=16.0,
        description="In case of a constant value for the number of grain contacts, "
        "a value of 8-9 is common",
    )


class PatchyCementParams(BaseModel):
    upper_bound_cement_fraction: float = Field(
        default=0.1,
        description="There is an upper limit for the constant cement model, which "
        "is part of the Patchy Cement model. Values higher than 0.1 can "
        "lead to the model reaching saturation",
    )
    cement_fraction: float = Field(
        default=0.04,
        gt=0,
        le=0.1,
        description="Representative cement fraction for Patchy Cement should be chosen "
        "so that the model trend line goes through the median of the log "
        "values",
    )
    critical_porosity: float = Field(
        default=0.4,
        ge=0.3,
        le=0.5,
        description="Critical porosity is the porosity of the sands at the time of "
        "deposition, before any compaction",
    )
    shear_reduction: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Shear reduction is related to the fraction of tangential friction "
        "between grains. Shear reduction of 1 means frictionless contact, "
        "and 0 means full friction",
    )
    coordination_number_function: (
        CoordinationNumberPorBased | CoordinationNumberConstVal
    ) = Field(
        default_factory=CoordinationNumberPorBased,
        description="Coordinate number is the number of grain-grain contacts. It is "
        "normally assumed to be a function of porosity for friable sand",
    )


class TMatrixParams(BaseModel):
    t_mat_model_version: Literal["PETEC", "EXP"] = Field(
        description="When T Matrix model is calibrated and optimised based on well "
        "data, a selection is made on how much information will be "
        "available when the calibrated model is applied to a PEM model"
    )
    angle: float = Field(
        default=90.0,
        ge=0.0,
        lt=180.0,
        description="Angle between axis of symmetry and horizontal plane. A standard "
        "VTI medium will have 90 deg angle",
    )
    freq: float = Field(
        default=100.0,
        gt=0.0,
        description="Frequency of the acoustic signal in Hz. For seismic, a standard "
        "value of 100 is used. Sonic log or ultrasonic measurements will "
        "require a higher value",
    )
    perm: float = Field(
        default=100.0,
        gt=0.0,
        description="Permeability of the rock matrix in mD. A standard value of 100 mD "
        "is commonly used",
    )
    visco: float = Field(
        default=10.0,
        gt=0.0,
        description="Fluid viscosity in cP",
    )
    tau: float = Field(
        default=1.0e-7,
        description="A time factor for reaching equilibrium in fluid movement. Best "
        "left alone",
    )


class RhoRegressionMixin(BaseModel):
    rho_weights: List[float] = Field(
        default=[
            1.0,
        ],
        description="List of float values for polynomial regression for density "
        "based on porosity",
    )
    rho_regression: bool = Field(
        default=False,
        description="Matrix density is normally estimated from "
        "mineral composition and the density of each mineral. "
        "Setting this to True will estimate matrix "
        "density based on porosity alone. In that case, check the "
        "rho regression parameters",
    )


class VpVsRegressionParams(RhoRegressionMixin):
    vp_weights: List[float] = Field(
        default=None,
        description="List of float values for polynomial regression for Vp "
        "based on porosity",
    )
    vs_weights: List[float] = Field(
        default=None,
        description="List of float values for polynomial regression for Vs "
        "based on porosity",
    )
    mode: Literal["vp_vs"] = Field(
        default="vp_vs",
        description="Regression mode mode must be set to 'vp_vs' for "
        "estimation of Vp and Vs based on porosity",
    )


class KMuRegressionParams(RhoRegressionMixin):
    k_weights: List[float] = Field(
        default=None,
        description="List of float values for polynomial regression for bulk modulus "
        "based on porosity",
    )
    mu_weights: List[float] = Field(
        default=None,
        description="List of float values for polynomial regression for shear modulus "
        "based on porosity",
    )
    mode: Literal["k_mu"] = Field(
        default="k_mu",
        description="Regression mode mode must be set to 'k_mu' for "
        "estimation of bulk and shear modulus based on porosity",
    )


class RegressionModels(BaseModel):
    sandstone: VpVsRegressionParams | KMuRegressionParams = Field(
        description="Selection of model type for sandstone regression model"
    )
    shale: VpVsRegressionParams | KMuRegressionParams = Field(
        description="Selection of model type for shale regression model"
    )


class PatchyCementRPM(BaseModel):
    model_config = ConfigDict(title="Patchy Cement Model")
    model_name: Literal[RPMType.PATCHY_CEMENT]
    parameters: PatchyCementParams


class FriableRPM(BaseModel):
    model_config = ConfigDict(title="Friable Sand Model")
    model_name: Literal[RPMType.FRIABLE]
    parameters: PatchyCementParams


class TMatrixRPM(BaseModel):
    model_config = ConfigDict(title="T-Matrix Inclusion Model")
    model_name: Literal[RPMType.T_MATRIX]
    parameters: TMatrixParams


class RegressionRPM(BaseModel):
    model_config = ConfigDict(title="Regression Model")
    model_name: Literal[RPMType.REGRESSION]
    parameters: RegressionModels

