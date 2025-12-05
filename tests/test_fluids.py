import numpy as np
import pytest

from fmu.pem import INTERNAL_EQUINOR
from fmu.pem.pem_functions import fluid_properties
from fmu.pem.pem_functions.fluid_properties import effective_fluid_properties_zoned
from fmu.pem.pem_utilities import EffectiveFluidProperties, SimRstProperties
from fmu.pem.pem_utilities.enum_defs import CO2Models, FluidMixModel, TemperatureMethod


# Stubs for fluid parameters
class StubBrine:
    """Stub brine class"""

    salinity = 35000.0
    perc_na = 90.0
    perc_ca = 5.0
    perc_k = 5.0


class StubGasParams:
    """Stub gas params class"""

    gas_gravity = 0.65
    model = "flag_default"


class StubOilParams:
    """Stub oil params class"""

    reference_density = 800.0
    gas_gravity = 0.8


class StubCondensateParams:
    """Stub condensate params class"""

    reference_density = 750.0
    gas_gravity = 0.7


class StubTemperatureCfg:
    """Stub temperature from simulator class (degC)"""

    type = TemperatureMethod.FROMSIM
    temperature_value = 60.0


class StubMixMethodWood:
    """Stub for Wood mixing method"""

    method = FluidMixModel.WOOD


class StubPVTZone:
    """Stub PVT zone - mimics PVTZone from pem_config_validation"""

    def __init__(self, gas_z_factor=1.0):
        self.pvtnum = "*"
        self.brine = StubBrine()
        self.gas = StubGasParams()
        self.oil = StubOilParams()
        self.condensate = StubCondensateParams()
        self.temperature = StubTemperatureCfg()
        self.gas_saturation_is_co2 = False
        self.gas_z_factor = gas_z_factor
        self.calculate_condensate = False
        self.co2_model = CO2Models.FLAG


class StubFluids:
    """Composite stub for fluids - mimic Pydantic object with pvt_zones"""

    def __init__(self, gas_z_factor=1.0):
        self.pvt_zones = [StubPVTZone(gas_z_factor=gas_z_factor)]
        self.salinity_from_sim = True
        self.co2_model = CO2Models.FLAG
        self.fluid_mix_method = StubMixMethodWood()


# SimRstProperties stub with inheritance
class StubSimRstProperties(SimRstProperties):
    def __init__(self, swat, sgas, rs, pressure, salt, temp, rv=None):
        # Convert all inputs to masked arrays before passing to parent
        swat = np.ma.MaskedArray(np.asarray(swat), mask=False)
        sgas = np.ma.MaskedArray(np.asarray(sgas), mask=False)
        rs = np.ma.MaskedArray(np.asarray(rs), mask=False)
        pressure = np.ma.MaskedArray(np.asarray(pressure), mask=False)
        soil = np.ma.MaskedArray(np.zeros_like(swat), mask=False)

        super().__init__(swat, sgas, soil, rs, pressure)

        # Set additional properties as masked arrays
        self.salt = np.ma.MaskedArray(np.asarray(salt), mask=False)
        self.temp = np.ma.MaskedArray(np.asarray(temp), mask=False)
        if rv is not None:
            self.rv = np.ma.MaskedArray(np.asarray(rv), mask=False)


@pytest.fixture
def fluids():
    return StubFluids()


@pytest.fixture
def pvtnum_grid():
    """Create a single-zone PVTNUM grid matching restart property shape."""
    # Shape (3,) to match test data (3 cells)
    shape = (3,)
    # All cells belong to PVTNUM=1, no masking
    data = np.ones(shape, dtype=int)
    mask = np.zeros(shape, dtype=bool)
    return np.ma.masked_array(data, mask=mask)


@pytest.fixture
def sim_props_high_pressure():
    """High pressure scenario - above bubble point"""
    return StubSimRstProperties(
        swat=[1.0, 0.0, 0.3],
        sgas=[0.0, 1.0, 0.2],
        rs=[50, 50, 50],
        pressure=[50e6, 50e6, 50e6],  # 500 bar - well above bubble point
        salt=[35, 35, 35],
        temp=[90, 90, 90],
    )


