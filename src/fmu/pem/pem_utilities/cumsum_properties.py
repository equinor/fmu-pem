from dataclasses import asdict

from .pem_config_validation import PemConfig


def calculate_diff_properties(props: list, conf_params: PemConfig) -> tuple[list, list]:
    """
    Function to calculate difference attributes between grid properties

    :param props: grid properties
    :param conf_params: configuration parameters
    :return: difference of time steps according to config file
    """
    _verify_diff_inputs(props, conf_params)
    props = _filter_diff_inputs(props, conf_params)

    def diff(x, y):
        return x - y

    def diffpercent(x, y):
        return 100.0 * (x - y) / y

    def ratio(x, y):
        return x / y

    lookup = dict(
        zip(
            conf_params.global_params.seis_dates,  # type: ignore
            range(len(conf_params.global_params.seis_dates)),  # type: ignore
        )
    )
    date_str = []
    diff_prop = []
    # Need to iterate over the lists in props, which contain the properties
    # for each date
    for monitor, base in conf_params.global_params.diff_dates:  # type: ignore
        tmp_dict = {}
        for k, v_base in props[lookup[base]].items():
            if k in conf_params.diff_calculation:
                operations = conf_params.diff_calculation[k]
                v_monitor = props[lookup[monitor]][k]
                for op in operations:
                    if op in locals():
                        tmp_dict[k + op] = locals()[op](v_monitor, v_base)
                    else:
                        raise ValueError(
                            f"{__file__}: unknown difference operation: {op}, should "
                            f'be one of "diff","diff_percent" or "ratio"'
                        )
        if tmp_dict:
            diff_prop.append(tmp_dict)
            date_str.append(monitor + "_" + base)
    return diff_prop, date_str


def _verify_diff_inputs(prop_set, conf):
    if not isinstance(prop_set, list):
        raise ValueError(
            f"{__file__}: input grid properties must be contained in a list "
            f"of lists, with one set of properties for each simulator model "
            f"date in the inner lists"
        )
    for prop_list in prop_set:
        if len(prop_list) != len(conf.global_params.seis_dates):
            raise ValueError(
                f"{__file__}: mismatch between property sets and "
                f"simulation model dates: "
                f"{len(prop_list)} vs. {len(conf.global_params.seis_dates)}"
            )
    if not {a for ll in conf.global_params.diff_dates for a in ll}.issubset(
        set(conf.global_params.seis_dates)
    ):
        raise ValueError(
            f"{__file__}: trying to take difference between dates not saved from "
            f"simulation model"
        )
    return


def _filter_diff_inputs(prop_list_list, conf):
    # Filter out the properties that are not in the diff_calculation list.
    # Keep the time-step order in the list
    return_list = [{} for _ in range(len(prop_list_list[0]))]
    for prop_list in prop_list_list:
        for i, prop_set in enumerate(prop_list):
            tmp_dict = {
                k: v for k, v in asdict(prop_set).items() if k in conf.diff_calculation
            }
            if tmp_dict:
                return_list[i].update(tmp_dict)
    if conf.global_params is None:
        raise ValueError(
            f"{__file__}: unable to calculate cumsum values, global "
            f"settings are missing"
        )
    if conf.global_params.seis_dates is None:
        raise ValueError(
            f"{__file__}: unable to calculate cumsum values, global "
            f"settings seismic dates are missing"
        )
    return return_list
