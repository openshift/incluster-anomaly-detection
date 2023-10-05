"""Helper for the kubernetes interaction."""
import daiquiri
from kubernetes import client

from src.common.config import (
    DAIQUIRI_LOG_LEVEL,
)

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def create_cr(anomaly_data):
    """Create CRD object to store anomaly data."""
    custom_api_instance = client.CustomObjectsApi()
    custom_api_instance.create_namespaced_custom_object(
        group="backend.anomaly.io",
        version="v1alpha1",
        namespace="osa-anomaly-detection",
        plural="anomalydata",
        body=anomaly_data,
    )

    _logger.info("Anomaly stored Resource created successfully.")
