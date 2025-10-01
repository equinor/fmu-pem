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
from xtgeo import Grid

from fmu.pem.pem_utilities import (
    MatrixProperties,
    PemConfig,
    SimInitProperties,
    filter_and_one_dim,
    get_shale_fraction,
    import_fractions,
    reverse_filter_and_restore,
    to_masked_array,
)
from fmu.pem.pem_utilities.enum_defs import MineralMixModel
from fmu.pem.pem_utilities.pem_config_validation import (
    MineralProperties,
)


def effective_mineral_properties(
    root_dir: Path, config: PemConfig, sim_init: SimInitProperties, sim_grid: Grid
) -> Tuple[Union[np.ma.MaskedArray, None], MatrixProperties]:
    """Estimate effective mineral properties for each grid cell

    Args:
        root_dir: start directory for running of PEM
        config: configuration parameters
        sim_init: simulation initial properties

    Returns:
        shale volume, effective mineral properties
    """
    fractions = import_fractions(root_dir, config, sim_grid)

    vsh = get_shale_fraction(
        fractions,
        config.rock_matrix.fraction_names,
        config.rock_matrix.shale_fractions,
    )

    mineral_names = config.rock_matrix.fraction_minerals
    eff_min_props = estimate_effective_mineral_properties(
        mineral_names, fractions, config, sim_init.poro
    )
    return vsh, eff_min_props


def estimate_effective_mineral_properties(
    fraction_names: Union[str, List[str]],
    fractions: Union[np.ma.MaskedArray, List[np.ma.MaskedArray]],
    pem_config: PemConfig,
    porosity: np.ma.MaskedArray,
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
        fraction_names,
        fractions,
        pem_config.rock_matrix.complement,
        porosity,
        pem_config.rock_matrix.volume_fractions.fractions_are_mineral_fraction,
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

    # ToDo: check mixing functions - high values for K
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
    porosity: np.ma.MaskedArray,
    mineral_fractions: bool,
) -> Tuple[list[str], list[np.ma.MaskedArray]]:
    """Normalizes mineral fractions and adds complement mineral if needed.

    If the fractions are volume fractions, porosity must be taken into account
    when the fractions are normalized.

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
    # Decide the mode of normalization - volume or mineral fractions
    normalize_sum = 1.0 if mineral_fractions else 1.0 - porosity

    # Check for single or list of names and fractions
    names = [names] if isinstance(names, str) else names
    fracs = [fracs] if isinstance(fracs, np.ma.MaskedArray) else fracs

    # Demand values in the range [0.0, 1.0]
    for i, frac in enumerate(fracs):
        if np.any(frac < 0.0) or np.any(frac > 1.0):
            warn(
                f"fraction {names[i]} has values outside of range 0.0 to 1.0,"
                f"clipped to range",
                UserWarning,
            )
            fracs[i] = np.ma.MaskedArray(np.ma.clip(frac, 0.0, 1.0))

    # Adjust values so that no cells exceed normalize_sum
    tot_fractions = sum(fracs)
    if np.ma.any(tot_fractions > normalize_sum):
        warn(
            "sum of fractions has values above limit, rescaled to range",
            UserWarning,
        )
        scale_factor = np.ma.max(tot_fractions / normalize_sum)
        for i, frac in enumerate(fracs):
            fracs[i] /= scale_factor

    # Add a complement fraction if needed
    comp_fraction = normalize_sum - sum(fracs)
    if np.any(comp_fraction > 0.0):
        names = names + [complement]
        fracs = fracs + [comp_fraction]

    # Rescale from volume fractions to mineral fractions if needed
    if not mineral_fractions:
        for i, frac in enumerate(fracs):
            fracs[i] /= normalize_sum

    # Final check that all fractions sum to 1.0 for all cells
    try:
        np.testing.assert_allclose(sum(fracs), 1.0, rtol=1.0e-6, atol=1.0e-6)
    except AssertionError as e:
        raise ValueError(f"mineral fractions do not sum to 1: {e}") from e
    return names, fracs
