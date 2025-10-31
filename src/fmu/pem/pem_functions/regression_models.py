"""Regression models for saturated sandstones

Regression based on polynomial models for saturated sandstones. The models are
based on porosity polynomials to estimate either Vp and Vs, or K and Mu.
"""

import numpy as np
import numpy.typing as npt
from rock_physics_open.equinor_utilities.std_functions import (
    gassmann,
    hashin_shtrikman_average,
    moduli,
    velocity,
    voigt_reuss_hill,
)

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    EffectiveMineralProperties,
    PressureProperties,
    RockMatrixProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)
from fmu.pem.pem_utilities.enum_defs import (
    MineralMixModel,
    ParameterTypes,
    PhysicsPressureModelTypes,
)
from fmu.pem.pem_utilities.rpm_models import (
    KMuRegressionParams,
    VpVsRegressionParams,
)

from .pressure_sensitivity import (
    apply_dry_rock_pressure_sensitivity_model,
)


def gen_regression(
    porosity: np.ndarray, polynom_weights: list | np.ndarray
) -> np.ndarray:
    """Regression model for Vp

    Args:
        porosity: porosity [fraction]
        polynom_weights: weights for the polynomial regression model

    Returns:
        Vp [m/s]
    """
    pol = np.polynomial.Polynomial(polynom_weights)
    poly_val: np.ndarray = pol(porosity)
    return poly_val


def dry_rock_regression(
    porosity: npt.NDArray[np.float64],
    rho_min: npt.NDArray[np.float64],
    params: VpVsRegressionParams | KMuRegressionParams,
) -> tuple[npt.NDArray[np.float64], ...]:
    """
    Calculates dry rock properties based on porosity and polynomial weights.

    Args:
        porosity: An array of porosity values.
        rho_min: An array of mineral density values.
        params: PemConfig object containing the regression model parameters.

    Returns:
        A dictionary with keys corresponding to the calculated properties and
        their values.

    Raises:
        ValueError: If an invalid mode is provided or necessary weights for
        the selected mode are missing.
    """
    if not params.rho_model:
        # rho_model = False, use mineral density
        rho_dry = rho_min * (1 - porosity)
    else:
        rho_dry = gen_regression(porosity, params.rho_model.rho_weights)

    if (
        params.mode == "vp_vs"
        and params.vp_weights is not None
        and params.vs_weights is not None
    ):
        vp_dry = gen_regression(porosity, params.vp_weights)
        vs_dry = gen_regression(porosity, params.vs_weights)
        k_dry, mu = moduli(vp_dry, vs_dry, rho_dry)
    elif (
        params.mode == "k_mu"
        and params.k_weights is not None
        and params.mu_weights is not None
    ):
        k_dry = gen_regression(porosity, params.k_weights)
        mu = gen_regression(porosity, params.mu_weights)
    else:
        raise ValueError("Invalid mode or missing weights for the selected mode.")

    return k_dry, mu, rho_dry


