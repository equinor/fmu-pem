from dataclasses import dataclass, fields
from typing import Self

import numpy as np
from numpy.ma import MaskedArray

from .enum_defs import PhaseSystem


class PropertiesSubgridMasked:
    """
    Class to derive object properties in a subgrid. The mask is assumed to
    come from a numpy masked array.

    In a numpy masked array, True means masked, False means not masked
    """

    def masked_where(self: Self, mask: np.ndarray, invert_mask: bool = True) -> Self:
        """
            Method to derive object properties in a subgrid. The mask is assumed to
            come from a numpy masked array.

        In a numpy masked array, True means masked, False means not masked
            Args:
                self: object with np.ndarray or np.ma.MaskedArray attributes
                mask: Boolean mask to apply
                invert_mask: If True, invert the mask with ~mask

            Returns:
                New instance of the same type with masked arrays
        """
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
    aquifern: MaskedArray | None = None

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

    def reconcile_phase_saturations(
        self, phase_system: PhaseSystem, tol: float = 1.0e-6
    ) -> None:
        """Validate saturations against ``phase_system`` and normalise in place.

        For each of water/gas/oil:

        - If the phase is declared absent in ``phase_system``, the saturation
          must be at most ``tol`` in magnitude everywhere; otherwise
          ``ValueError`` is raised. The array is then forced to exactly zero.
        - If the phase is declared present but its saturation is (numerically)
          zero everywhere, it is derived as ``1 - sum_of_other_phases``. At most
          one present phase may be derived this way; if more than one is empty,
          ``ValueError`` is raised.
        - All other present phases are clipped to ``[0, 1]``.

        After the per-phase handling, the three saturations are renormalised
        cell-by-cell so they sum to 1, correcting any small numerical drift.
        """
        sats: dict[PhaseSystem, tuple[str, MaskedArray]] = {
            PhaseSystem.WATER: ("water (SWAT)", np.ma.clip(self.swat, 0.0, 1.0)),
            PhaseSystem.GAS: ("gas (SGAS)", np.ma.clip(self.sgas, 0.0, 1.0)),
            PhaseSystem.OIL: ("oil (SOIL)", np.ma.clip(self.soil, 0.0, 1.0)),
        }

        for flag, (name, sat) in list(sats.items()):
            if phase_system & flag:
                continue
            max_abs = float(np.ma.max(np.ma.abs(sat)))
            if max_abs > tol:
                raise ValueError(
                    f"SimRstProperties: phase {name} is declared absent by "
                    f"PhaseSystem={phase_system!r} but has non-zero saturation "
                    f"(max |sat| = {max_abs:g})."
                )
            sats[flag] = (
                name,
                np.ma.masked_array(np.zeros_like(sat.data), mask=sat.mask),
            )

        derived = [
            flag
            for flag, (_name, sat) in sats.items()
            if (phase_system & flag) and float(np.ma.max(np.ma.abs(sat))) <= tol
        ]
        if len(derived) > 1:
            raise ValueError(
                "SimRstProperties: more than one present phase has zero saturation "
                f"({[sats[f][0] for f in derived]}); cannot derive both."
            )
        if derived:
            flag = derived[0]
            other_sum = sum(
                (sat for f, (_n, sat) in sats.items() if f != flag),
                start=np.ma.zeros_like(sats[flag][1]),
            )
            sats[flag] = (sats[flag][0], np.ma.clip(1.0 - other_sum, 0.0, 1.0))

        total = (
            sats[PhaseSystem.WATER][1]
            + sats[PhaseSystem.GAS][1]
            + sats[PhaseSystem.OIL][1]
        )
        safe_total = np.ma.where(total > 0.0, total, 1.0)
        self.swat = sats[PhaseSystem.WATER][1] / safe_total
        self.sgas = sats[PhaseSystem.GAS][1] / safe_total
        self.soil = sats[PhaseSystem.OIL][1] / safe_total


# Elastic properties for matrix, i.e. mixed minerals and volume fractions
@dataclass
class EffectiveMineralProperties(PropertiesSubgridMasked):
    bulk_modulus: MaskedArray | np.ndarray
    shear_modulus: MaskedArray | np.ndarray
    density: MaskedArray | np.ndarray

    def __post_init__(self):
        self.vs = np.sqrt(self.shear_modulus / self.density)
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
    """
    All attributes shall have unit Pa
    """

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
        self.vpvs = self.vp / self.vs
