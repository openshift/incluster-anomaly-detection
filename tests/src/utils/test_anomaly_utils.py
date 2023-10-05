"""Test class for the anomaly util."""
import unittest

from src.common.constants import AnomalyMethod
from src.utils.anomaly_utils import get_change_from_telemetry_data


class AnomalyUtilTest(unittest.TestCase):
    """Test class for the config util."""

    def test_get_change_from_telemetry_data(self):
        """Test get_change_from_telemetry_data logic."""

        config = {
            "min": 60,
            "max": 100,
            "method": AnomalyMethod.MIN_MAX,
            "name": "etcd_object_namespaces",
            "query": 'max(apiserver_storage_objects{resource=~"namespaces"}) by (resource)',
            "have_multi_result_data": False,
        }
        data = [{"metric": {"resource": "namespaces"}, "value": [1695813252.521, "70"]}]

        # Call method
        anomaly_lst = get_change_from_telemetry_data(data, config)

        # assert result
        self.assertEqual(len(anomaly_lst), 0)
