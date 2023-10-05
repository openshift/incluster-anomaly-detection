"""Anomaly detection logic using min-max method."""
import daiquiri

from src.anomaly.abstract_anomaly_detector import AbstractAnomalyDetector
from src.common.config import DAIQUIRI_LOG_LEVEL
from src.utils.common_utils import get_num

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


class MinMaxAnomaly(AbstractAnomalyDetector):
    """Class to detect Anomaly with min_max method."""

    def detect_anomaly(self):
        """Detect anomaly based on min/max method."""
        latest_value = get_num(self._data[1])
        timestamp = get_num(self._data[0])

        if latest_value < self._config["min"] or latest_value > self._config["max"]:
            _logger.info(
                f"Anomaly detected, name: {self._config['name']}, latest_value: {latest_value}"
            )
            return self.build_anomaly_object(
                properties={"latest_value": latest_value, "timestamp": timestamp}
            )

        return None
