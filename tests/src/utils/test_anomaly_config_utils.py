"""Test class for the anomaly config util."""
import unittest

from src.common.constants import AnomalyMethod
from src.utils.anomaly_config_utils import get_metric_config


class AnomalyConfigUtilTest(unittest.TestCase):
    """Test class for the config util."""

    def test_get_metric_config(self):
        """Test get_metric_config logic."""
        # Call method
        config_lst = get_metric_config(
            config_file="tests/src/data_asset/test_anomaly_config.yaml",
            query_names=None,
        )

        # assert result
        self.assertEqual(
            set(config_lst.keys()),
            set(
                [
                    "kube_configmap_info",
                    "etcd_object_namespaces",
                    "etcd_object_secrets_config_maps",
                    "min_max_default",
                    "percentage_change_default",
                ]
            ),
        )

        # assert kube_configmap_info properties
        kube_configmap_info = config_lst["kube_configmap_info"]
        self.assertEqual(kube_configmap_info["step"], 2)
        self.assertEqual(kube_configmap_info["percentage_change"], 60)
        self.assertEqual(kube_configmap_info["period_range"], 60)
        self.assertEqual(kube_configmap_info["min_no_of_data_points"], 10)
        self.assertEqual(kube_configmap_info["method"], AnomalyMethod.PERCENTAGE_CHANGE)
        self.assertEqual(kube_configmap_info["query"], "count(kube_configmap_info)")
        self.assertEqual(kube_configmap_info["have_multi_result_data"], False)

        # assert etcd_object_namespaces properties
        namespace_prop = config_lst["etcd_object_namespaces"]
        self.assertEqual(namespace_prop["min"], 65)
        self.assertEqual(namespace_prop["max"], 100)
        self.assertEqual(namespace_prop["method"], AnomalyMethod.MIN_MAX)
        self.assertEqual(
            namespace_prop["query"],
            'max(apiserver_storage_objects{resource=~"namespaces"}) by (resource)',
        )
        self.assertEqual(namespace_prop["have_multi_result_data"], True)
