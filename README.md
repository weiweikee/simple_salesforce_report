# Simple Salesforce Report
[![Pylint](https://github.com/weiweikee/simple_salesforce_report/actions/workflows/pylint.yml/badge.svg)](https://github.com/weiweikee/simple_salesforce_report/actions/workflows/pylint.yml)
[![Pytest](https://github.com/weiweikee/simple_salesforce_report/actions/workflows/pytest.yml/badge.svg)](https://github.com/weiweikee/simple_salesforce_report/actions/workflows/pylint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/weiweikee/simple_salesforce_report/blob/main/LICENSE)

The Salesforce Report Package is a Python library that provides functionality to interact with Salesforce reports using the [Simple Salesforce](https://github.com/simple-salesforce/simple-salesforce).
> [!WARNING]
> [Salesforce Reports and Dashboards REST API only support 2000 rows](https://developer.salesforce.com/docs/atlas.en-us.api_analytics.meta/api_analytics/sforce_analytics_rest_api_limits_limitations.htm)

--- 
## Overview
This package enables you to retrieve Salesforce reports and convert them into pandas DataFrames for further analysis and processing within your Python environment. It simplifies the process of fetching Salesforce report data and makes it easy to work with in data analysis workflows.

> [!IMPORTANT]
> This only works for salesforce report that do **NOT** have <ins>**GROUPED ROWS**</ins> or <ins>**GROUPED COLUMNS**</ins> for now.

## Installation
To install the package, you can use pip:
```
pip install git+https://github.com/weiweikee/simple_salesforce_report
```

To upgrade the package, you can use:
```
pip install --upgrade git+https://github.com/weiweikee/simple_salesforce_report
```

## Usage
To use this package

1. First import the Salesforce_Report object.

```
from simple_salesforce_report import Salesforce_Report
```
2. Providing an environment file containing Salesforce credentials and company information.
```
sf_report = Salesforce_Report(
        sf_username,
        sf_password,
        sf_security_token,
        sf_domain,
    )
```
Please refer to [example.env](example.env) for arguments examples.

3. Then, you can retrieve reports and convert them into pandas DataFrames.
```
df = sf_report.get_simple_report(report_id)
```
## Dependencies
- simple_salesforce: A Python library for interacting with Salesforce APIs.
- pandas: A powerful data manipulation library in Python.

## License
This package is licensed under the MIT License. See the LICENSE file for details.

