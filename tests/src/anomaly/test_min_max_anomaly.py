"""Test cases for the min/max anomaly detection logic."""
from unittest import TestCase

from src.anomaly.min_max_anomaly import MinMaxAnomaly


class MinMaxAnomalyTestCase(TestCase):
    """Test class for the min_max anomaly detection."""

    def setUp(self):
        """Setup for the test cases."""
        self._config = {
            "max": 100,
            "method": "min_max",
            "min": 65,
            "name": "etcd_object_namespaces",
            "query": 'max(apiserver_storage_objects{resource=~"namespaces"}) by (resource)',
        }

    def test_detect_anomaly_with_anomaly(self):
        """Test detect_anomaly with data having outliers."""
        data = [1689083181, "300"]

        # create anomaly detection class object and call detect_anomaly method
        anomaly_detection_obj = MinMaxAnomaly(
            data=data, metric_info={"resource": "namespace"}, config=self._config
        )
        anomaly = anomaly_detection_obj.detect_anomaly()

        # assert results
        self.assertIsNotNone(anomaly)
        self.assertTrue("spec" in anomaly)
        self.assertEqual(anomaly["spec"]["anomalyname"], self._config["name"])
        self.assertEqual(anomaly["spec"]["method"], self._config["method"])

        self.assertTrue("config" in anomaly["spec"])
        self.assertEqual(anomaly["spec"]["config"]["query"], self._config["query"])
        self.assertEqual(anomaly["spec"]["config"]["min"], self._config["min"])
        self.assertEqual(anomaly["spec"]["config"]["max"], self._config["max"])

        self.assertTrue("metricdata" in anomaly["spec"])
        self.assertEqual(anomaly["spec"]["metricdata"]["timestamp"], 1689083181)
        self.assertEqual(anomaly["spec"]["metricdata"]["latestvalue"], 300)
        self.assertEqual(
            anomaly["spec"]["metricdata"]["groupeddata"], '{"resource": "namespace"}'
        )

    def test_detect_anomaly_without_anomaly(self):
        """Test detect_anomaly with data within defined range."""
        data = [1689083181, "80"]

        # create anomaly detection class object and call detect_anomaly method
        anomaly_detection_obj = MinMaxAnomaly(
            data=data, metric_info={"resource": "namespace"}, config=self._config
        )
        anomaly = anomaly_detection_obj.detect_anomaly()

        # assert results
        self.assertIsNone(anomaly)
