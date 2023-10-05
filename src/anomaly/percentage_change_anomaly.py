"""Anomaly detection logic using percentage-change method."""
from statistics import mean

import daiquiri

from src.anomaly.abstract_anomaly_detector import AbstractAnomalyDetector
from src.common.config import DAIQUIRI_LOG_LEVEL
from src.utils.common_utils import get_last_data_point, get_num

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


class PercentageChangeAnomaly(AbstractAnomalyDetector):
    """Class to detect Anomaly with percentage change method."""

    @staticmethod
    def __get_change(current, previous):
        """Get percentage change based on two values."""
        if current == previous:
            return 0
        try:
            return ((current - previous) / previous) * 100.0
        except ZeroDivisionError:
            return float("inf")

    def detect_anomaly(self):
        """Detect anomaly based on percentage change method."""
        if len(self._data) >= self._config["min_no_of_data_points"]:
            # get latest value
            timestamp, latest_value = get_last_data_point(self._data)

            values = []
            for item in self._data[0: len(self._data) - 1]:
                values.append(get_num(item[1]))
            _logger.debug(f"older values : {values}")

            # get mean value from the previous data points
            mean_value = round(mean(values), 2)
            _logger.debug(f"mean_value from older data points: {mean_value}")

            percentage_change = round(self.__get_change(latest_value, mean_value), 2)
            _logger.debug(f"percentage_change : {percentage_change}")

            if abs(percentage_change) > self._config["percentage_change"]:
                _logger.info(
                    f"Anomaly detected, name: {self._config['name']}, percentage_change: {percentage_change}"
                )
                return self.build_anomaly_object(
                    data=self._data,
                    properties={
                        "percentage_change": percentage_change,
                        "latest_value": latest_value,
                        "timestamp": timestamp,
                        "prev_data_mean_value": mean_value,
                    },
                )
        else:
            _logger.debug(
                f"There is only {len(self._data)} data points available "
                f"while we require minimum {self._config['min_no_of_data_points']} data points to detect Anomaly."
            )

        return None
