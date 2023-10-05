"""Test class for the factory logic."""
import unittest

from src.anomaly.factory import factory_get_class
from src.anomaly.min_max_anomaly import MinMaxAnomaly
from src.anomaly.percentage_change_anomaly import PercentageChangeAnomaly


class FactoryTestCase(unittest.TestCase):
    """Factory logic test class."""

    def test_factory_get_class_default_param(self):
        """Test logic of factory_get_class with default param."""
        # method call
        anomaly_cls = factory_get_class()

        # assert result
        self.assertIs(anomaly_cls, PercentageChangeAnomaly)

    def test_factory_get_class_without_default_param(self):
        """Test logic of factory_get_class without default param."""
        # method call
        anomaly_cls = factory_get_class(anomaly_detection_type="min_max")

        # assert result
        self.assertIs(anomaly_cls, MinMaxAnomaly)