@pytest.fixture
def sim_props_low_pressure():
    """Low pressure scenario - below bubble point"""
    return StubSimRstProperties(
        swat=[1.0, 0.0, 0.3],
        sgas=[0.0, 1.0, 0.2],
        rs=[50, 50, 50],
        pressure=[5e6, 5e6, 5e6],  # 50 bar - below bubble point
        salt=[35, 35, 35],
        temp=[90, 90, 90],
    )


@pytest.fixture
def sim_props_no_condensate():
    """Medium pressure scenario"""
    return StubSimRstProperties(
        swat=[1.0, 0.0, 0.3],
        sgas=[0.0, 1.0, 0.2],
        rs=[50, 50, 50],
        pressure=[20e6, 20e6, 20e6],  # 200 bar
        salt=[35, 35, 35],
        temp=[90, 90, 90],
    )


@pytest.fixture
def sim_props_with_condensate():
    return StubSimRstProperties(
        swat=[0.0, 0.0, 0.3],
        sgas=[1.0, 1.0, 0.2],
        rs=[80, 80, 80],
        pressure=[25e6, 25e6, 25e6],
        salt=[35, 35, 35],
        temp=[100, 100, 100],
        rv=[0.0, 0.5, 0.0],
    )


@pytest.fixture(autouse=True)
def mock_flag_models(monkeypatch):
    def brine_properties(temperature, pressure, salinity, p_nacl, p_cacl, p_kcl):
        n = len(temperature)
        return np.full(n, 1500.0), np.full(n, 1030.0), np.full(n, 2.5e9)

    def oil_properties(temperature, pressure, rho0, gas_oil_ratio, gas_gravity):
        n = len(temperature)
        return np.full(n, 1400.0), np.full(n, 800.0), np.full(n, 1.5e9)

    def gas_properties(temperature, pressure, gas_gravity, model):
        n = len(temperature)
        return np.full(n, 2000.0), np.full(n, 200.0), np.full(n, 0.5e9), None

    def co2_properties(temp, pres):
        n = len(temp)
        return np.full(n, 1800.0), np.full(n, 400.0), np.full(n, 0.8e9)

    def bp_standing_mock(density, gas_oil_ratio, gas_gravity, temperature):
        """
        Mock bubble point calculation.
        Returns 100 bar (1e7 Pa) - this is above sim_props_low_pressure (50 bar)
        but below sim_props_high_pressure (500 bar) and sim_props_no_condensate
        (200 bar).
        """
        n = len(density) if hasattr(density, "__len__") else 1
        return np.full(n, 1.0e7)  # 100 bar in Pa

    monkeypatch.setattr(fluid_properties.flag, "brine_properties", brine_properties)
    monkeypatch.setattr(fluid_properties.flag, "oil_properties", oil_properties)
    monkeypatch.setattr(fluid_properties.flag, "gas_properties", gas_properties)
    monkeypatch.setattr(fluid_properties, "bp_standing", bp_standing_mock)

    # CO2 properties available through different modules depending on INTERNAL_EQUINOR
    if INTERNAL_EQUINOR:
        monkeypatch.setattr(fluid_properties.flag, "co2_properties", co2_properties)
    else:
        monkeypatch.setattr(
            fluid_properties.span_wagner, "co2_properties", co2_properties
        )

    if INTERNAL_EQUINOR:

        def condensate_properties(
            temperature, pressure, rho0, gas_oil_ratio, gas_gravity
        ):
            n = len(temperature)
            return np.full(n, 1600.0), np.full(n, 600.0), np.full(n, 1.0e9)

        monkeypatch.setattr(
            fluid_properties.flag, "condensate_properties", condensate_properties
        )

    if INTERNAL_EQUINOR:

        def saturations_below_bubble_point_mock(
            gas_saturation_init,
            oil_saturation_init,
            brine_saturation_init,
            gor_init,
            oil_gas_gravity,
            free_gas_gravity,
            oil_density,
            z_factor,
            pres_depl,
            temp_res,
        ):
            # Return unchanged saturations and properties
            # (simulating above bubble point)
            return gas_saturation_init, oil_saturation_init, gor_init, free_gas_gravity

        monkeypatch.setattr(
            fluid_properties,
            "saturations_below_bubble_point",
            saturations_below_bubble_point_mock,
        )


def test_accepts_single_and_list(sim_props_high_pressure, fluids, pvtnum_grid):
    res_single = effective_fluid_properties_zoned(
        sim_props_high_pressure, fluids, pvtnum_grid
    )
    res_list = effective_fluid_properties_zoned(
        [sim_props_high_pressure], fluids, pvtnum_grid
    )
    assert isinstance(res_single[0], EffectiveFluidProperties)
    assert np.allclose(res_single[0].density, res_list[0].density)


