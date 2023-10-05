"""Test class for the thanos logic."""
import json
import unittest
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from src.utils.thanos_utils import get_metric_data, get_metric_query_range


class ThanosUtilsTestCase(unittest.TestCase):
    """Thanos util test class."""

    @patch("src.utils.thanos_utils.requests.get")
    def test_get_metric_data(self, mock_requests):
        """Test get_metric_data logic."""
        # setup data
        with open(
            "tests/src/data_asset/sample_thanos_latest_data_response.json", "r"
        ) as f:
            sample_telemetry_json_data = json.load(f)

        # thanos returning data in text format so converting json into str using json.dumps and final result as object
        mock_requests.return_value = json.loads(
            json.dumps(
                {"status_code": 200, "text": json.dumps(sample_telemetry_json_data)}
            ),
            object_hook=lambda d: SimpleNamespace(**d),
        )

        # method call
        data = get_metric_data(
            query='max(apiserver_storage_objects{resource=~"secrets|configmaps"}) by (resource)'
        )

        # assert results
        self.assertIsNotNone(data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]["result"]), 2)
        self.assertEqual(data["data"]["result"][0]["metric"]["resource"], "configmaps")
        self.assertEqual(len(data["data"]["result"][0]["values"]), 1)
        self.assertEqual(data["data"]["result"][0]["values"][0][1], "514")

    @patch("src.utils.thanos_utils.requests.get")
    def test_get_metric_query_range(self, mock_requests):
        """Test get_metric_data logic."""
        # setup data
        with open(
            "tests/src/data_asset/sample_thanos_time_range_response.json", "r"
        ) as f:
            sample_telemetry_json_data = json.load(f)

        # thanos returning data in text format so converting json into str using json.dumps and final result as object
        mock_requests.return_value = json.loads(
            json.dumps(
                {"status_code": 200, "text": json.dumps(sample_telemetry_json_data)}
            ),
            object_hook=lambda d: SimpleNamespace(**d),
        )

        # method call
        data = get_metric_query_range(
            query="count(kube_configmap_info)",
            start_time=datetime.utcnow() - timedelta(minutes=60),
            end_time=datetime.utcnow(),
            step_seconds=300,
        )

        # assert results
        self.assertIsNotNone(data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]["result"]), 1)
        self.assertEqual(len(data["data"]["result"][0]["metric"]), 0)
        self.assertEqual(len(data["data"]["result"][0]["values"]), 10)
        self.assertEqual(data["data"]["result"][0]["values"][0][1], "532")
        self.assertEqual(data["data"]["result"][0]["values"][9][1], "544")
