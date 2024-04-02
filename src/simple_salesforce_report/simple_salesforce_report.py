"""
Module: simple_salesforce_report.py
A module for interacting with Salesforce reports.
"""

from typing import Any, Dict, Optional
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest
import pandas as pd


class SalesforceReport:
    """
    A class to interact with Salesforce reports.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        security_token: Optional[str] = None,
        domain: Optional[str] = None,
    ):
        """
        Initializes an instance of Simple Salesforce within your module.

        Args:
            username (str): Salesforce username.
            password (str): Salesforce password.
            security_token (str): Salesforce security token.
            domain (str): Salesforce domain.
        """
        self.username = username
        self.password = password
        self.security_token = security_token
        self.domain = domain
        if self.username and self.password and self.security_token:
            self.sf = self.__connect_to_salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
            )
        else:
            raise TypeError(
                "You must provide login information or an instance and token"
            )

    def __connect_to_salesforce(self, *args, **kwargs) -> Optional[Salesforce]:
        """
        Connect to Salesforce using the stored credentials.
        """
        return Salesforce(*args, **kwargs)

    def get_simple_report(self, report_id: str) -> Optional[pd.DataFrame]:
        """
        Retrieve a simple report from Salesforce.

        Parameters:
        - report_id (str): The ID of the report to retrieve.

        Returns:
        - DataFrame containing the report data.
        """

        try:
            report_json = self.sf.restful(f"analytics/reports/{report_id}")
        except SalesforceMalformedRequest as error:
            print(f"Malformed request error: {error}")
            return None  # Handle the error gracefully or raise an exception
        return SalesforceReport.get_simple_report_dataframe(report_json)

    @staticmethod
    def get_simple_report_dataframe(report_json: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert report JSON to a DataFrame.

        Parameters:
        - report_json (dict): JSON representation of the report.

        Returns:
        - DataFrame containing the report data.
        """
        detail_column_info = report_json["reportExtendedMetadata"]["detailColumnInfo"]
        columns = [
            detail_column_info[column_key]["label"]
            for column_key in detail_column_info.keys()
        ]
        rows = []
        for record in report_json["factMap"]["T!T"]["rows"]:
            column_data = []
            for var in record["dataCells"]:
                column_data.append(var["label"])
            rows.append(column_data)
        return pd.DataFrame(rows, columns=columns)
