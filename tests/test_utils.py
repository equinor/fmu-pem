import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from fmu.pem.pem_functions.mineral_properties import (
    normalize_mineral_fractions,
    verify_mineral_inputs,
)
from fmu.pem.pem_utilities import (
    filter_and_one_dim,
    get_shale_fraction,
    reverse_filter_and_restore,
)
from fmu.pem.pem_utilities.pem_config_validation import (
    MineralProperties,
)


def test_get_shale_fraction_single_shale():
    vol_fractions = [
        np.ma.array([0.1, 0.2, 0.3]),
        np.ma.array([0.2, 0.3, 0.4]),
        np.ma.array([0.7, 0.5, 0.3]),
    ]
    fraction_names = ["sand", "shale", "limestone"]
    shale_fraction_names = "shale"

    result = get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)
    np.testing.assert_array_equal(result, np.ma.array([0.2, 0.3, 0.4]))


def test_get_shale_fraction_multiple_shales():
    vol_fractions = [
        np.ma.array([0.1, 0.2, 0.3]),
        np.ma.array([0.2, 0.3, 0.4]),
        np.ma.array([0.3, 0.2, 0.1]),
    ]
    fraction_names = ["clay", "shale1", "shale2"]
    shale_fraction_names = ["shale1", "shale2"]

    result = get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)
    np.testing.assert_array_equal(result, np.ma.array([0.5, 0.5, 0.5]))


def test_get_shale_fraction_no_shale():
    vol_fractions = [np.ma.array([0.1, 0.2, 0.3]), np.ma.array([0.2, 0.3, 0.4])]
    fraction_names = ["sand", "limestone"]
    shale_fraction_names = None

    result = get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)
    assert result is None


def test_get_shale_fraction_empty_shale_list():
    vol_fractions = [np.ma.array([0.1, 0.2, 0.3]), np.ma.array([0.2, 0.3, 0.4])]
    fraction_names = ["sand", "limestone"]
    shale_fraction_names = []

    result = get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)
    assert result is None


def test_get_shale_fraction_with_masked_values():
    vol_fractions = [
        np.ma.array([0.1, 0.2, 0.3]),
        np.ma.masked_array([0.2, 0.3, 0.4], mask=[False, True, False]),
    ]
    fraction_names = ["sand", "shale"]
    shale_fraction_names = "shale"

    result = get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)
    np.testing.assert_array_equal(result.mask, [False, True, False])
    # Note that masked elements are set to 0 internally.
    np.testing.assert_array_equal(result.data, [0.2, 0.0, 0.4])


def test_get_shale_fraction_unknown_shale():
    vol_fractions = [np.ma.array([0.1, 0.2, 0.3]), np.ma.array([0.2, 0.3, 0.4])]
    fraction_names = ["sand", "limestone"]
    shale_fraction_names = "unknown_shale"

    with pytest.raises(ValueError, match="unknown shale fraction: unknown_shale"):
        get_shale_fraction(vol_fractions, fraction_names, shale_fraction_names)


def test_verify_mineral_inputs():
    minerals = {
        "shale": MineralProperties(
            bulk_modulus=25000000000.0, shear_modulus=12000000000.0, density=2680.0
        ),
        "quartz": MineralProperties(
            bulk_modulus=36800000000.0, shear_modulus=44000000000.0, density=2650.0
        ),
        "calcite": MineralProperties(
            bulk_modulus=76800000000.0, shear_modulus=32000000000.0, density=2710.0
        ),
        "dolomite": MineralProperties(
            bulk_modulus=94900000000.0, shear_modulus=45000000000.0, density=2870.0
        ),
        "stevensite": MineralProperties(
            bulk_modulus=32500000000.0, shear_modulus=11600000000.0, density=2490.0
        ),
    }

    # Test valid single input - should not raise any exceptions
    names = "shale"
    fracs = np.ma.array([0.6])
    verify_mineral_inputs(names, fracs, minerals, "quartz")

    # Test invalid mineral name
    with pytest.raises(ValueError, match="mineral names not listed in config file"):
        verify_mineral_inputs("invalid_mineral", fracs, minerals, "quartz")

    # Test invalid complement name
    with pytest.raises(ValueError, match="mineral names not listed in config file"):
        verify_mineral_inputs(names, fracs, minerals, "invalid_complement")

    # Test mismatched lengths
    with pytest.raises(
        ValueError, match="mismatch between number of mineral names and fractions"
    ):
        verify_mineral_inputs(
            ["shale", "calcite"], np.ma.array([0.6]), minerals, "quartz"
        )


