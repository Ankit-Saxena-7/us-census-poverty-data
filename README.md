# US CENSUS POVERTY DATA

Summary:
Extracting data from the US Census website and storing the data in a PostgreSQL database

How to execute the files:
* Run the Python code in the file _Solution.py_
* Follow the instructions in the comments
  * Copies of the Python data frames will be downloaded as Excel files for reference
  * The _Data_ folder contains these Excel files
* Connect to a local PostgreSQL database using the commands in the _Solution.py_ Python file
* Once connected, and all the commands in the _Solution.py_ file have been performed, execute the SQL commands in the _PostgreSQLCode.sql_ file in a PostgreSQL admin platform. I used pgAdmin from this [link](https://www.pgadmin.org/)
* The PDF _Database ERD.pdf_ contains an entity–relationship diagram for the SQL schemas

Details on the SQL database:
* The database name is _enteraassessment_
* The database has two schemas: _data_access_layer_ and _data_analysis_layer_relational_
 * _data_access_layer_ has all the data fetched from the Python script and is an intermediate platform
 * _data_analysis_layer_relational_ has reorganized data in a relational format for analysis
 
Final SQL data set for analysis:
* The table _tblZipCodeMetaData_ in the _data_analysis_layer_relational_ schema contains the final data for analysis
* The _zip_code_ column is the Primary Index
* The columns suffixed with _rank_ represent poverty-related rankings based on different breakdowns
