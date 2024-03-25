# salesforce_report/__init__.py
"""
Module to initialize the Salesforce report package.

This module imports the Salesforce_Report class from simple_salesforce_report module
and defines the __all__ list for explicit module import.

Usage:
    Import this module in your code to access the Salesforce_Report class:

    >>> from salesforce_report import Salesforce_Report

Contents:
    - Salesforce_Report: A class to interact with Salesforce reports.

Example:
    >>> from salesforce_report import Salesforce_Report
    >>> report = Salesforce_Report(env_filename='config.env')
"""
from .simple_salesforce_report import SalesforceReport

__all__ = ["SalesforceReport"]
