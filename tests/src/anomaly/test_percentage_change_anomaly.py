"""Test cases for the percentage_change anomaly detection logic."""
import json
from unittest import TestCase

from src.anomaly.percentage_change_anomaly import PercentageChangeAnomaly


class PercentageChangeAnomalyTestCase(TestCase):
    """Test class for the percentage_change anomaly detection."""

    def setUp(self):
        """Setup for the test cases."""
        self._config = {
            "step": 2,
            "percentage_change": 60,
            "min_no_of_data_points": 5,
            "query": "max(apiserver_storage_objects) by (resource)",
            "period_range": 20,
            "method": "percentage_change",
            "have_multi_result_data": True,
            "name": "etcd_object",
        }

    def test_detect_anomaly_with_anomaly(self):
        """Test detect_anomaly with data having outliers."""
        data = [
            [1690372380, "518"],
            [1690372500, "510"],
            [1690372620, "513"],
            [1690372740, "520"],
            [1690372860, "520"],
            [1690372980, "518"],
            [1690372740, "520"],
            [1690372860, "520"],
            [1690372980, "518"],
            [1690373100, "980"],
        ]

        # create anomaly detection class object and call detect_anomaly method
        anomaly_detection_obj = PercentageChangeAnomaly(
            data=data, metric_info={"resource": "configmaps"}, config=self._config
        )
        anomaly = anomaly_detection_obj.detect_anomaly()

        # assert results
        self.assertIsNotNone(anomaly)

        self.assertTrue("spec" in anomaly)
        self.assertEqual(anomaly["spec"]["method"], self._config["method"])
        self.assertEqual(anomaly["spec"]["anomalyname"], self._config["name"])

        self.assertTrue("config" in anomaly["spec"])
        self.assertEqual(anomaly["spec"]["config"]["query"], self._config["query"])
        self.assertEqual(
            anomaly["spec"]["config"]["percentagechange"],
            self._config["percentage_change"],
        )
        self.assertEqual(anomaly["spec"]["config"]["step"], self._config["step"])
        self.assertEqual(
            anomaly["spec"]["config"]["periodrange"], self._config["period_range"]
        )

        self.assertTrue("metricdata" in anomaly["spec"])
        self.assertEqual(anomaly["spec"]["metricdata"]["timestamp"], 1690373100)
        self.assertEqual(anomaly["spec"]["metricdata"]["latestvalue"], 980)
        self.assertEqual(anomaly["spec"]["metricdata"]["percentagechange"], 89.39)
        self.assertEqual(anomaly["spec"]["metricdata"]["prevdatameanvalue"], 517.44)
        self.assertEqual(json.loads(anomaly["spec"]["metricdata"]["datapoints"]), data)

    def test_detect_anomaly_without_anomaly(self):
        """Test detect_anomaly with data within defined range."""
        data = [
            [1690372380, "518"],
            [1690372500, "510"],
            [1690372620, "513"],
            [1690372740, "520"],
            [1690372860, "520"],
            [1690372980, "518"],
            [1690373100, "525"],
            [1690372740, "520"],
            [1690372860, "520"],
            [1690372980, "650"],
        ]

        # create anomaly detection class object and call detect_anomaly method
        anomaly_detection_obj = PercentageChangeAnomaly(
            data=data, metric_info={"resource": "configmaps"}, config=self._config
        )
        anomaly = anomaly_detection_obj.detect_anomaly()

        # assert results
        self.assertIsNone(anomaly)

    def test_detect_anomaly_without_minimum_data(self):
        """Test detect_anomaly with data within defined range."""
        data = [
            [1690372380, "518"],
            [1690372500, "510"],
            [1690372620, "513"],
            [1690372740, "1350"],
        ]

        # create anomaly detection class object and call detect_anomaly method
        anomaly_detection_obj = PercentageChangeAnomaly(
            data=data, metric_info={"resource": "configmaps"}, config=self._config
        )
        anomaly = anomaly_detection_obj.detect_anomaly()

        # assert results
        self.assertIsNone(anomaly)
