# Simple Salesforce Report

The Salesforce Report Package is a Python library that provides functionality to interact with Salesforce reports using the [Simple Salesforce](https://github.com/simple-salesforce/simple-salesforce).

## Overview
This package enables you to retrieve Salesforce reports and convert them into pandas DataFrames for further analysis and processing within your Python environment. It simplifies the process of fetching Salesforce report data and makes it easy to work with in data analysis workflows.

### Note
This only works for salesforce report that do **NOT** have <ins>**GROUPED ROWS**</ins> or <ins>**GROUPED COLUMNS**</ins>.

## Installation
To install the package, you can use pip:
```
pip install git+https://github.com/weiweikee/simple_salesforce_report
```

## Usage
To use this package

1. First import the Salesforce_Report object.

```
from simple_salesforce_report import Salesforce_Report
```
2. Providing an environment file containing Salesforce credentials and company information.
```
sf_report = Salesforce_Report(env_filepath)
```

3. Then, you can retrieve reports and convert them into pandas DataFrames.
```
df = sf_report.get_simple_report(report_id)
```
## Example Env
```env
[DEFAULT]
SALESFORCE_USERNAME=john.smith@gmail.com
SALESFORCE_PASSWORD=password
SALESFORCE_SECURITY_TOKEN=token
# This is the Salesforce Domain
COMPANY_NAME=bcpi
```

## Dependencies
- simple_salesforce: A Python library for interacting with Salesforce APIs.
- pandas: A powerful data manipulation library in Python.

## License
This package is licensed under the MIT License. See the LICENSE file for details.