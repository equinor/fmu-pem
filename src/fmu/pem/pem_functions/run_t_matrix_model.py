from pathlib import Path

import numpy as np
from rock_physics_open.t_matrix_models import (
    carbonate_pressure_model,
    run_t_matrix_forward_model_with_opt_params_exp,
    run_t_matrix_forward_model_with_opt_params_petec,
)

from fmu.pem.pem_utilities import (
    EffectiveFluidProperties,
    MatrixProperties,
    PemConfig,
    PressureProperties,
    SaturatedRockProperties,
    filter_and_one_dim,
    reverse_filter_and_restore,
)

from .run_patchy_cement_model import _verify_inputs


def run_t_matrix_model(
    mineral_properties: MatrixProperties,
    fluid_properties: list[EffectiveFluidProperties] | EffectiveFluidProperties,
    porosity: np.ma.MaskedArray,
    vsh: None | np.ma.MaskedArray,
    pressure: list[PressureProperties] | PressureProperties,
    config: PemConfig,
    petec_parameter_file: Path = Path("t_mat_params_petec.pkl"),
    exp_parameter_file: Path = Path("t_mat_params_exp.pkl"),
    pres_model_vp: Path = Path("carbonate_pressure_model_vp_exp.pkl"),
    pres_model_vs: Path = Path("carbonate_pressure_model_vs_exp.pkl"),
) -> list[SaturatedRockProperties]:
    """Model for carbonate rock with possibility to estimate changes due to
    production, i.e., saturation changes, changes in the fluids due to pore pressure
    change and also changes in the properties of the matrix by increase in effective
    pressure.

    The first timestep is regarded as in situ conditions for the pressure
    substitution, any later timestep also takes into account the changes in effective
    pressure from the initial one. Pressure sensitivity can be deselected in the
    configuration of the PEM.

    Calibration of parameters for the T-Matrix model must be made before running the
    forward model, this is only possible in RokDoc with 1D match to logs.

    Notice that t-matrix differs from the other saturated rock physics models in that
    there is no intermediate step for dry rock properties. For this reason, the pressure
    sensitive model is fixed, as this is a model that is adapted to saturated carbonate
    rocks. This model can be overridden by saving an alternative model with the same
    format as the default ones.

    Args:
        mineral_properties: bulk modulus (k) [Pa], shear modulus (mu) [Pa],
            density [kg/m^3]
        fluid_properties: bulk modulus (k) [Pa] and density [kg/m^3] for each restart
            date
        porosity: porosity [fraction]
        vsh: shale volume [fraction]
        pressure: overburden, effective and formation (pore) pressure per restart date
        config: configuration parameters
        petec_parameter_file: additional parameters for the T-Matrix model, determined
            through optimisation to well logs
        exp_parameter_file: additional parameters for the T-Matrix model, determined
            through optimisation to well logs
        pres_model_vp: pressure sensitivity model for vp
        pres_model_vs: pressure sensitivity model for vs

    Returns:
        saturated rock properties with vp [m/s], vs [m/s], density [kg/m^3],
        ai (vp * density), si (vs * density), vpvs (vp / vs)
    """
    fluid_properties, pressure = _verify_inputs(fluid_properties, pressure)

    # All model files are gathered with the config file for the PEM model,
    # i.e. in ../sim2seis/model
    petec_parameter_file = config.paths.rel_path_pem / petec_parameter_file
    exp_parameter_file = config.paths.rel_path_pem / exp_parameter_file

    saturated_props = []
    t_mat_params = config.rock_matrix.model.parameters

    if vsh is None and t_mat_params.t_mat_model_version == "EXP":
        raise ValueError("Shale volume must be provided for EXP model")
    if vsh is None:
        # For simplicity in the filtering, if no shale volume is provided, it is set
        # to zero
        vsh = np.ma.array(
            np.zeros_like(porosity), mask=np.zeros_like(porosity).astype(bool)
        )
    # Change unit from bar to Pa
    pres_ovb = pressure[0].overburden_pressure * 1.0e5
    pres_form = pressure[0].formation_pressure * 1.0e5

    for time_step, fl_prop in enumerate(fluid_properties):
        if time_step > 0:
            pres_depl = pressure[time_step].formation_pressure * 1.0e5
            (
                mask,
                tmp_min_k,
                tmp_min_mu,
                tmp_min_rho,
                tmp_fl_k,
                tmp_fl_rho,
                tmp_por,
                tmp_vsh,
                tmp_pres_over,
                tmp_pres_form,
                tmp_pres_depl,
            ) = filter_and_one_dim(
                mineral_properties.bulk_modulus,
                mineral_properties.shear_modulus,
                mineral_properties.density,
                fl_prop.bulk_modulus,
                fl_prop.density,
                porosity,
                vsh,
                pres_ovb,
                pres_form,
                pres_depl,
            )
        else:
            tmp_pres_over, tmp_pres_form, tmp_pres_depl = (None, None, None)
            (
                mask,
                tmp_min_k,
                tmp_min_mu,
                tmp_min_rho,
                tmp_fl_k,
                tmp_fl_rho,
                tmp_por,
                tmp_vsh,
            ) = filter_and_one_dim(
                mineral_properties.bulk_modulus,
                mineral_properties.shear_modulus,
                mineral_properties.density,
                fl_prop.bulk_modulus,
                fl_prop.density,
                porosity,
                vsh,
            )
        if t_mat_params.t_mat_model_version == "PETEC":
            vp, vs, rho, k, mu = run_t_matrix_forward_model_with_opt_params_petec(
                tmp_min_k,
                tmp_min_mu,
                tmp_min_rho,
                tmp_fl_k,
                tmp_fl_rho,
                tmp_por,
                t_mat_params.angle,
                t_mat_params.perm,
                t_mat_params.visco,
                t_mat_params.tau,
                t_mat_params.freq,
                str(petec_parameter_file),
            )
        else:
            vp, vs, rho, k, mu = run_t_matrix_forward_model_with_opt_params_exp(
                tmp_fl_k,
                tmp_fl_rho,
                tmp_por,
                tmp_vsh,
                t_mat_params.angle,
                t_mat_params.perm,
                t_mat_params.visco,
                t_mat_params.tau,
                t_mat_params.freq,
                str(exp_parameter_file),
            )
        if time_step > 0 and config.rock_matrix.pressure_sensitivity:
            vp, vs, rho, _, _ = carbonate_pressure_model(
                tmp_fl_rho,
                vp,
                vs,
                rho,
                vp,
                vs,
                rho,
                tmp_por,
                tmp_pres_over,
                tmp_pres_form,
                tmp_pres_depl,
                pres_model_vp,
                pres_model_vs,
                config.paths.rel_path_pem.absolute(),
                False,
            )
        vp, vs, rho = reverse_filter_and_restore(mask, vp, vs, rho)
        props = SaturatedRockProperties(vp=vp, vs=vs, density=rho)
        saturated_props.append(props)
    return saturated_props
