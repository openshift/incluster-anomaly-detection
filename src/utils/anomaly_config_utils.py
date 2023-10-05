"""Util class for the config logic."""
import daiquiri

from src.common.config import (
    DAIQUIRI_LOG_LEVEL,
    MIN_VALUE,
    MAX_VALUE,
    DEFAULT_STEP,
    DEFAULT_ANOMALY_PERCENTAGE,
    DEFAULT_ANOMALY_PERIOD,
    MIN_NO_OF_DATA_POINTS,
    ANOMALY_CONFIG_FILE,
)
from src.common.constants import AnomalyMethod
from src.utils.file_utils import get_json_from_yaml_file

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def get_metric_config(config_file: str = ANOMALY_CONFIG_FILE, query_names: list = None):
    """Merge metric properties with default parameter."""
    config_data = get_json_from_yaml_file(config_file)
    config_lst = {}
    if config_data is not None:
        for item_name, item in config_data.items():
            if query_names is None or item_name in query_names:
                if "query" in item and item["query"].strip():
                    query_config = item
                    query_config["name"] = query_config.get("name", item_name)
                    query_config["have_multi_result_data"] = item.get(
                        "have_multi_result_data", True
                    )

                    if "method" not in query_config:
                        query_config["method"] = AnomalyMethod.PERCENTAGE_CHANGE
                    else:
                        query_config["method"] = AnomalyMethod(
                            query_config["method"].lower()
                        )

                    if query_config["method"] == AnomalyMethod.MIN_MAX:
                        default_parameters = {"min": MIN_VALUE, "max": MAX_VALUE}

                    elif query_config["method"] == AnomalyMethod.PERCENTAGE_CHANGE:
                        default_parameters = {
                            "step": DEFAULT_STEP,
                            "percentage_change": DEFAULT_ANOMALY_PERCENTAGE,
                            "period_range": DEFAULT_ANOMALY_PERIOD,
                            "min_no_of_data_points": MIN_NO_OF_DATA_POINTS,
                        }

                    # update config with default parameters
                    query_config = {**default_parameters, **query_config}
                    config_lst[item_name] = query_config
                else:
                    _logger.error(f"Query not present for '{item_name}'")

    else:
        _logger.error(f"No anomaly config found @ '{config_file}' location")

    return config_lst
