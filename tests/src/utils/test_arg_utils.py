"""Test class for the argument parser."""
import unittest

from src.utils.arg_utils import get_arguments


class AnomalyParserTest(unittest.TestCase):
    """Test class for the arg parser"""

    def test_without_args(self):
        """Test parser get_arguments without any arguments."""
        # Call method
        parsed_data = get_arguments([])

        # assert result
        self.assertEqual(len(vars(parsed_data).items()), 1)
        self.assertIsNone(parsed_data.anomaly_queries)

    def test_actual_argument(self):
        """Test parser get_arguments with supplied argument data."""

        # prepare arguments data
        anomaly_report_name = "test1,test2"
        args = ["--anomaly_queries", anomaly_report_name]

        # Call method
        parsed_data = get_arguments(args)

        # assert data
        self.assertEqual(len(vars(parsed_data).items()), 1)
        self.assertEqual(parsed_data.anomaly_queries, ["test1", "test2"])
