"""
Test module for the SalesforceReport class.
"""

import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from simple_salesforce_report import SalesforceReport


class TestSimpleSalesforceReport(unittest.TestCase):
    """Tests the functionality of the SalesforceReport class."""

    # Sample report JSON data
    sample_report_json = {
        "reportExtendedMetadata": {
            "detailColumnInfo": {
                "column1": {"label": "Column 1"},
                "column2": {"label": "Column 2"},
            }
        },
        "factMap": {
            "T!T": {
                "rows": [
                    {"dataCells": [{"label": "Value 1"}, {"label": "Value 2"}]},
                    {"dataCells": [{"label": "Value 3"}, {"label": "Value 4"}]},
                ]
            }
        },
    }

    @patch(
        "simple_salesforce_report.simple_salesforce_report.Salesforce"
    )  # Patch the Salesforce object
    def test_init_valid_credentials(self, mock_sf):
        """Tests the functionality of the SalesforceReport class."""
        # Create a mock Salesforce instance
        mock_sf.return_value = MagicMock()

        report = SalesforceReport(
            username="testuser",
            password="testpass",
            security_token="mytoken",
            domain="test.salesforce.com",
        )

        # Assertions
        self.assertEqual(report.username, "testuser")
        # ... more assertions for other attributes
        mock_sf.assert_called_once_with(  # Verify connection was attempted
            username="testuser",
            password="testpass",
            security_token="mytoken",
            instance_url="test.salesforce.com",
        )

    def test_init_missing_credentials(self):
        """
        Tests that an error is raised when
        SalesforceReport is initialized without credentials.
        """
        with self.assertRaises(TypeError) as cm:
            SalesforceReport()  # No credentials provided

        self.assertEqual(
            str(cm.exception),
            "You must provide login information or an instance and token",
        )

    def test_get_simple_report_dataframe(self):  # Assuming you have a fixture
        """Tests the get_simple_report_dataframe method."""
        result_df = SalesforceReport.get_simple_report_dataframe(
            TestSimpleSalesforceReport.sample_report_json
        )

        # Assert the DataFrame structure
        assert isinstance(result_df, pd.DataFrame)
        assert list(result_df.columns) == ["Column 1", "Column 2"]

        # Assert the DataFrame content
        expected_df = pd.DataFrame(
            [["Value 1", "Value 2"], ["Value 3", "Value 4"]],
            columns=["Column 1", "Column 2"],
        )
        pd.testing.assert_frame_equal(result_df, expected_df)
