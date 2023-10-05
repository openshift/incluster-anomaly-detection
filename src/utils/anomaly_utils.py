"""Helper for the anomaly detection."""
import daiquiri

from src.anomaly.factory import factory_get_class
from src.common.config import DAIQUIRI_LOG_LEVEL

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def get_change_from_telemetry_data(results: dict, config: dict):
    """Get change in the latest data point compared to earlier data."""
    anomaly_lst = []

    if len(results) > 0:
        for item in results:
            data = item.get("values", item.get("value"))
            _logger.debug("----------------Metric data---------------")
            _logger.debug(data)
            _logger.debug("------------------------------------------")

            if len(data) > 0:
                anomaly_detection_cls = factory_get_class(config["method"])
                anomaly_detection_obj = anomaly_detection_cls(
                    data=data, metric_info=item["metric"], config=config
                )
                anomaly = anomaly_detection_obj.detect_anomaly()

                if anomaly:
                    anomaly_lst.append(anomaly)
            else:
                _logger.debug("Not enough data to detect Anomaly")

            if not config["have_multi_result_data"]:
                break
    else:
        _logger.debug("------------------------------------------")
        _logger.debug("Not enough data to detect Anomaly")

    return anomaly_lst
