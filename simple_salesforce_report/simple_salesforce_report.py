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
        sf_username: str,
        sf_password: str,
        sf_security_token: str,
        sf_instance: str,
    ) -> None:
        """
        Initialize SalesforceReport with Salesforce credentials.

        Parameters:
        - sf_username (str): The Salesforce username.
        - sf_password (str): The Salesforce password.
        - sf_security_token (str): The Salesforce security token.
        - sf_instance (str): The Salesforce instance URL.
        """
        self.__sf_username = sf_username
        self.__sf_password = sf_password
        self.__sf_security_token = sf_security_token
        self.__sf_instance = sf_instance

        self.__sf = self.__connect_to_salesforce()

    def __connect_to_salesforce(self) -> Optional[Salesforce]:
        """
        Connect to Salesforce using the stored credentials.
        """
        return Salesforce(
            username=self.__sf_username,
            password=self.__sf_password,
            security_token=self.__sf_security_token,
            instance=self.__sf_instance,
        )

    def get_simple_report(self, report_id: str) -> Optional[pd.DataFrame]:
        """
        Retrieve a simple report from Salesforce.

        Parameters:
        - report_id (str): The ID of the report to retrieve.

        Returns:
        - DataFrame containing the report data.
        """
        if self.__sf is None:
            self.__sf = self.__connect_to_salesforce()
        try:
            report_json = self.__sf.restful(f"analytics/reports/{report_id}")
        except SalesforceMalformedRequest as error:
            print(f"Malformed request error: {error}")
            return None  # Handle the error gracefully or raise an exception
        return self.get_simple_report_dataframe(report_json)

    def get_simple_report_dataframe(self, report_json: Dict[str, Any]) -> pd.DataFrame:
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
