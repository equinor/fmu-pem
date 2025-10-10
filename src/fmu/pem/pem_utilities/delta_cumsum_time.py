import numpy as np

from .pem_class_definitions import (
    SaturatedRockProperties,
    SimInitProperties,
    TwoWayTime,
)
from .pem_config_validation import PemConfig


def estimate_delta_time(
    delta_z: np.ma.MaskedArray, vp: np.ma.MaskedArray, vs: np.ma.MaskedArray
) -> dict[str, np.ma.MaskedArray]:
    """Estimate seismic TWT parameters - PP, PS, SS modes

    Args:
        delta_z: delta depth cube [m]
        vp: compressional velocity [m/s]
        vs: shear velocity [m/s]

    Returns:
        delta PP time, delta SS time, delta PS time, all in [ms]
    """
    _verify_delta_t([delta_z, vp, vs])
    dt_pp = 2000.0 * delta_z / vp
    dt_ss = 2000.0 * delta_z / vs
    return {"twtpp": dt_pp, "twtss": dt_ss, "twtps": (dt_pp + dt_ss) / 2.0}


def _verify_delta_t(arrays: list[np.ma.MaskedArray]) -> None:
    for arr in arrays:
        if not isinstance(arr, np.ma.MaskedArray):
            raise TypeError(
                f"inputs to estimate_delta_time must be a numpy masked "
                f"arrays, is {type(arr)}."
            )
    dim_arr = np.array([arr.shape for arr in arrays])
    if not (dim_arr == dim_arr[0]).all():
        raise ValueError(
            f"{__file__}: the shape of the arrays to estimate_delta_t do not match"
        )
    return


def calculate_time_cumsum(
    props: list | dict, conf_params: PemConfig
) -> list[dict[str, np.ma.MaskedArray]]:
    """
    Function to calculate cumulative sum of time difference properties

    :param props: grid properties
    :param conf_params: configuration parameters
    :return: cumulative sum of properties along the z-axis
    """
    props = _verify_cumsum_inputs(props)
    sum_prop = []
    for prop_set in props:
        prop_set_dict = {}
        for k, v in prop_set.items():
            prop_set_dict[k] = np.cumsum(v, axis=2)
        sum_prop.append(prop_set_dict)

    return sum_prop


def _verify_cumsum_inputs(input_set):
    if not isinstance(input_set, list):
        input_set = [
            input_set,
        ]
    for this_input in input_set:
        if not isinstance(this_input, dict):
            raise ValueError(
                f"{__file__}: unexpected input type, should be dict, is "
                f"{type(this_input)}"
            )
    return input_set


def estimate_sum_delta_time(
    constant_props: SimInitProperties,
    sat_rock_props: list[SaturatedRockProperties],
    config: PemConfig,
) -> list[TwoWayTime]:
    """Calculate TWT (two-way-time) for seismic signal for each restart date

    Args:
        constant_props: constant properties, here the delta Z property of the eclipse
            grid is used
        sat_rock_props: effective properties for the saturated rock per restart date
        config: configuration parameters

    Returns:
        list of delta time and cumulative time per restart date
    """
    delta_time = [
        estimate_delta_time(constant_props.delta_z, sat_rock.vp, sat_rock.vs)
        for sat_rock in sat_rock_props
    ]
    cum_time_list = calculate_time_cumsum(delta_time, config)
    return [TwoWayTime(**time_set) for time_set in cum_time_list]
