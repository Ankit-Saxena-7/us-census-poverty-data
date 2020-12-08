### US CENSUS POVERTY DATA

__Summary__:
Extracting data from the US Census website and storing the data in a PostgreSQL database

__How to execute the files__:
* Run the Python code in the file _Solution.py_
* Follow the instructions in the comments
  * Copies of the Python data frames will be downloaded as Excel files for reference
  * The _Data_ folder contains these Excel files
* Connect to a local PostgreSQL database using the commands in the _Solution.py_ Python file
* Once connected, and all the commands in the _Solution.py_ file have been performed, execute the SQL commands in the _PostgreSQLCode.sql_ file in a PostgreSQL admin platform. I used pgAdmin from this [link](https://www.pgadmin.org/)
* The PDF _Database ERD.pdf_ contains an entity–relationship diagram for the SQL schemas

__Details on the SQL database__:
* The database name is _enteraassessment_
* The database has two schemas: _data_access_layer_ and _data_analysis_layer_relational_
 * _data_access_layer_ has all the data fetched from the Python script and is an intermediate platform
 * _data_analysis_layer_relational_ has reorganized data in a relational format for analysis
 
__Final SQL data set for analysis__:
* The table _tblZipCodeMetaData_ in the _data_analysis_layer_relational_ schema contains the final data for analysis
* The _zip_code_ column is the Primary Index
* The columns suffixed with _rank_ represent poverty-related rankings based on different breakdowns

__Which tables from the US Census were slelected and why?__<br/>
For this analysis, I have used ACS 5-year data from 2017.
The ACS covers a broad range of topics about social, economic, demographic, and housing characteristics of the U.S. population.
The 5-year estimates from the ACS are "period" estimates that represent data collected over a period of time. 
The primary advantage of using multiyear estimates is the increased statistical reliability of the data for less populated areas and small population subgroups.
ACS 5-year data contains data at the zip code level which is why that is the data source of choice.

__Within the ACS5 data set, the following tables were extracted__:
* Poverty status in the past 12 months of families by household type by educational attainment of householder (by zip code)
  * JUSTIFICATION: Research has consistently shown a relationship between education level and poverty
  * SOURCE: Van der Berg, S. (2008). Poverty and education. Education policy series, 10, 28.
  * Table code: B17018
* Poverty status in the past 12 months of individuals by sex by work experience (by zip code)
  * JUSTIFICATION: Work experience is directly correlated with income which determines poverty
  * SOURCE: Sen, A. (2006). Conceptualizing and measuring poverty. Poverty and inequality, 30-46.
  * Table code: B17004
* Health insurance coverage status by ratio of income to poverty level in the past 12 months by age (by zip code)
  * JUSTIFICATION: Smart insurance investments have shown to alleviate the harmful effects of poverty
  * SOURCE: Hamid, S. A., Roberts, J., & Mosley, P. (2011). Can micro health insurance reduce poverty? Evidence from Bangladesh. Journal of risk and Insurance, 78(1), 57-82.
  * Table code: C27016
* Ratio of income to poverty level in the past 12 months by nativity of children under 18 years in families and subfamilies by living arrangements and nativity of parents (by zip code)
  * JUSTIFICATION: Income and poverty are closely relarted and hence their ratio is a relevant indicator of poverty-levels
  * SOURCE: Semega, J. L., Fontenot, K. R., & Kollar, M. A. (2017). Income and poverty in the United States: 2016. Current Population Reports, (P60-259).
  * Table code: B05010