@pytest.mark.skipif(
    not INTERNAL_EQUINOR, reason="Condensate only inside Equinor context"
)
def test_condensate_overwrite(sim_props_with_condensate, fluids, pvtnum_grid):
    fluids.pvt_zones[0].calculate_condensate = True
    res = effective_fluid_properties_zoned(
        sim_props_with_condensate, fluids, pvtnum_grid
    )[0]
    assert res.density[0] == pytest.approx(200.0)
    assert res.density[1] == pytest.approx(600.0)


def test_co2_path(sim_props_high_pressure, fluids, pvtnum_grid, monkeypatch):
    calls = {"co2": 0}
    fluids.pvt_zones[0].gas_saturation_is_co2 = True

    def co2_properties(temp, pres):
        calls["co2"] += 1
        n = len(temp)
        return np.full(n, 1800.0), np.full(n, 400.0), np.full(n, 0.8e9)

    # Mock the appropriate module based on INTERNAL_EQUINOR
    if INTERNAL_EQUINOR:
        monkeypatch.setattr(fluid_properties.flag, "co2_properties", co2_properties)
    else:
        monkeypatch.setattr(
            fluid_properties.span_wagner, "co2_properties", co2_properties
        )

    effective_fluid_properties_zoned(sim_props_high_pressure, fluids, pvtnum_grid)
    assert calls["co2"] == 1


def test_density_and_bulk_shapes(sim_props_high_pressure, fluids, pvtnum_grid):
    res = effective_fluid_properties_zoned(
        sim_props_high_pressure, fluids, pvtnum_grid
    )[0]
    assert res.density.shape == res.bulk_modulus.shape
    assert res.density.ndim == 1
    assert np.all(res.bulk_modulus > 0.0)
    # Verify masked arrays are returned
    assert isinstance(res.density, np.ma.MaskedArray)
    assert isinstance(res.bulk_modulus, np.ma.MaskedArray)


def test_list_multiple(
    sim_props_high_pressure, sim_props_with_condensate, fluids, pvtnum_grid
):
    results = effective_fluid_properties_zoned(
        [sim_props_high_pressure, sim_props_with_condensate], fluids, pvtnum_grid
    )
    assert len(results) == 2
    assert all(isinstance(r, EffectiveFluidProperties) for r in results)
    # Verify all results are masked arrays
    assert all(isinstance(r.density, np.ma.MaskedArray) for r in results)
    assert all(isinstance(r.bulk_modulus, np.ma.MaskedArray) for r in results)


def test_below_bubble_point_raises_error(sim_props_low_pressure, pvtnum_grid):
    """Test that pressures below bubble point trigger an error when gas_z_factor=1.0"""
    fluids_default = StubFluids(gas_z_factor=1.0)
    with pytest.raises(
        ValueError, match="Fraction of cells with pressure below oil bubble point"
    ):
        effective_fluid_properties_zoned(
            sim_props_low_pressure, fluids_default, pvtnum_grid
        )


def test_above_bubble_point_succeeds(sim_props_high_pressure, pvtnum_grid):
    """Test normal operation with pressures above bubble point"""
    fluids_default = StubFluids(gas_z_factor=1.0)
    res = effective_fluid_properties_zoned(
        sim_props_high_pressure, fluids_default, pvtnum_grid
    )[0]
    assert isinstance(res, EffectiveFluidProperties)
    assert res.density.shape == (3,)
    assert np.all(res.bulk_modulus > 0.0)


def test_below_bubble_point_with_z_factor(sim_props_low_pressure, pvtnum_grid):
    """Test that setting gas_z_factor != 1.0 allows operation below bubble point"""
    fluids_with_z = StubFluids(gas_z_factor=0.95)
    # Should not raise an error, and should issue a warning instead
    with pytest.warns(UserWarning, match="Detected pressure below bubble point"):
        res = effective_fluid_properties_zoned(
            sim_props_low_pressure, fluids_with_z, pvtnum_grid
        )[0]
    assert isinstance(res, EffectiveFluidProperties)
    assert res.density.shape == (3,)
    assert np.all(res.bulk_modulus > 0.0)
