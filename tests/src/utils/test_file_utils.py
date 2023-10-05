"""Test class for the file util logic."""
import unittest

from src.utils.file_utils import get_json_from_yaml_file


class FileUtilsTestCase(unittest.TestCase):
    """File util test class."""

    def test_get_json_from_yaml_valid_file_path(self):
        """Test logic of get_json_from_yaml_file with valid file path."""
        file_path = "tests/src/data_asset/test_anomaly_config.yaml"

        # method call
        data = get_json_from_yaml_file(file_path)

        # assert result
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 6)
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "min_max_default",
                    "percentage_change_default",
                    "invalid_config",
                    "kube_configmap_info",
                    "etcd_object_namespaces",
                    "etcd_object_secrets_config_maps",
                ]
            ),
        )

        config_map_data = data["kube_configmap_info"]
        self.assertIsNotNone(config_map_data)
        self.assertEqual(config_map_data["query"], "count(kube_configmap_info)")
        self.assertEqual(config_map_data["step"], 2)
        self.assertEqual(config_map_data["period_range"], 60)
        self.assertEqual(config_map_data["percentage_change"], 60)
        self.assertEqual(config_map_data["have_multi_result_data"], False)

        namespaces = data["etcd_object_namespaces"]
        self.assertIsNotNone(namespaces)
        self.assertEqual(
            namespaces["query"],
            'max(apiserver_storage_objects{resource=~"namespaces"}) by (resource)',
        )
        self.assertEqual(namespaces["min"], 65)
        self.assertEqual(namespaces["max"], 100)

        secret_config_maps = data["etcd_object_namespaces"]
        self.assertIsNotNone(secret_config_maps)

    def test_get_json_from_yaml_invalid_file_path(self):
        """Test logic of get_json_from_yaml_file with invalid file path."""
        file_path = "file_not_exist.yaml"

        # method call
        data = get_json_from_yaml_file(file_path)

        # assert result
        self.assertIsNone(data)
