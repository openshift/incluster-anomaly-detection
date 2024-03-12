"""Abstract class for the anomaly detection logic."""
import json
from abc import ABCMeta, abstractmethod
from datetime import datetime

import daiquiri

from src.common.config import DAIQUIRI_LOG_LEVEL, ANOMALY_CR_CONFIG

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


class AbstractAnomalyDetector(metaclass=ABCMeta):
    """Abstract class for the anomaly detection."""

    def __init__(self, data, metric_info, config, **kwargs):
        """Init method."""
        self._data = data
        self._metric_info = metric_info
        self._config = config
        self._kwargs = kwargs

    @abstractmethod
    def detect_anomaly(self):
        """Abstract method to detect anomaly."""
        pass

    def build_anomaly_object(self, properties, data=None, **kwargs):
        """Build anomaly object."""
        # build storage object name
        name = (
            f"{datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')}-{self._config['name']}"
        )
        if len(self._metric_info) > 0:
            for _, value in self._metric_info.items():
                name = name + "-" + value

        # convert name based on kubernetes data standards.
        name = name.replace(" ", "-").replace("_", "-").lower()

        # Build anomaly object that will be saved to CR in cluster later point
        anomaly_obj = {
            "apiVersion": f"{ANOMALY_CR_CONFIG['group']}/{ANOMALY_CR_CONFIG['version']}",
            "kind": ANOMALY_CR_CONFIG["kind"],
            "metadata": {
                "label": {"app.kubernetes.io/created-by": "anomaly-engine"},
                "name": name,
            },
            "spec": {
                "anomalyname": self._config.get("name"),
                "method": self._config.get("method"),
                "config": {
                    "query": self._config.get("query"),
                    "step": self._config.get("step"),
                    "percentagechange": self._config.get("percentage_change"),
                    "periodrange": self._config.get("period_range"),
                    "min": self._config.get("min"),
                    "max": self._config.get("max"),
                },
                "metricdata": {
                    "timestamp": properties.get("timestamp"),
                    "latestvalue": properties.get("latest_value"),
                    "percentagechange": properties.get("percentage_change"),
                    "prevdatameanvalue": properties.get("prev_data_mean_value"),
                    "groupeddata": json.dumps(self._metric_info)
                    if len(self._metric_info) > 0
                    else None,
                    "datapoints": json.dumps(data) if data else None,
                },
            },
        }

        if kwargs:
            anomaly_obj = {**anomaly_obj, **kwargs}

        return anomaly_obj