def run_regression_models(
    matrix: EffectiveMineralProperties,
    fluid_properties: list[EffectiveFluidProperties],
    porosity: np.ma.MaskedArray,
    pressure: list[PressureProperties],
    rock_matrix: RockMatrixProperties,
    vsh: np.ma.MaskedArray | None = None,
) -> list[SaturatedRockProperties]:
    """Run regression models for saturated rock properties.

    Args:
        matrix: Effective mineral properties containing bulk modulus (k) [Pa],
            shear modulus (mu) [Pa] and density (rho_sat) [kg/m3]
        fluid_properties: list of fluid properties,
            each containing bulk modulus (k) [Pa] and density (rho_sat) [kg/m3]
        porosity: Porosity as a masked array [fraction]
        pressure: list of pressure properties containing effective pressure values
            [bar] following Eclipse reservoir simulator convention
        rock_matrix: rock matrix properties
        vsh: Volume of shale as a masked array [fraction], optional

    Returns:
        list[SaturatedRockProperties]: Saturated rock properties for each time step.
            Only fluid properties change between time steps in this model.
    """

    saturated_props = []
    tmp_pres_over = None
    tmp_pres_form = None
    tmp_pres_depl = None

    if vsh is None:
        vsh = np.ma.MaskedArray(
            data=np.zeros_like(porosity), mask=np.zeros_like(porosity).astype(bool)
        )
        multiple_lithologies = False
    else:
        multiple_lithologies = True

    # Convert pressure from bar to Pa
    pres_ovb = pressure[0].overburden_pressure * 1.0e5
    pres_form = pressure[0].formation_pressure * 1.0e5
    for time_step, fl_prop in enumerate(fluid_properties):
        # Prepare data using filter_and_one_dim
        if time_step > 0 and rock_matrix.pressure_sensitivity:
            pres_depl = pressure[time_step].formation_pressure * 1.0e5
            (
                mask,
                tmp_min_k,
                tmp_min_mu,
                tmp_min_rho,
                tmp_fl_prop_k,
                tmp_fl_prop_rho,
                tmp_por,
                tmp_vsh,
                tmp_pres_over,
                tmp_pres_form,
                tmp_pres_depl,
            ) = filter_and_one_dim(
                matrix.bulk_modulus,
                matrix.shear_modulus,
                matrix.density,
                fl_prop.bulk_modulus,
                fl_prop.density,
                porosity,
                vsh,
                pres_ovb,
                pres_form,
                pres_depl,
                return_numpy_array=True,
            )
        else:
            (
                mask,
                tmp_min_k,
                tmp_min_mu,
                tmp_min_rho,
                tmp_fl_prop_k,
                tmp_fl_prop_rho,
                tmp_por,
                tmp_vsh,
            ) = filter_and_one_dim(
                matrix.bulk_modulus,
                matrix.shear_modulus,
                matrix.density,
                fl_prop.bulk_modulus,
                fl_prop.density,
                porosity,
                vsh,
                return_numpy_array=True,
            )

        if not multiple_lithologies:
            k_dry, mu, rho_dry = dry_rock_regression(
                tmp_por, tmp_min_rho, rock_matrix.model.parameters.sandstone
            )
        else:
            k_sand, mu_sand, rho_sand = dry_rock_regression(
                tmp_por, tmp_min_rho, rock_matrix.model.parameters.sandstone
            )
            k_shale, mu_shale, rho_shale = dry_rock_regression(
                tmp_por, tmp_min_rho, rock_matrix.model.parameters.shale
            )
            rho_dry = rho_sand * (1.0 - tmp_vsh) + rho_shale * tmp_vsh
            if rock_matrix.mineral_mix_model == MineralMixModel.HASHIN_SHTRIKMAN:
                k_dry, mu = hashin_shtrikman_average(
                    k_sand, k_shale, mu_sand, mu_shale, (1.0 - tmp_vsh)
                )
            else:
                k_dry, mu = voigt_reuss_hill(
                    k_sand, k_shale, mu_sand, mu_shale, (1.0 - tmp_vsh)
                )

        # Perform pressure correction on dry rock properties
        if time_step > 0 and rock_matrix.pressure_sensitivity:
            # Prepare in-situ properties dictionary based on what we have
            in_situ_dict = {
                ParameterTypes.K.value: k_dry,
                ParameterTypes.MU.value: mu,
                ParameterTypes.RHO.value: rho_dry,
                ParameterTypes.POROSITY.value: tmp_por,
            }

            mineral_props = None
            cement_props = None

            # Regression model requirements are met as default, but in the case of a
            # "physics model" (friable or patchy cement), extra matrix properties are
            # needed
            if hasattr(
                rock_matrix.pressure_sensitivity_model, "model_type"
            ) and rock_matrix.pressure_sensitivity_model.model_type in list(
                PhysicsPressureModelTypes
            ):
                # Create mineral properties from matrix properties
                mineral_props = EffectiveMineralProperties(
                    bulk_modulus=tmp_min_k,
                    shear_modulus=tmp_min_mu,
                    density=tmp_min_rho,
                )

                # If patchy cement model, create cement properties
                if (
                    rock_matrix.pressure_sensitivity_model.model_type
                    == PhysicsPressureModelTypes.PATCHY_CEMENT
                ):
                    # Use specified cement mineral
                    cement_props = rock_matrix.minerals[rock_matrix.cement]

            # Apply pressure sensitivity model
            depleted_props = apply_dry_rock_pressure_sensitivity_model(
                model=rock_matrix.pressure_sensitivity_model,
                initial_eff_pressure=(
                    tmp_pres_over - tmp_pres_form
                ),  # effective initial pressure
                depleted_eff_pressure=(
                    tmp_pres_over - tmp_pres_depl
                ),  # effective depleted pressure
                in_situ_dict=in_situ_dict,
                mineral_properties=mineral_props,
                cement_properties=cement_props,
            )

            # Update dry properties with pressure-corrected values
            k_dry = depleted_props[ParameterTypes.K.value]
            mu = depleted_props[ParameterTypes.MU.value]
            rho_dry = depleted_props[ParameterTypes.RHO.value]

        # Saturate rock
        k_sat = gassmann(k_dry, tmp_por, tmp_fl_prop_k, tmp_min_k)
        rho_sat = rho_dry + tmp_por * tmp_fl_prop_rho
        vp, vs = velocity(k_sat, mu, rho_sat)[0:2]

        vp, vs, rho_sat = reverse_filter_and_restore(mask, vp, vs, rho_sat)
        saturated_props.append(SaturatedRockProperties(vp=vp, vs=vs, density=rho_sat))

    return saturated_props
