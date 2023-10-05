"""Util class for common logic."""
import daiquiri

from src.common.config import DAIQUIRI_LOG_LEVEL

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def get_num(value_str):
    """Convert values to number."""
    try:
        return int(value_str)
    except ValueError:
        return float(value_str)


def get_last_data_point(data):
    """Get last data point as numeric type."""
    last_data_points = data[len(data) - 1]
    last_value = get_num(last_data_points[1])
    last_timestamp = get_num(last_data_points[0])
    _logger.debug(
        f"last element: {last_data_points}, last_value: {last_value}, last_timestamp: {last_timestamp}"
    )
    return last_timestamp, last_value
