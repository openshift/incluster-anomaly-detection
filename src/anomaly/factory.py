"""factory logic to return relevant class based on anomaly detection type/method."""
from src.anomaly.min_max_anomaly import MinMaxAnomaly
from src.anomaly.percentage_change_anomaly import PercentageChangeAnomaly
from src.common.constants import AnomalyMethod


def factory_get_class(
    anomaly_detection_type: AnomalyMethod = AnomalyMethod.PERCENTAGE_CHANGE,
):
    """Get type of class based on anomaly_detection_type/method."""
    types = {
        AnomalyMethod.PERCENTAGE_CHANGE: PercentageChangeAnomaly,
        AnomalyMethod.MIN_MAX: MinMaxAnomaly,
    }

    return types[anomaly_detection_type]
