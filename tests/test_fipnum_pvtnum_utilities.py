import numpy as np
import pytest

from fmu.pem.pem_utilities.fipnum_pvtnum_utilities import (
    detect_overlaps,
    input_num_string_to_list,
    missing_num_areas,
    num_boolean_array,
)

num_list = list(range(1, 15 + 1))
del num_list[5]


def test_input_string_to_list():
    # Test wildcard
    num_str = "*"
    expected_num = num_list
    assert input_num_string_to_list(num_str, num_list) == expected_num

    # Test range
    num_str = "1-5"
    expected_num = [1, 2, 3, 4, 5]
    assert input_num_string_to_list(num_str, num_list) == expected_num

    # Test single numbers
    num_str = "1, 7, 9"
    expected_num = [1, 7, 9]
    assert input_num_string_to_list(num_str, num_list) == expected_num

    # Test range and single numbers (in this test it should not be detected
    # that "6" is not part of num_list
    num_str = "1-7, 14, 15"
    expected_num = [1, 2, 3, 4, 5, 6, 7, 14, 15]
    assert input_num_string_to_list(num_str, num_list) == expected_num

    # Test illegal input
    num_str = "not integers"
    with pytest.raises(ValueError, match="unable to convert string"):
        input_num_string_to_list(num_str, num_list)


def test_num_boolean_array():
    # Test range
    num_str = "1-5"
    expected_bool = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=bool)
    assert np.all(num_boolean_array(num_str, num_list) == expected_bool)

    # Test single numbers
    num_str = "1, 7, 9"
    expected_bool = np.array([1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], dtype=bool)
    assert np.all(num_boolean_array(num_str, num_list) == expected_bool)

    # Test range and single numbers
    num_str = "1-5, 7, 14, 15"
    expected_bool = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1], dtype=bool)
    assert np.all(num_boolean_array(num_str, num_list) == expected_bool)

    # Test value outside of range
    num_str = "14-17"
    with pytest.raises(ValueError, match="Range end"):
        num_boolean_array(num_str, num_list)


def test_missing_num_areas():
    # Test wildcard
    num_str = [
        "*",
    ]
    expected_num = []
    assert missing_num_areas(num_str, num_list) == expected_num

    # Test full range
    num_str = ["1-5", "7-15"]
    expected_num = []
    assert missing_num_areas(num_str, num_list) == expected_num

    # Test partial range
    num_str = ["1-5"]
    expected_num = [7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert missing_num_areas(num_str, num_list) == expected_num

    # Test single values
    num_str = ["1", "5", "7"]
    expected_num = [2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15]
    assert missing_num_areas(num_str, num_list) == expected_num

    # Test range with illegal value - should be accepted
    num_str = [
        "1-15",
    ]
    expected_num = []
    assert missing_num_areas(num_str, num_list) == expected_num

    # Test range and single numbers with illegal value - should be caught
    num_str = [
        "1-15, 6",
    ]
    with pytest.raises(ValueError, match="Individual number"):
        missing_num_areas(num_str, num_list)


def test_detect_overlap():
    # Test no overlap in ranges
    num_str = ["1-4", "7-9"]
    expected_result = False
    assert detect_overlaps(num_str, num_list) == expected_result

    # Test overlaps
    num_str = ["1-7", "4-9"]
    expected_result = True
    assert detect_overlaps(num_str, num_list) == expected_result

    # Test overlaps - allow for overlap within a group
    num_str = ["1-7, 3", "12-14"]
    expected_result = False
    assert detect_overlaps(num_str, num_list) == expected_result
