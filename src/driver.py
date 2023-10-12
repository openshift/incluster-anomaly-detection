"""Driver for in-cluster metric data access and detect basic anomaly."""
import datetime
import json
import sys

import daiquiri
from kubernetes.config import load_incluster_config

from src.common.config import (
    DAIQUIRI_LOG_LEVEL,
    ANOMALY_CONFIG_FILE,
)
from src.common.constants import AnomalyMethod
from src.utils.anomaly_config_utils import get_metric_config
from src.utils.anomaly_utils import get_change_from_telemetry_data
from src.utils.arg_utils import get_arguments
from src.utils.kube_utils import create_cr
from src.utils.thanos_utils import get_metric_query_range, get_metric_data

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def __get_telemetry_data(config: dict):
    """Get telemetry data points."""
    if config["method"] == AnomalyMethod.PERCENTAGE_CHANGE:
        current_time = datetime.datetime.now()

        end_time = current_time.replace(microsecond=0).replace(second=0)

        start_time = end_time - datetime.timedelta(minutes=config["period_range"])
        _logger.info(f"start_time: {start_time}, end_time: {end_time}")
        response = get_metric_query_range(
            query=config["query"],
            start_time=start_time,
            end_time=end_time,
            step_seconds=config["step"] * 60,
        )
    else:
        response = get_metric_data(query=config["query"])

    return response


def main():
    """Start of the main logic."""
    _logger.info("Inside main method")
    # get arguments
    args = get_arguments(sys.argv[1:])
    query_configs = get_metric_config(ANOMALY_CONFIG_FILE, args.anomaly_queries)
    _logger.debug(f"No of queries : {len(query_configs)}")

    try:
        anomaly_lst = []
        for key, config in query_configs.items():
            _logger.info(f"query_name: {key}, configuration: {config}")

            # get telemetry data points
            response = __get_telemetry_data(config)

            if response:
                data = response["data"]["result"]
                temp_anomaly_lst = get_change_from_telemetry_data(data, config)
                anomaly_lst.extend(temp_anomaly_lst)

        _logger.info("-----------anomaly_lst-----------")
        if len(anomaly_lst) > 0:
            json_str = json.dumps(anomaly_lst, indent=4, sort_keys=True)
            _logger.info(json_str)
            load_incluster_config()

            for item in anomaly_lst:
                create_cr(item)
        else:
            _logger.info("No Anomaly Found")
        _logger.info("---------------------------------")

    except Exception as ex:
        _logger.error("error occurred")
        raise ex

    _logger.info("Anomaly Detection Program Completed.")


if __name__ == "__main__":
    main()
