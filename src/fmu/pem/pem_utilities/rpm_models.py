"""
Define RPM model types and their parameters
"""

from typing import Any, Literal, Self

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema
from rock_physics_open.equinor_utilities.machine_learning_utilities import (
    ExponentialPressureModel,
    PolynomialPressureModel,
)
from rock_physics_open.sandstone_models import (
    friable_model_dry,
    patchy_cement_model_dry,
)

from fmu.pem.pem_utilities.enum_defs import (
    CoordinationNumberFunction,
    ParameterTypes,
    PhysicsPressureModelTypes,
    RegressionPressureModelTypes,
    RegressionPressureParameterTypes,
    RPMType,
)
from fmu.pem.pem_utilities.pem_class_definitions import EffectiveMineralProperties


class OptionalField(BaseModel):
    def __eq__(self, other):
        return other is None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return False

    model_config = ConfigDict(title="This field is optional")


class MineralProperties(BaseModel):
    bulk_modulus: float = Field(gt=1.0e9, lt=5.0e11, description="Unit: `Pa`")
    shear_modulus: float = Field(gt=1.0e9, lt=5.0e11, description="Unit: `Pa`")
    density: float = Field(gt=1.0e3, lt=1.0e4, description="Unit: `kg/m³`")


class FriableParams(BaseModel):
    """Friable sandstone model parameters."""

    model_config = ConfigDict(title="Friable Model Parameters")

    critical_porosity: float = Field(
        ge=0.3, le=0.5, default=0.4, description="Critical porosity"
    )
    coordination_number_function: str = Field(
        default="PorBased", description="Coordination number function"
    )
    coord_num: float = Field(
        default=9.0,
        description="Coordination number value."
        " This is normally only used in patchy cement model",
    )
    shear_reduction: float = Field(
        default=1.0, ge=0, le=1, description="Shear reduction factor"
    )
    model_max_pressure: float = Field(
        default=40,  # MPa
        description="Maximum pressure value for the friable sandstone model used as"
        " pressure sensitive model",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert friable parameters to dictionary."""
        return {
            "critical_porosity": self.critical_porosity,
            "coordination_number_function": self.coordination_number_function,
            "coord_num": self.coord_num,
            "shear_reduction": self.shear_reduction,
            "model_max_pressure": self.model_max_pressure,
        }


class PatchyCementParams(FriableParams):
    """Patchy cement model parameters."""

    model_config = ConfigDict(title="Patchy Cement Parameters")

    cement_fraction: float = Field(gt=0, le=0.1, description="Cement volume fraction")

    def to_dict(self) -> dict[str, Any]:
        """Convert patchy cement parameters to dictionary."""
        base_dict = super().to_dict()
        base_dict["cement_fraction"] = self.cement_fraction
        return base_dict


class TMatrixParams(BaseModel):
    t_mat_model_version: Literal["PETEC", "EXP"] = Field(
        default="PETEC",
        description="When T Matrix model is calibrated and optimised based on well "
        "data, a selection is made on how much information will be "
        "available when the calibrated model is applied to a PEM model",
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


class RhoRegressionParams(BaseModel):
    rho_weights: list[float] = Field(
        description="\n\n".join(
            [
                "Polynomial coefficients for matrix density as a function of porosity:",
                "`rho(phi) = w1 + w2*phi + w3*phi^2 + ... + wn*phi^n`",
                "List order: `[w1, w2, w3, ..., wn]`",
                "where `phi` is porosity (fraction) and `rho` is in kg/m³.",
            ]
        )
    )
    rho_model: bool = Field(
        default=False,
        description="Matrix density is normally estimated from "
        "mineral composition and the density of each mineral. "
        "Setting this to True will estimate matrix "
        "density based on porosity alone. In that case, weights "
        "for the polynomial expression must be provided.",
    )


class VpVsRegressionParams(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    vp_weights: list[float] = Field(
        description="\n\n".join(
            [
                "Polynomial coefficients for vp as a function of porosity:",
                "`vp(phi) = w1 + w2*phi + w3*phi^2 + ... + wn*phi^n`",
                "List order: `[w1, w2, w3, ..., wn]`",
                "where `phi` is porosity (fraction) and `vp` is in m/s.",
            ]
        ),
    )
    vs_weights: list[float] = Field(
        description="\n\n".join(
            [
                "Polynomial coefficients for vs as a function of porosity:",
                "`vs(phi) = w1 + w2*phi + w3*phi^2 + ... + wn*phi^n`",
                "List order: `[w1, w2, w3, ..., wn]`",
                "where `phi` is porosity (fraction) and `vs` is in m/s.",
            ]
        ),
    )
    mode: Literal["vp_vs"] = Field(
        default="vp_vs",
        description="Mode for Vp/Vs regression. 'vp_vs' indicates that both "
        "Vp and Vs are modeled as polynomial functions of porosity "
        "using the provided coefficients.",
    )
    rho_model: OptionalField | RhoRegressionParams = Field(
        description="Optional model for rho regression. ",
        default_factory=OptionalField,
    )


class KMuRegressionParams(BaseModel):
    k_weights: list[float] = Field(
        description="\n\n".join(
            [
                "Polynomial coefficients for bulk modulus as a function of porosity:",
                "`k(phi) = w1 + w2*phi + w3*phi^2 + ... + wn*phi^n`",
                "List order: `[w1, w2, w3, ..., wn]`",
                "where `phi` is porosity (fraction) and `k` is in Pa.",
            ]
        ),
    )
    mu_weights: list[float] = Field(
        description="\n\n".join(
            [
                "Polynomial coefficients for shear modulus as a function of porosity:",
                "`mu(phi) = w1 + w2*phi + w3*phi^2 + ... + wn*phi^n`",
                "List order: `[w1, w2, w3, ..., wn]`",
                "where `phi` is porosity (fraction) and `mu` is in Pa.",
            ]
        ),
    )
    mode: Literal["k_mu"] = Field(
        default="k_mu",
        description="Regression mode mode must be set to 'k_mu' for "
        "estimation of bulk and shear modulus based on porosity",
    )
    rho_model: OptionalField | RhoRegressionParams = Field(
        description="Optional model for rho regression. "
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
    parameters: FriableParams


class TMatrixRPM(BaseModel):
    model_config = ConfigDict(title="T-Matrix Inclusion Model")
    model_name: Literal[RPMType.T_MATRIX]
    parameters: TMatrixParams


class RegressionRPM(BaseModel):
    model_config = ConfigDict(title="Regression Model")
    model_name: Literal[RPMType.REGRESSION]
    parameters: RegressionModels


class ExpParams(BaseModel):
    """Exponential pressure model parameters."""

    model_config = ConfigDict(title="Exponential Parameters")

    a_factor: float = Field(description="Exponential coefficient A")
    b_factor: float = Field(description="Exponential coefficient B")

    def to_dict(self) -> dict[str, Any]:
        """Convert exponential parameters to dictionary."""
        return {
            "a_factor": self.a_factor,
            "b_factor": self.b_factor,
            "model_max_pressure": self.model_max_pressure,
        }

    model_max_pressure: float = Field(
        default=40,  # MPa
        description="Maximum pressure value for the exponential pressure"
        " sensitive model",
    )


class PolyParams(BaseModel):
    """Polynomial pressure model parameters."""

    model_config = ConfigDict(title="Polynomial Parameters")

    weights: list[float] = Field(description="Polynomial coefficients")

    def to_dict(self) -> dict[str, Any]:
        """Convert polynomial parameters to dictionary."""
        return {
            "weights": self.weights,
            "model_max_pressure": self.model_max_pressure,
        }

    model_max_pressure: float = Field(
        default=40,  # MPa
        description="Maximum pressure value for the polynomial pressure"
        " sensitive model",
    )


class RegressionPressureSensitivity(BaseModel):
    """
    Pressure sensitivity model for rock physics modeling.

    This model handles different pressure-dependent parameter types (VP/VS or K/MU)
    using various model types (exponential, polynomial.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, title="Regression Pressure Sensitivity"
    )
    # Selections that cover model types Exponential/Polynomial and parameter types
    # VP-VS or K-MU
    model_type: RegressionPressureModelTypes = Field(
        description="Type of pressure model"
    )
    mode: RegressionPressureParameterTypes = Field(
        description="Parameter mode (VP/VS or K/MU)"
    )

    # Parameter containers
    parameters: dict[ParameterTypes, ExpParams | PolyParams]

    @field_validator("model_type", mode="before")
    @classmethod
    def check_model_type(cls, v: str, info: ValidationInfo) -> str:
        if v in list(RegressionPressureModelTypes):
            return v
        raise ValueError(
            f"unknown physics pressure model type: {v}\n"
            f"Should be one of {list(RegressionPressureModelTypes)}"
        )

    @field_validator("mode", mode="before")
    @classmethod
    def check_mode(cls, v: str, info: ValidationInfo) -> str:
        if v in list(RegressionPressureParameterTypes):
            return v
        raise ValueError(
            f"unknown physics pressure model type: {v}\n"
            + f"Should be one of {list(RegressionPressureParameterTypes)}"
        )

    @field_validator("parameters", mode="before")
    @classmethod
    def check_parameters(cls, v: dict, info: ValidationInfo) -> str:
        for key, value in v.items():
            if key not in list(ParameterTypes):
                raise ValueError(f"unknown pressure parameter: {key}")
            if not isinstance(value, (ExpParams, PolyParams)):
                raise ValueError(f"unknown pressure parameter type: {value}")
        return v

    @model_validator(mode="after")
    def _validate_model_configuration(self) -> Self:
        """Validate model configuration and parameter consistency."""
        if self.mode == RegressionPressureParameterTypes.VP_VS and not (
            self.parameters.get(ParameterTypes.VP)
            and self.parameters.get(ParameterTypes.VS)
        ):
            raise ValueError("VP/VS mode requires both vp_parameters and vs_parameters")
        if self.mode == RegressionPressureParameterTypes.K_MU and not (
            self.parameters.get(ParameterTypes.K)
            and self.parameters.get(ParameterTypes.MU)
        ):
            raise ValueError("K/MU mode requires both k_parameters and mu_parameters")
        """Validate model configuration and parameter consistency."""
        for key, value in self.parameters.items():
            if self.model_type == RegressionPressureModelTypes.POLYNOMIAL and (
                not isinstance(value, PolyParams)
            ):
                raise ValueError(
                    "model parameter mismatch, expected polynomial weights"
                )
            if self.model_type == RegressionPressureModelTypes.EXPONENTIAL and (
                not isinstance(value, ExpParams)
            ):
                raise ValueError(
                    "model parameter mismatch, expected exponential parameters"
                )
        return self

    def _get_ml_models(self):
        ml_models = {}
        for key, value in self.parameters.items():
            if self.model_type == RegressionPressureModelTypes.POLYNOMIAL:
                ml_models[key] = PolynomialPressureModel(**value.to_dict())
            if self.model_type == RegressionPressureModelTypes.EXPONENTIAL:
                ml_models[key] = ExponentialPressureModel(**value.to_dict())
        return ml_models

    def predict_elastic_properties(
        self,
        prop1: np.ndarray,
        prop2: np.ndarray,
        in_situ_press: np.ndarray,
        depl_press: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Predict depleted elastic properties based on pressure change.

        Args:
            prop1: First elastic property (K or VP depending on mode)
            prop2: Second elastic property (MU or VS depending on mode)
            in_situ_press: In-situ pressure array
            depl_press: Depletion pressure array

        Returns:
            Tuple of depleted (prop1, prop2) arrays
        """
        models = self._get_ml_models()

        # Determine parameter keys based on mode
        key1, key2 = (
            (ParameterTypes.K, ParameterTypes.MU)
            if self.mode == RegressionPressureParameterTypes.K_MU
            else (ParameterTypes.VP, ParameterTypes.VS)
        )
        # The model has set a maximum depletion, make sure that the depleted
        # pressure does not exceed this. Maximum depletion is given in MPa,
        # must be converted to Pa
        max_depl = 1.0e6 * min(
            self.parameters[key1].model_max_pressure,
            self.parameters[key2].model_max_pressure,
        )
        depl_press = in_situ_press + np.minimum(depl_press - in_situ_press, max_depl)

        # Build input array for first property
        input_array = np.concatenate(
            (
                prop1.reshape(-1, 1),
                in_situ_press.reshape(-1, 1),
                depl_press.reshape(-1, 1),
            ),
            axis=1,
        )
        prop1_depl = models[key1].predict_abs(input_array, case="depl")

        # Reuse array for second property
        input_array[:, 0] = prop2
        prop2_depl = models[key2].predict_abs(input_array, case="depl")

        return prop1_depl, prop2_depl


class PhysicsModelPressureSensitivity(BaseModel):
    """
    Pressure sensitivity modelling using theoretical rock physics models.

    Parameter types are determined by the model type. At this point, friable dry
    rock model and patchy cement dry rock model are available, and both of them
    are based on moduli (k, mu)
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, title="Physics Model Pressure Sensitivity"
    )
    model_type: PhysicsPressureModelTypes = Field(description="Type of pressure model")
    parameters: PatchyCementParams | FriableParams = Field(
        description="Dry rock model parameters"
    )

    @field_validator("model_type", mode="before")
    @classmethod
    def check_model_type(cls, v: str, info: ValidationInfo) -> str:
        if v in list(PhysicsPressureModelTypes):
            return v
        raise ValueError(
            f"unknown physics pressure model type: {v}\n"
            f"Should be one of {list(PhysicsPressureModelTypes)}"
        )

    @model_validator(mode="after")
    def _validate_model_configuration(self) -> Self:
        if self.model_type == PhysicsPressureModelTypes.FRIABLE and (
            not isinstance(self.parameters, FriableParams)
        ):
            raise ValueError("Mismatch between Friable model and parameter set")
        if self.model_type == PhysicsPressureModelTypes.PATCHY_CEMENT and (
            not isinstance(self.parameters, PatchyCementParams)
        ):
            raise ValueError("Mismatch between Patchy cement model and parameter set")
        return self

    def predict_elastic_properties(
        self,
        k_dry: np.ndarray,
        mu_dry: np.ndarray,
        poro: np.ndarray,
        min_prop: EffectiveMineralProperties,
        in_situ_press: np.ndarray,
        depl_press: np.ndarray,
        cem_prop: EffectiveMineralProperties | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        # The only differences in inputs and parameters between friable model and
        # patchy cement model are the parameter cement fraction and the cement
        # mineral properties.
        if (
            cem_prop is None
            and self.model_type == PhysicsPressureModelTypes.PATCHY_CEMENT
        ):
            raise ValueError("patchy cement model requires cement mineral properties")

        # To please the IDE ...
        k_in_situ = None
        mu_in_situ = None
        k_depl = None
        mu_depl = None

        # The model has set a maximum depletion, make sure that the depleted pressure
        # does not exceed this. Maximum depletion is given in MPa, must be converted
        # to Pa
        max_depl = 1.0e6 * self.parameters.model_max_pressure
        depl_press = in_situ_press + np.minimum(depl_press - in_situ_press, max_depl)

        if self.model_type == PhysicsPressureModelTypes.FRIABLE:
            k_in_situ, mu_in_situ = friable_model_dry(
                k_min=min_prop.bulk_modulus,
                mu_min=min_prop.shear_modulus,
                phi=poro,
                p_eff=in_situ_press,
                phi_c=self.parameters.critical_porosity,
                coord_num_func=self.parameters.coordination_number_function,
                n=self.parameters.coord_num,
                shear_red=self.parameters.shear_reduction,
            )
            k_depl, mu_depl = friable_model_dry(
                k_min=min_prop.bulk_modulus,
                mu_min=min_prop.shear_modulus,
                phi=poro,
                p_eff=depl_press,
                phi_c=self.parameters.critical_porosity,
                coord_num_func=self.parameters.coordination_number_function,
                n=self.parameters.coord_num,
                shear_red=self.parameters.shear_reduction,
            )
        if self.model_type == PhysicsPressureModelTypes.PATCHY_CEMENT:
            k_in_situ, mu_in_situ, _ = patchy_cement_model_dry(
                k_min=min_prop.bulk_modulus,
                mu_min=min_prop.shear_modulus,
                rho_min=min_prop.density,
                k_cem=cem_prop.bulk_modulus,
                mu_cem=cem_prop.shear_modulus,
                rho_cem=cem_prop.density,
                phi=poro,
                p_eff=in_situ_press,
                frac_cem=self.parameters.cement_fraction,
                phi_c=self.parameters.critical_porosity,
                coord_num_func=self.parameters.coordination_number_function,
                n=self.parameters.coord_num,
                shear_red=self.parameters.shear_reduction,
            )
            k_depl, mu_depl, _ = patchy_cement_model_dry(
                k_min=min_prop.bulk_modulus,
                mu_min=min_prop.shear_modulus,
                rho_min=min_prop.density,
                k_cem=cem_prop.bulk_modulus,
                mu_cem=cem_prop.shear_modulus,
                rho_cem=cem_prop.density,
                phi=poro,
                p_eff=depl_press,
                frac_cem=self.parameters.cement_fraction,
                phi_c=self.parameters.critical_porosity,
                coord_num_func=self.parameters.coordination_number_function,
                n=self.parameters.coord_num,
                shear_red=self.parameters.shear_reduction,
            )
        # Should not be necessary to test if there is an erroneous model type,
        # that would have been caught in the model validation
        k_dry = k_dry * (k_depl / k_in_situ)
        mu_dry = mu_dry * (mu_depl / mu_in_situ)
        return k_dry, mu_dry
