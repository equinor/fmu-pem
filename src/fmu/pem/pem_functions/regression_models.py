"""Regression models for saturated sandstones

Regression based on polynomial models for saturated sandstones. The models are
based on porosity polynomials to estimate either Vp and Vs, or K and Mu.
"""

from pathlib import Path
from typing import List, Union

import numpy as np
import numpy.typing as npt
from rock_physics_open.equinor_utilities.std_functions import (
    gassmann,
    hashin_shtrikman_average,
    moduli,
    velocity,
    voigt_reuss_hill,
)
from rock_physics_open.t_matrix_models import carbonate_pressure_model

from fmu.pem.pem_utilities import (
    DryRockProperties,
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    PressureProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)
from fmu.pem.pem_utilities.enum_defs import MineralMixModel
from fmu.pem.pem_utilities.rpm_models import (
    KMuRegressionParams,
    VpVsRegressionParams,
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
    return pol(porosity)


def dry_rock_regression(
    porosity: npt.NDArray[np.float64] | np.ma.MaskedArray,
    rho_min: npt.NDArray[np.float64] | np.ma.MaskedArray,
    params: VpVsRegressionParams | KMuRegressionParams,
) -> DryRockProperties:
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
    if not params.rho_regression:
        # rho_regression = False, use mineral density
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

    return DryRockProperties(
        bulk_modulus=np.ma.MaskedArray(k_dry),
        shear_modulus=np.ma.MaskedArray(mu),
        dens=np.ma.MaskedArray(rho_dry),
    )


def run_regression_models(
    mineral: MatrixProperties,
    fluid_properties: list[EffectiveFluidProperties],
    porosity: np.ma.MaskedArray,
    pressure: list[PressureProperties],
    config: PemConfig,
    vsh: Union[np.ma.MaskedArray, None] = None,
    pres_model_vp: Path = Path("carbonate_pressure_model_vp_exp.pkl"),
    pres_model_vs: Path = Path("carbonate_pressure_model_vs_exp.pkl"),
) -> List[SaturatedRockProperties]:
    """Run regression models for saturated rock properties.

    Args:
        mineral: Mineral properties containing bulk modulus (k) [Pa],
            shear modulus (mu) [Pa] and density (rho_sat) [kg/m3]
        fluid_properties: List of fluid properties,
            each containing bulk modulus (k) [Pa] and density (rho_sat) [kg/m3]
        porosity: Porosity as a masked array [fraction]
        pressure: List of pressure properties containing effective pressure values
            [bar] following Eclipse reservoir simulator convention
        config: Parameters for the PEM
        vsh: Volume of shale as a masked array [fraction], optional
        pres_model_vp: Path to the pressure sensitivity model file for P-wave velocity
            (default: "carbonate_pressure_model_vp_exp_2023.pkl")
        pres_model_vs: Path to the pressure sensitivity model file for S-wave velocity
            (default: "carbonate_pressure_model_vs_exp_2023.pkl")


    Returns:
        List[SaturatedRockProperties]: Saturated rock properties for each time step.
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
        if time_step > 0 and config.rock_matrix.pressure_sensitivity:
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
                mineral.bulk_modulus,
                mineral.shear_modulus,
                mineral.dens,
                fl_prop.bulk_modulus,
                fl_prop.dens,
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
                mineral.bulk_modulus,
                mineral.shear_modulus,
                mineral.dens,
                fl_prop.bulk_modulus,
                fl_prop.dens,
                porosity,
                vsh,
            )
        if not multiple_lithologies:
            dry_props = dry_rock_regression(
                tmp_por, tmp_min_rho, config.rock_matrix.model.parameters.sandstone
            )
        else:
            dry_props_sand = dry_rock_regression(
                tmp_por, tmp_min_rho, config.rock_matrix.model.parameters.sandstone
            )
            dry_props_shale = dry_rock_regression(
                tmp_por, tmp_min_rho, config.rock_matrix.model.parameters.shale
            )
            dry_rho = (
                dry_props_sand.dens * (1.0 - tmp_vsh) + dry_props_shale.dens * tmp_vsh
            )
            if config.rock_matrix.mineral_mix_model == MineralMixModel.HASHIN_SHTRIKMAN:
                k_dry, mu = hashin_shtrikman_average(
                    dry_props_sand.bulk_modulus,
                    dry_props_shale.bulk_modulus,
                    dry_props_sand.shear_modulus,
                    dry_props_shale.shear_modulus,
                    (1.0 - tmp_vsh),
                )
            else:
                k_dry, mu = voigt_reuss_hill(
                    dry_props_sand.bulk_modulus,
                    dry_props_shale.bulk_modulus,
                    dry_props_sand.shear_modulus,
                    dry_props_shale.shear_modulus,
                    (1.0 - tmp_vsh),
                )
            dry_props = DryRockProperties(
                bulk_modulus=k_dry, shear_modulus=mu, dens=dry_rho
            )

        # Perform pressure correction on dry rock properties
        dry_vp, dry_vs, _, _ = velocity(
            dry_props.bulk_modulus, dry_props.shear_modulus, dry_props.dens
        )
        if time_step > 0 and config.rock_matrix.pressure_sensitivity:
            # Inputs must be numpy arrays, not masked arrays
            dry_vp, dry_vs, dry_rho, _, _ = carbonate_pressure_model(
                tmp_fl_prop_rho,
                dry_vp.data,
                dry_vs.data,
                dry_props.dens.data,
                dry_vp.data,
                dry_vs.data,
                dry_props.dens.data,
                tmp_por,
                tmp_pres_over,
                tmp_pres_form,
                tmp_pres_depl,
                pres_model_vp,
                pres_model_vs,
                config.paths.rel_path_pem.absolute(),
                False,
            )
            k_dry, mu = moduli(dry_vp, dry_vs, dry_props.dens.data)
            dry_props = DryRockProperties(
                bulk_modulus=k_dry, shear_modulus=mu, dens=dry_rho
            )

        # Saturate rock
        k_sat = gassmann(dry_props.bulk_modulus, tmp_por, tmp_fl_prop_k, tmp_min_k)
        rho_sat = dry_props.dens + tmp_por * tmp_fl_prop_rho
        vp, vs = velocity(k_sat, dry_props.shear_modulus, rho_sat)[0:2]

        vp, vs, rho_sat = reverse_filter_and_restore(mask, vp, vs, rho_sat)
        props = SaturatedRockProperties(vp=vp, vs=vs, dens=rho_sat)
        saturated_props.append(props)

    return saturated_props
