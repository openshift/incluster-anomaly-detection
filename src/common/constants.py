"""Constant file."""
from enum import Enum

from src.common.config import ACCESS_TOKEN, THANOS_QUERIER_HOST

REQUEST_HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

HTTP_PROTOCOL = "https"
THANOS_API = f"{HTTP_PROTOCOL}://{THANOS_QUERIER_HOST}/api/v1/query"
THANOS_QUERY_RANGE_API = f"{HTTP_PROTOCOL}://{THANOS_QUERIER_HOST}/api/v1/query_range"


# Enum to store AnomalyDetectionType options
class AnomalyMethod(str, Enum):
    """Enum class to store Anomaly detection methods."""

    MIN_MAX = "min_max"
    PERCENTAGE_CHANGE = "percentage_change"

    @classmethod
    def get_values(cls):
        """Get values."""
        return [item.value for item in cls]
