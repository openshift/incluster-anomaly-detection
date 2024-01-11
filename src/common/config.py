"""Config file."""
import os

DAIQUIRI_LOG_LEVEL = os.environ.get("DAIQUIRI_LOG_LEVEL", "DEBUG").upper()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", None)
THANOS_QUERIER_HOST = os.environ.get(
    "THANOS_HOST", "thanos-querier.openshift-monitoring.svc.cluster.local:9091"
)

ANOMALY_CONFIG_FILE = os.environ.get(
    "ANOMALY_CONFIG_FILE", "src/data_asset/anomaly_config.yaml"
)

# Default parameter for the "percentage_change" query type
DEFAULT_ANOMALY_PERCENTAGE = int(os.environ.get("DEFAULT_ANOMALY_PERCENTAGE", 100))
DEFAULT_STEP = int(os.environ.get("DEFAULT_STEP", 5))
DEFAULT_ANOMALY_PERIOD = int(os.environ.get("DEFAULT_ANOMALY_PERIOD", 60))
MIN_NO_OF_DATA_POINTS = int(os.environ.get("MIN_NO_OF_DATA_POINTS", 10))

# Default parameter for the "min_max" query type
MIN_VALUE = int(os.environ.get("MIN_VALUE", 100))
MAX_VALUE = int(os.environ.get("MAX_VALUE", 1000))

# Config to store anomaly data into `AnomalyData` CR
ANOMALY_CR_CONFIG = {
    "group": os.environ.get("ANOMALY_CR_GROUP", "observability-analytics.redhat.com"),
    "version": os.environ.get("ANOMALY_CR_VERSION", "v1alpha1"),
    "namespace": os.environ.get("ANOMALY_CR_NAMESPACE", "osa-anomaly-detection"),
    "plural": os.environ.get("ANOMALY_CR_PLURAL", "anomalydata"),
    "kind": os.environ.get("ANOMALY_CR_kIND", "AnomalyData"),
}
