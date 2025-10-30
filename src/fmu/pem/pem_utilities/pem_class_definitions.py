from dataclasses import dataclass, fields

import numpy as np
from numpy.ma import MaskedArray


class PropertiesSubgridMasked:
    """
    Class to derive object properties in a subgrid. The mask is assumed to
    come from a numpy masked array.

    In a numpy masked array, True means masked, False means not masked

    Args:
        self: object with np.ndarray or np.ma.MaskedArray attributes
        mask: Boolean mask to apply
        invert: If True, invert the mask with ~mask

    Returns:
        New instance of the same type with masked arrays
    """

    def masked_where(self, mask: np.ndarray, invert_mask: bool = True):
        actual_mask = ~mask if invert_mask else mask

        field_values = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                field_values[field.name] = None
            else:
                field_values[field.name] = np.ma.masked_where(actual_mask, value.data)
        return type(self)(**field_values)


# Eclipse simulator file classes - SimInitProperties and time step SimRstProperties
@dataclass
class SimInitProperties(PropertiesSubgridMasked):
    poro: MaskedArray
    depth: MaskedArray
    vsh_pem: MaskedArray | None = None
    pvtnum: MaskedArray | None = None
    fipnum: MaskedArray | None = None

    @property
    def delta_z(self) -> MaskedArray:
        """Estimate delta depth in the vertical direction"""

        def _verify_delta_z(inp_arr: MaskedArray) -> None:
            if not isinstance(inp_arr, MaskedArray) or inp_arr.dtype.kind != "f":
                raise TypeError(
                    f"input to estimate_delta_z must be a 3D numpy masked "
                    f"array with float data, is {type(inp_arr)}."
                )
            if np.ndim(inp_arr) != 3:
                raise ValueError(
                    f"{__file__}: 3-dimensional array must be input to "
                    f"estimate_delta_z. Depth difference is calculated along the "
                    f"third axis"
                )
            return

        _verify_delta_z(self.depth)
        d_z = np.zeros_like(self.depth)
        d_z[:, :, 1:] = self.depth.data[:, :, 1:] - self.depth.data[:, :, 0:-1]
        d_z[...] = np.clip(d_z, 0.0, a_max=None)
        delta_z: MaskedArray = MaskedArray(d_z, mask=self.depth.mask)
        return delta_z


@dataclass
class SimRstProperties(PropertiesSubgridMasked):
    swat: MaskedArray
    sgas: MaskedArray
    soil: MaskedArray
    rs: MaskedArray
    pressure: MaskedArray
    temp: MaskedArray | None = None
    rv: MaskedArray | None = None
    salt: MaskedArray | None = None


# Elastic properties for matrix, i.e. mixed minerals and volume fractions
@dataclass
class EffectiveMineralProperties(PropertiesSubgridMasked):
    bulk_modulus: MaskedArray | np.ndarray
    shear_modulus: MaskedArray | np.ndarray
    density: MaskedArray | np.ndarray

    def __post_init__(self):
        self.vs = np.sqrt(self.shear_modulus * self.density)
        self.vp = np.sqrt(
            (self.bulk_modulus + 4 / 3 * self.shear_modulus) / self.density
        )


# Separate class for dry rock, can use MatrixProperties as base
# class
@dataclass
class DryRockProperties(EffectiveMineralProperties):
    pass


# Acoustic properties for mixed fluids. If non-Newtonian fluids are to be considered,
# shear modulus and vs must be added
@dataclass
class EffectiveFluidProperties(PropertiesSubgridMasked):
    bulk_modulus: MaskedArray
    density: MaskedArray

    @property
    def vp(self):
        return np.sqrt(self.bulk_modulus / self.density)


# Pressure properties - overburden, formation and effective (strictly speaking
# differential) pressure
@dataclass
class PressureProperties(PropertiesSubgridMasked):
    formation_pressure: MaskedArray
    effective_pressure: MaskedArray
    overburden_pressure: MaskedArray


# Seismic two-way time
@dataclass
class TwoWayTime:
    twtpp: MaskedArray
    twtss: MaskedArray
    twtps: MaskedArray


# For isotropic elastic properties, only three independent components are needed
# to be defined, others can be derived from them, but this construction is needed
# to have all properties recognised by dataclasses.asdict()
@dataclass
class SaturatedRockProperties(PropertiesSubgridMasked):
    vp: MaskedArray
    vs: MaskedArray
    density: MaskedArray
    ai: MaskedArray | None = None
    si: MaskedArray | None = None
    vpvs: MaskedArray | None = None

    def __post_init__(self):
        """Calculate derived properties from independent variables.

        This runs both at initialization and can be called manually after
        updating vp/vs/density arrays (e.g., after zone merging).
        """
        self.recalculate_derived()

    def recalculate_derived(self):
        """Recalculate derived properties (ai, si, vpvs) from current vp, vs, density.

        Call this method after modifying vp, vs, or density arrays to update
        the derived properties.
        """
        self.ai = self.vp * self.density
        self.si = self.vs * self.density
        # Division may not preserve masks properly; explicitly combine masks
        vpvs_data = self.vp.data / self.vs.data
        vpvs_mask = np.logical_or(self.vp.mask, self.vs.mask)
        self.vpvs = np.ma.MaskedArray(vpvs_data, mask=vpvs_mask)
