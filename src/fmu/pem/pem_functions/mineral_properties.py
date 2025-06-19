"""
Effective mineral properties are calculated from the individual mineral properties of
the volume fractions. In the case that only a single net-to-gross fraction is
available, this is transformed to shale and sand fractions. A net-to-gross fraction
can also be estimated from porosity property.

If the ntg_calculation_flag is set in the PEM configuration parameter file, this will
override settings for volume fractions. In that case net-to-gross fraction is either
read from file, or calculated from porosity.
"""

from pathlib import Path
from typing import List, Tuple, Union
from warnings import warn

import numpy as np
from rock_physics_open.equinor_utilities.std_functions import (
    multi_hashin_shtrikman,
    multi_voigt_reuss_hill,
)

from fmu.pem.pem_utilities import (
    MatrixProperties,
    PemConfig,
    SimInitProperties,
    filter_and_one_dim,
    get_shale_fraction,
    import_fractions,
    ntg_to_shale_fraction,
    read_ntg_grid,
    reverse_filter_and_restore,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import MineralMixModel, VolumeFractions
from fmu.pem.pem_utilities.pem_config_validation import (
    MineralProperties,
)


def effective_mineral_properties(
    root_dir: Path, config: PemConfig, sim_init: SimInitProperties
) -> Tuple[Union[np.ma.MaskedArray, None], MatrixProperties]:
    """Estimate effective mineral properties for each grid cell

    Args:
        root_dir: start directory for running of PEM
        config: configuration parameters
        sim_init: simulation initial properties

    Returns:
        shale volume, effective mineral properties
    """
    if config.rock_matrix.volume_fractions.mode == VolumeFractions.NTG_SIM:
        # ntg_from_init_file flag takes precedence over ntg_from_porosity
        if config.rock_matrix.volume_fractions.from_porosity:
            vsh = calc_ntg_from_porosity(sim_init.poro)
        else:
            vsh = ntg_to_shale_fraction(sim_init.ntg, sim_init.poro)
        fractions = [
            vsh,
        ]
    else:
        fractions = import_fractions(root_dir, config)
        # In case of a single fraction: it can either be NTG or a true volume fraction
        if len(fractions) == 1 and config.rock_matrix.volume_fractions.fraction_is_ntg:
            fractions[0] = ntg_to_shale_fraction(fractions[0], sim_init.poro)
        vsh = get_shale_fraction(
            fractions,
            config.rock_matrix.fraction_names,
            config.rock_matrix.shale_fractions,
        )

    mineral_names = config.rock_matrix.fraction_minerals
    eff_min_props = estimate_effective_mineral_properties(
        mineral_names, fractions, config
    )
    return vsh, eff_min_props


def estimate_effective_mineral_properties(
    fraction_names: Union[str, List[str]],
    fractions: Union[np.ma.MaskedArray, List[np.ma.MaskedArray]],
    pem_config: PemConfig,
) -> MatrixProperties:
    """Estimation of effective mineral properties must be able to handle cases where
    there is a more complex combination of minerals than the standard sand/shale case.
    For carbonates the input can be based on minerals (e.g. calcite, dolomite, quartz,
    smectite, ...) or PRTs (petrophysical rock types) that each have been assigned
    elastic properties to.
    The rock physics library is aimed at one-dimensional arrays, not masked arrays, so
    special handling of input objects is needed.

    Args:
        fraction_names: mineral names of the different fractions.
        fractions: fraction of each mineral
        pem_config: parameter object

    Returns:
        bulk modulus [Pa], shear modulus [Pa] and density [kg/m3] of effective mineral
    """
    verify_mineral_inputs(
        fraction_names,
        fractions,
        pem_config.rock_matrix.minerals,
        pem_config.rock_matrix.complement,
    )

    fraction_names, fractions = normalize_mineral_fractions(
        fraction_names, fractions, pem_config.rock_matrix.complement
    )

    mask, *fractions = filter_and_one_dim(*fractions)
    k_list = []
    mu_list = []
    rho_list = []
    for name in fraction_names:
        mineral = pem_config.rock_matrix.minerals[name]
        k_list.append(to_masked_array(mineral.bulk_modulus, fractions[0]))
        mu_list.append(to_masked_array(mineral.shear_modulus, fractions[0]))
        rho_list.append(to_masked_array(mineral.density, fractions[0]))

    if pem_config.rock_matrix.mineral_mix_model == MineralMixModel.HASHIN_SHTRIKMAN:
        eff_k, eff_mu = multi_hashin_shtrikman(
            *[arr for prop in zip(k_list, mu_list, fractions) for arr in prop]
        )
    else:
        eff_k, eff_mu = multi_voigt_reuss_hill(
            *[arr for prop in zip(k_list, mu_list, fractions) for arr in prop]
        )
    # Use phi masked array to restore original shape
    eff_rho: np.ma.MaskedArray = np.ma.MaskedArray(
        sum(rho * frac for rho, frac in zip(rho_list, fractions))
    )
    eff_min_k, eff_min_mu, eff_min_rho = reverse_filter_and_restore(
        mask, eff_k, eff_mu, eff_rho
    )
    return MatrixProperties(
        bulk_modulus=eff_min_k, shear_modulus=eff_min_mu, dens=eff_min_rho
    )


def verify_mineral_inputs(
    names: str | list[str],
    fracs: np.ma.MaskedArray | list[np.ma.MaskedArray],
    minerals: dict[str, MineralProperties],
    complement: str,
) -> None:
    if isinstance(names, str):
        names = [names]

    if isinstance(fracs, np.ma.MaskedArray):
        fracs = [fracs]

    if len(names) != len(fracs):
        raise ValueError(
            f"mismatch between number of mineral names and fractions, "
            f"{len(names)} vs. {len(fracs)}"
        )

    for name in names + [complement]:
        if name not in minerals:
            raise ValueError(f"mineral names not listed in config file: {name}")


def normalize_mineral_fractions(
    names: str | list[str],
    fracs: np.ma.MaskedArray | list[np.ma.MaskedArray],
    complement: str,
) -> Tuple[list[str], list[np.ma.MaskedArray]]:
    """Normalizes mineral fractions and adds complement mineral if needed.

    When the sum of specified mineral fractions is less than 1.0, adds the complement
    mineral to make up the remainder. For example, if shale is 0.6 (60%) and the
    complement mineral is quartz, then quartz will be added at 0.4 (40%) to reach 100%.

    If fractions exceed valid range (0-1), they are clipped. If total exceeds 1.0,
    all fractions are scaled down proportionally.

    Args:
        names: Single mineral name or list of mineral names
        fracs: Single masked array or list of masked arrays containing mineral fractions
        complement: Name of mineral to use as complement if sum < 1.0

    Returns:
        Tuple containing:
            - List of mineral names (with complement added if needed)
            - List of normalized mineral fractions as masked arrays
    """
    if isinstance(names, str):
        names = [names]

    if isinstance(fracs, np.ma.MaskedArray):
        fracs = [fracs]

    for i, frac in enumerate(fracs):
        if np.any(frac[~frac.mask] < 0.0) or np.any(frac[~frac.mask] > 1.0):
            warn(
                f"mineral fraction {names[i]} has values outside of range 0.0 to 1.0,"
                f"clipped to range",
                UserWarning,
            )
            fracs[i] = np.ma.MaskedArray(np.ma.clip(frac, 0.0, 1.0))

    tot_fractions = np.ma.sum(fracs, axis=0)
    max_fraction = np.ma.max(tot_fractions)
    TOLERANCE = 0.00001

    if np.any(tot_fractions[~tot_fractions.mask] > 1.0 + TOLERANCE):
        warn(
            f"sum of mineral fractions are above 1.0 for "
            f"{np.sum(tot_fractions[~tot_fractions.mask] > 1.0)} cells, is "
            f"scaled to maximum 1.0.\n"
            f"Max value is {np.max(tot_fractions[~tot_fractions.mask])}",
            UserWarning,
        )
        for i, frac in enumerate(fracs):
            fracs[i] /= max_fraction

    comp_fraction = 1.0 - np.ma.sum(fracs, axis=0)
    if np.any(comp_fraction > 0.0):
        names = names + [complement]
        fracs = fracs + [comp_fraction]

    return names, fracs


def calc_ntg_from_porosity(porosity: np.ma.MaskedArray) -> np.ma.MaskedArray:
    vsh = to_masked_array(0, porosity)
    vsh[porosity <= 0.33] = np.ma.power((0.33 - porosity[porosity < 0.33]) / 0.33, 2.0)
    return (vsh / (1.0 - porosity)).clip(0.0, 1.0)
