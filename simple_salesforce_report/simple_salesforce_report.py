"""
Module: simple_salesforce_report.py
A module for interacting with Salesforce reports.
"""
import configparser
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest
import pandas as pd
class SalesforceReport():
    """
    A class to interact with Salesforce reports.
    """
    def __init__(self, env_filename):
        """
        Initialize SalesforceReport with Salesforce credentials loaded from an environment file.

        Parameters:
        - env_filename (str): The path to the environment file.
        """
        self.__sf_username, \
        self.__sf_password, \
        self.__sf_security_token, \
        self.__instance = self.load_env(env_filename)

        self.__sf = self.__connect_to_salesforce()

    def __connect_to_salesforce(self):
        """
        Connect to Salesforce using the stored credentials.
        """
        return Salesforce(
            username=self.__sf_username,
            password=self.__sf_password,
            security_token=self.__sf_security_token,
            instance=self.__instance,
        )

    def load_env(self, env_filename):
        """
        Load Salesforce credentials from the environment file.

        Parameters:
        - env_filename (str): The path to the environment file.

        Returns:
        - Tuple containing Salesforce credentials.
        """
        config = configparser.ConfigParser()
        config.read(env_filename)

        # Get Salesforce credentials from the .env file
        salesforce_username = config['DEFAULT']['SALESFORCE_USERNAME']
        salesforce_password = config['DEFAULT']['SALESFORCE_PASSWORD']
        salesforce_security_token = config['DEFAULT']['SALESFORCE_SECURITY_TOKEN']
        instance = config['DEFAULT']['INSTANCE']

        return salesforce_username, salesforce_password, salesforce_security_token, instance

    def get_simple_report(self, report_id):
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
            report_json = self.__sf.restful(f'analytics/reports/{report_id}')
        except SalesforceMalformedRequest as error:
            print(f"Malformed request error: {error}")
            return None #Handle the error gracefully or raise an exception
        return self.get_simple_report_dataframe(report_json)

    def get_simple_report_dataframe(self, report_json):
        """
        Convert report JSON to a DataFrame.

        Parameters:
        - report_json (dict): JSON representation of the report.

        Returns:
        - DataFrame containing the report data.
        """
        detail_column_info = report_json['reportExtendedMetadata']['detailColumnInfo']
        columns = [
            detail_column_info[column_key]['label']
            for column_key in detail_column_info.keys()
        ]
        rows = []
        for record in report_json['factMap']['T!T']['rows']:
            column_data = []
            for var in record['dataCells']:
                column_data.append(var['label'])
            rows.append(column_data)
        return pd.DataFrame(rows, columns=columns)
