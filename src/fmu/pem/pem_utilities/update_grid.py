import warnings
from dataclasses import asdict

import numpy as np
import xtgeo

from .pem_class_definitions import SaturatedRockProperties


def update_inactive_grid_cells(
    grid: xtgeo.grid3d.Grid,
    props: list[SaturatedRockProperties],
) -> xtgeo.grid3d.Grid:
    """
    Update the grid mask based on the mask of the properties

    Args:
        grid: original grid
        props: list of saturated rock properties

    Returns:
        Grid with the same geometry, but with updated mask for inactive cells
    """
    # Make sure that the 'props' are of type SaturatedRockProperties
    for prop in props:
        if not isinstance(prop, SaturatedRockProperties):
            raise ValueError(
                f"Expected 'props' to be of type SaturatedRockProperties, got "
                f"{type(prop)}"
            )

    grid_mask = grid.get_actnum(asmasked=True)

    init_mask = np.zeros_like(grid.actnum_array).astype(bool)

    for prop in props:
        # Iterate over all properties (vp, vs, density, ai, si, vpvs)
        for prop_arr in asdict(prop).values():
            init_mask = np.logical_or(init_mask, prop_arr.mask.astype(bool))

    # To match the logic in xtgeo grid actnum, the mask must be inverted
    init_mask = np.logical_not(init_mask)

    if not np.all(init_mask == grid.actnum_array.astype(bool)):
        warnings.warn(
            f"There are undefined values in PEM results: "
            f"{np.sum(np.logical_xor(init_mask, grid.actnum_array.astype(bool)))} "
            f"cells are added to the model's inactive cells. \nPlease investigate the "
            f"PEM's intermediate and final results for a cause."
        )
        init_mask = np.logical_and(init_mask, grid.actnum_array.astype(bool))
        grid_mask.values = init_mask
        grid.set_actnum(grid_mask)

    return grid
