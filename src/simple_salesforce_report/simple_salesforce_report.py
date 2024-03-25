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
        **kwargs
    ):
        """
        Initializes an instance of Simple Salesforce within your module.

        Args:
            username (str): Salesforce username.
            password (str): Salesforce password.
            security_token (str): Salesforce security token.
            session_id (str): Salesforce session ID.
            instance (str): Salesforce instance URL.
            instance_url (str): Salesforce instance URL.
            organizationId (str): Salesforce organization ID.
            version (str): Salesforce API version.
            proxies (dict): Proxy configuration.
            session (requests.Session): HTTP session.
            client_id (str): Salesforce client ID.
            domain (str): Salesforce domain.
            consumer_key (str): Salesforce consumer key.
            consumer_secret (str): Salesforce consumer secret.
            privatekey_file (str): Path to private key file.
            privatekey (str): Private key.
            parse_float (Callable[[str], Any]): Function to parse floats.
            object_pairs_hook (Callable[[List[Tuple[Any, Any]]], Any]): 
                Function to hook for converting JSON object pairs.

            **kwargs: Additional keyword arguments to pass to Simple Salesforce.
        """
        self.__sf = self.__connect_to_salesforce(
            username=username,
            password=password,
            security_token=security_token,
            **kwargs
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
