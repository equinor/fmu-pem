from __future__ import annotations

import numpy as np


def input_num_string_to_list(
    input_string: str,
    num_array: list[int],
) -> list[int]:
    """Input is a string of comma-separated ranges like
    10-15, 20-25 and outputs the expanded verbose list of individual integers.
    """

    parts = [part.strip() for part in input_string.split(",")]

    integers = []

    for part in parts:
        if "-" in part:
            [start, end] = [int(integer) for integer in part.split("-")]
            integers += list(range(start, end + 1))
        elif "*" in part:
            return num_array
        else:
            try:
                integers.append(int(part))
            except ValueError as e:
                raise ValueError(f"unable to convert string '{part}' to integers: {e}")

    unique_integer_list = list(set(integers))
    unique_integer_list.sort()

    return unique_integer_list


# TODO: Should num_array type here instead be numpy?
def num_boolean_array(
    input_string: str,
    num_array: list[int],
) -> np.ndarray:
    """Returns a boolean array where a given element is True if the corresponding
    element in num_array (representing PVTNUM/FIPNUM) is part of the input_string
    definition, which is of format e.g. "10-20, 25"
    """

    # ToDo: should we let input_num_string_to_list handle '*'?
    if input_string.strip() == "*":
        return np.ones(np.shape(num_array), dtype=bool)

    _validate_input_strings(
        [
            input_string,
        ],
        num_array,
    )

    return np.isin(num_array, input_num_string_to_list(input_string, num_array))


# TODO: Should num_array type here instead be numpy?
def missing_num_areas(
    input_strings: list[str],
    num_array: list[int],
) -> list[int]:
    """Returns a list of all FIPNUM/PVTNUM integers not covered by the user input.
    If all integers are covered, the return value is an empty list. This function
    can be used to get a list of FIPNUM or PVTNUM areas the user has not given
    a value for.
    """
    _validate_input_strings(input_strings, num_array)

    if any(input_string.strip() == "*" for input_string in input_strings):
        return []

    unique_integers_grid = set(num_array)

    unique_integers_input_config = {
        num
        for input_string in input_strings
        for num in input_num_string_to_list(input_string, num_array)
    }

    missing_areas = list(unique_integers_grid - unique_integers_input_config)
    missing_areas.sort()

    return missing_areas


def detect_overlaps(
    input_strings: list[str],
    num_array: list[int],
) -> bool:
    """If there are any overlapping groups in the input strings, returns True."""
    _validate_input_strings(input_strings, num_array)

    def _map_values(inp_array: list[int], all_num_array: list[int]) -> list[int]:
        return [all_num_array.index(num) for num in inp_array if num in all_num_array]

    is_already_taken = np.zeros_like(num_array, dtype=bool)
    for string in input_strings:
        string_nums = input_num_string_to_list(string, num_array)
        position_list = _map_values(string_nums, num_array)
        if np.any(is_already_taken[position_list]):
            return True
        is_already_taken[position_list] = True
    return False


def _validate_input_strings(
    input_strings: list[str],
    num_array: list[int],
) -> None:
    """Make sure that there are no numbers in the input strings that are not part
    of num_array, but allow ranges to cover missing numbers in num_array"""
    num_set = set(num_array)
    min_num = min(num_array)
    max_num = max(num_array)

    for input_string in input_strings:
        parts = [part.strip() for part in input_string.split(",")]

        for part in parts:
            if "*" in part:
                continue
            if "-" in part:
                # Ranges are allowed to span missing numbers in num_array
                # But range endpoints must be within min/max bounds
                try:
                    start, end = [int(integer) for integer in part.split("-")]
                    if start > end:
                        raise ValueError(f"Invalid range '{part}': start > end")
                    if start < min_num or start > max_num:
                        raise ValueError(
                            f"Range start {start} in '{part}' is outside "
                            f"num_array bounds [{min_num}, {max_num}]"
                        )
                    if end > max_num:
                        raise ValueError(
                            f"Range end {end} in '{part}' is outside "
                            f"num_array bounds [{min_num}, {max_num}]"
                        )
                except ValueError as e:
                    if "outside" in str(e) or "Invalid range" in str(e):
                        raise
                    raise ValueError(f"Invalid range format '{part}': {e}")
            else:
                # Individual numbers must exist in num_array
                try:
                    num = int(part)
                    if num not in num_set:
                        raise ValueError(
                            f"Individual number {num} from input '{input_string}' "
                            f"not found in num_array"
                        )
                except ValueError as e:
                    if "not found in num_array" in str(e):
                        raise
                    raise ValueError(f"Unable to parse '{part}' as integer: {e}")


def validate_zone_coverage(
    zone_strings: list[str],
    grid_values: np.ma.MaskedArray,
    zone_name: str = "zone",
) -> None:
    """
    Validate that all grid values have corresponding zone definitions.

    Enforces:
    - Single wildcard '*' cannot appear with other groups
    - No overlaps among explicit definitions
    - All grid values covered by definitions

    Args:
        zone_strings: List of zone definition strings (e.g., ["*"] or ["1-5", "6-10"])
        grid_values: Masked array of zone integers from simulator grid
        zone_name: Name of zone type for error messages (e.g., "PVTNUM", "FIPNUM")

    Raises:
        ValueError: If wildcard misused, overlaps detected, or grid values lack
        definitions
    """
    # Extract unique values from grid
    grid_data = grid_values.data
    grid_mask = (
        grid_values.mask
        if hasattr(grid_values, "mask")
        else np.zeros_like(grid_data, dtype=bool)
    )
    actual_values = set(np.unique(grid_data[~grid_mask]).astype(int))

    if not actual_values:
        raise ValueError(f"No valid {zone_name} values found in grid")

    # Check for wildcard-only definition
    if "*" in zone_strings:
        if len(zone_strings) > 1:
            raise ValueError(
                f"Wildcard '*' cannot be combined with explicit {zone_name} "
                "definitions. Either use '*' alone or list all zones explicitly."
            )
        return  # Wildcard covers everything

    # Check for overlaps in explicit definitions
    max_val = max(actual_values)
    tmp_array = list(range(1, max_val + 1))
    if detect_overlaps(zone_strings, tmp_array):
        raise ValueError(f"Overlapping {zone_name} definitions found: {zone_strings}")

    # Check coverage: all grid values must have definitions
    defined_values = set()
    for zone_str in zone_strings:
        defined_values.update(input_num_string_to_list(zone_str, tmp_array))

    missing = actual_values - defined_values
    if missing:
        raise ValueError(
            f"{zone_name} values {sorted(missing)} are present in grid but have no "
            f"zone definition. Add explicit definitions for these values."
        )
