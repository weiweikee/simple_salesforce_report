"""Simple_Salesforce_Report Package Setup"""
from setuptools import setup, find_packages

setup(
    name='simple_salesforce_report',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'simple_salesforce',
        'pandas',
    ],
    author='Wei-Wei Chi',
    author_email='weiweikee@gmail.com',
    description='Interface to create Pandas Dataframe from Salesforce Report',
    url='https://github.com/weiweikee/simple_salesforce_report',
    classifiers=[  # Classifiers help categorize your package for PyPI
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