def test_normalize_mineral_fractions():
    # Basic case - fractions sum to less than 1
    names = ["shale"]
    fracs = [np.ma.array([0.63])]
    por = np.ma.array([0.3])
    result_names, result_fracs = normalize_mineral_fractions(
        names, fracs, "quartz", por, False
    )
    assert result_names == ["shale", "quartz"]
    assert_array_almost_equal(result_fracs[0], 0.9)
    assert_array_almost_equal(result_fracs[1], 0.1)
    assert_array_almost_equal(np.ma.sum(result_fracs), 1.0)

    # Test clipping of negative values
    names = ["shale"]
    fracs = [np.ma.array([-0.1])]
    with pytest.warns(UserWarning, match="fraction shale has values outside of range"):
        result_names, result_fracs = normalize_mineral_fractions(
            names, fracs, "quartz", por, False
        )
    assert_array_almost_equal(result_fracs[0], 0.0)
    assert_array_almost_equal(result_fracs[1], 1.0)
    assert_array_almost_equal(np.ma.sum(result_fracs), 1.0)

    # Test clipping of values > 1
    names = ["shale"]
    fracs = [np.ma.array([1.2])]
    with pytest.warns(UserWarning, match="fraction shale has values outside of range"):
        result_names, result_fracs = normalize_mineral_fractions(
            names, fracs, "quartz", por, True
        )
    assert_array_almost_equal(result_fracs[0], 1.0)
    # No complement fraction should be added when the main fraction is 1.0
    assert len(result_fracs) == 1
    assert result_names == ["shale"]
    assert_array_almost_equal(np.ma.sum(result_fracs), 1.0)

    # Test scaling when sum > 1
    names = ["shale", "calcite"]
    fracs = [np.ma.array([0.7]), np.ma.array([0.6])]
    with pytest.warns(UserWarning, match="sum of fractions has values above limit"):
        result_names, result_fracs = normalize_mineral_fractions(
            names, fracs, "quartz", por, True
        )
    assert_array_almost_equal(np.ma.sum(result_fracs), 1.0)
    assert_array_almost_equal(result_fracs[0] / result_fracs[1], 0.7 / 0.6)

    # Test with masked values
    names = ["shale"]
    masked_array = np.ma.array([0.6, 0.7])
    masked_array[1] = np.ma.masked
    fracs = [masked_array]
    result_names, result_fracs = normalize_mineral_fractions(
        names, fracs, "quartz", por, True
    )
    assert result_fracs[0].mask[1]  # Check mask is preserved
    assert_array_almost_equal(result_fracs[0][0], 0.6)  # Check unmasked value
    assert_array_almost_equal(result_fracs[1][0], 0.4)  # Check complement
    assert_array_almost_equal(np.ma.sum([f[0] for f in result_fracs]), 1.0)


def test_filter_and_restore_round_trip_single_array():
    data = np.array([[0.0, 1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0, 9.0]])
    mask = np.array(
        [[False, True, False, False, True], [False, False, True, False, False]]
    )

    arr = np.ma.MaskedArray(data, mask=mask)
    fractions = [arr]

    mask, filtered_fraction = filter_and_one_dim(*fractions, return_numpy_array=False)

    # Check that array has been flattened and masked cells removed
    assert filtered_fraction.shape == (7,)
    np.testing.assert_equal(filtered_fraction.mask, False)

    # Check that mask and data are unchanged
    np.testing.assert_equal(mask, arr.mask)
    np.testing.assert_equal(filtered_fraction.data, arr[~mask].data)

    restored = reverse_filter_and_restore(mask, filtered_fraction)

    # Expecting 2D array with unmasked values restored to their original
    # positions and zeros in the positions that were masked,
    # i.e., where the mask is True.
    assert restored[0].data.shape == arr.shape
    np.testing.assert_equal(restored[0].mask, arr.mask)
    np.testing.assert_array_equal(
        restored[0].data,
        np.array([[0.0, 0.0, 2.0, 3.0, 0.0], [5.0, 6.0, 0.0, 8.0, 9.0]]),
    )


def test_filter_and_restore_round_trip_two_arrays():
    data1 = np.array([[0.0, 1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0, 9.0]])
    data2 = np.array([[10.0, 11.0, 12.0, 13.0, 14.0], [15.0, 16.0, 17.0, 18.0, 19.0]])
    mask1 = np.array(
        [[False, True, False, False, True], [False, False, True, False, False]]
    )
    mask2 = np.array(
        [[True, False, False, True, False], [False, False, False, False, False]]
    )

    arr1 = np.ma.MaskedArray(data1, mask=mask1)
    arr2 = np.ma.MaskedArray(data2, mask=mask2)
    fractions = [arr1, arr2]

    mask, *filtered_fractions = filter_and_one_dim(*fractions, return_numpy_array=False)
    assert len(filtered_fractions) == len(fractions)

    # Check that the arrays have been flattened and masked cells removed
    assert filtered_fractions[0].shape == (5,)
    assert filtered_fractions[1].shape == (5,)
    np.testing.assert_equal(filtered_fractions[0].mask, False)
    np.testing.assert_equal(filtered_fractions[1].mask, False)

    # Check that data are unchanged
    np.testing.assert_equal(filtered_fractions[0].data, arr1[~mask])
    np.testing.assert_equal(filtered_fractions[1].data, arr2[~mask])

    restored = reverse_filter_and_restore(mask, *filtered_fractions)

    # Execting 2D arrays with unmasked values restored to their original positions
    # and zeros in the positions that were masked,
    # i.e., where the mask is True.
    assert restored[0].data.shape == (2, 5)
    assert restored[1].data.shape == (2, 5)
    np.testing.assert_array_equal(
        restored[0].data,
        np.array([[0.0, 0.0, 2.0, 0.0, 0.0], [5.0, 6.0, 0.0, 8.0, 9.0]]),
    )
    np.testing.assert_array_equal(
        restored[1].data,
        np.array([[0.0, 0.0, 12.0, 0.0, 0.0], [15.0, 16.0, 0.0, 18.0, 19.0]]),
    )

    # Note that we started off with two arrays, arr1 and arr2 that have different masks.
    # After running them through filter_and_one_dim followed by
    # reverse_filter_and_restore, both arrays will have the same mask.
    np.testing.assert_array_equal(restored[0].mask, restored[1].mask)
