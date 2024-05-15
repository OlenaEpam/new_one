This project contains tests to run for TRN database
To run tests:

Set up the TRN database locally
Install Microsoft ODBC driver for SQL
Install pyodbc package via pip3 install pyodbc
Clone the project from repository to your local machine
Write credentials of the user - USERNAME and PASSWORD in credentials.py file
Run tests: pip install pytest, pip install sqlalchemy, type 'pytest' in console
To generate report: pip install pytest-html, type pytest --html=report.html