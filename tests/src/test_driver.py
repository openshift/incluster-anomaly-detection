"""Test class for the driver."""
from argparse import Namespace
from unittest import mock, TestCase

from src.driver import main


class DriverTestCase(TestCase):
    """Test class for the driver logic."""

    @mock.patch("src.driver.load_incluster_config")
    @mock.patch("src.driver.create_cr")
    @mock.patch("src.driver.get_change_from_telemetry_data")
    @mock.patch("src.driver.get_metric_data")
    @mock.patch("src.driver.get_metric_query_range")
    @mock.patch("src.driver.get_arguments")
    def test_main_default(
        self,
        _mock_get_argument,
        _mock_get_metric_query_range,
        _mock_get_metric_data,
        _mock_get_change_from_telemetry_data,
        _mock_create_cr,
        _mock_load_kube_config,
    ):
        """Test main method with default arguments."""
        _mock_get_argument.return_value = Namespace(anomaly_queries=None)

        # Call main method.
        main()

        # Assert call counts
        self.assertEqual(_mock_get_argument.call_count, 1)
        self.assertEqual(_mock_get_metric_query_range.call_count, 2)
        self.assertEqual(_mock_get_metric_data.call_count, 1)
        self.assertEqual(_mock_get_change_from_telemetry_data.call_count, 3)

    @mock.patch("src.driver.load_incluster_config")
    @mock.patch("src.driver.create_cr")
    @mock.patch("src.driver.get_change_from_telemetry_data")
    @mock.patch("src.driver.get_metric_data")
    @mock.patch("src.driver.get_metric_query_range")
    @mock.patch("src.driver.get_arguments")
    def test_main_with_given_anomaly_query(
        self,
        _mock_get_argument,
        _mock_get_metric_query_range,
        _mock_get_metric_data,
        _mock_get_change_from_telemetry_data,
        _mock_create_cr,
        _mock_load_kube_config,
    ):
        """Test main method with given anomaly queries."""
        _mock_get_argument.return_value = Namespace(
            anomaly_queries="kube_configmap_info,etcd_object_namespaces,dummy"
        )
        _mock_get_change_from_telemetry_data.side_effect = [[{"call1": "data"}], []]

        # Call main method.
        main()

        # Assert call counts
        self.assertEqual(_mock_get_argument.call_count, 1)
        self.assertEqual(_mock_get_metric_query_range.call_count, 1)
        self.assertEqual(_mock_get_metric_data.call_count, 1)
        self.assertEqual(_mock_get_change_from_telemetry_data.call_count, 2)
        self.assertEqual(_mock_create_cr.call_count, 1)
