import configparser
from simple_salesforce import Salesforce
import pandas as pd

class Salesforce_Report():
    def __init__(self, env_filename):
        self.__sf_username, self.__sf_password, self.__sf_security_token, self.__company_name = self.load_env(env_filename)
        
        self.__sf = Salesforce(
        username=self.__sf_username,
        password=self.__sf_password,
        security_token=self.__sf_security_token   
        )
        
        ''

    def load_env(self, env_filename):
        config = configparser.ConfigParser()
        config.read(env_filename)

        # Get Salesforce credentials from the .env file
        salesforce_username = config['DEFAULT']['SALESFORCE_USERNAME']
        salesforce_password = config['DEFAULT']['SALESFORCE_PASSWORD']
        salesforce_security_token = config['DEFAULT']['SALESFORCE_SECURITY_TOKEN']
        company_name = config['DEFAULT']['COMPANY_NAME']

        return salesforce_username, salesforce_password, salesforce_security_token, company_name
    
    def get_simple_report(self, report_id):
        try:
            report_json = self.__sf.restful('analytics/reports/{}'.format(report_id))
        except Exception as e:
            print("Error:", e)
            print("Response Status Code:", getattr(e, "status_code", None))
            return None  # Handle the error gracefully or raise an exception
        
        return self.get_simple_report_dataframe(report_json)
    
    def get_simple_report_dataframe(self, report_json):
        columns = [report_json['reportExtendedMetadata']['detailColumnInfo'][column_key]['label'] for column_key in report_json['reportExtendedMetadata']['detailColumnInfo'].keys()]
        rows = []
        for record in report_json['factMap']['T!T']['rows']:
            column_data = []
            for var in record['dataCells']:
                column_data.append(var['label'])
            rows.append(column_data)
    
        return pd.DataFrame(rows, columns=columns)
    
    
    