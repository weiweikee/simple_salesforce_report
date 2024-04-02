"""
Test module for the SalesforceReport class.
"""
import pytest
import pandas as pd
from simple_salesforce_report import SalesforceReport


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


def test_initialization_missing_credentials():
    """Tests that a TypeError is raised when credentials are missing during initialization."""
    with pytest.raises(TypeError) as excinfo:
        SalesforceReport()
    assert "You must provide login information or an instance and token" in str(
        excinfo.value
    )


def test_get_simple_report_dataframe():  # Assuming you have a fixture
    """Tests the get_simple_report_dataframe method.""" 
    result_df = SalesforceReport.get_simple_report_dataframe(sample_report_json)

    # Assert the DataFrame structure
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == ["Column 1", "Column 2"]

    # Assert the DataFrame content
    expected_df = pd.DataFrame(
        [["Value 1", "Value 2"], ["Value 3", "Value 4"]],
        columns=["Column 1", "Column 2"],
    )
    pd.testing.assert_frame_equal(result_df, expected_df)
