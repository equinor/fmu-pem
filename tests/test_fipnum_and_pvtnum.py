import numpy as np
import pytest

from fmu.pem.pem_utilities.fipnum_pvtnum_utilities import (
    input_num_string_to_list,
    missing_num_areas,
    num_boolean_array,
)


@pytest.mark.parametrize(
    ("input_string", "num_array", "expected_output"),
    [
        ("15-20,25-26", list(range(15, 27)), [15, 16, 17, 18, 19, 20, 25, 26]),
        (
            "5, 6, 7, 10-12, 14-16",
            list(range(5, 17)),
            [5, 6, 7, 10, 11, 12, 14, 15, 16],
        ),
    ],
)
def test_parsing_input_string(input_string, num_array, expected_output):
    output = input_num_string_to_list(input_string, num_array)

    assert np.array_equal(output, expected_output)


@pytest.mark.parametrize(
    ("input_config", "num_array", "expected_output"),
    [
        (
            [{"FIPNUM": "*", "value": 1}, {"FIPNUM": "2-4, 6", "value": 2}],
            [1, 1, 2, 3, 4, 5, 6, 6, 3, 1],
            [1, 1, 2, 2, 2, 1, 2, 2, 2, 1],
        ),
        (
            [{"FIPNUM": "1-3, 7", "value": 1}, {"FIPNUM": "4-6", "value": 2}],
            [7, 6, 5, 3, 2, 1, 2, 3, 4, 5, 6, 7],
            [1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1],
        ),
    ],
)
def test_filled_array(input_config, num_array, expected_output):
    """Example function which takes in user input, creates the filtered array
    which is used to find the indices to enter the value corresponding
    to the FIPNUM/PVTNUM string. Verifies at the end that the final
    array is as expected.
    """

    # Initialize empty array with same shape as PVTNUM/FIPNUM array:
    output = np.empty(np.shape(num_array))

    # Iterate over user config input:
    for area in input_config:
        # Create array which is True for grid cell
        # indices matching the user input string:
        filter_array = num_boolean_array(area["FIPNUM"], num_array)

        # Set output array to corresponding value:
        output[filter_array] = area["value"]

    assert np.array_equal(output, expected_output)


@pytest.mark.parametrize(
    ("input_config", "num_array", "expected_output"),
    [
        ([{"FIPNUM": "*"}, {"FIPNUM": "2-4, 6"}], [1, 1, 2, 3, 4, 5, 6, 6, 3, 1], []),
        (
            [{"FIPNUM": "2-3, 7"}, {"FIPNUM": "4-6"}],
            [7, 6, 5, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 8],
        ),
    ],
)
def test_coverage_check(input_config, num_array, expected_output):
    """Test coverage check, i.e. that each FIPNUM/PVTNUM area has a defined value."""

    input_strings = [area["FIPNUM"] for area in input_config]

    output = missing_num_areas(input_strings, num_array)

    assert np.array_equal(output, expected_output)
