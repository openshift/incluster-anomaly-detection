"""Helper for the thanos api interaction."""
import datetime
import json

import daiquiri
import requests

from src.common.config import DAIQUIRI_LOG_LEVEL
from src.common.constants import THANOS_API, REQUEST_HEADERS, THANOS_QUERY_RANGE_API

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def __parse_thanos_response(response):
    """Parse thanos api response text."""
    if response.status_code == 200:
        return json.loads(response.text)

    _logger.error(
        f"thanos api response status_code : {response.status_code}, reason: { response.reason}"
    )
    return None


def get_metric_data(query: str, limit: int = 100):
    """Get metric data."""
    params = {"query": query, "limit": limit}
    url = THANOS_API
    _logger.info(f"url: {url}, params: {params}")

    response = requests.get(
        url=url, params=params, headers=REQUEST_HEADERS, verify=False
    )

    return __parse_thanos_response(response)


def get_metric_query_range(
    query: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    step_seconds=300,
):
    """Get metric data for given time range."""
    params = {
        "query": query,
        "start": start_time.strftime("%s"),
        "end": end_time.strftime("%s"),
        "step": step_seconds,
    }

    url = THANOS_QUERY_RANGE_API

    _logger.info(f"url: {url}, params: {params}")

    response = requests.get(
        url=url, params=params, headers=REQUEST_HEADERS, verify=False
    )

    return __parse_thanos_response(response)
