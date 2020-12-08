"""
Naming conventions:
- Variables are prefixed with 'v'
- Parameters are prefixed with 'p'
- Tables are prefixed with 'df'
- Lists are prefixed with 'lst'
- Arrays are prefixed with 'arr'
- Functions are prefixed with 'func'
- CamelCase is used for naming entities
"""

"""
Terminal commands:
pip install census
pip install us
pip install openpyxl
"""

"""
JUSTIFICATION:
For this analysis, I have used ACS 5-year data from 2017.
The ACS covers a broad range of topics about social, economic, demographic, and housing characteristics of the U.S. population.
The 5-year estimates from the ACS are "period" estimates that represent data collected over a period of time. 
The primary advantage of using multiyear estimates is the increased statistical reliability of the data for less populated areas and small population subgroups.
ACS 5-year data contains data at the zip code level which is why that is the data source of choice.
"""

# Import libraries
from census import Census # For using the US Census API
import pandas as pd # For performing data analyses
import psycopg2  as pg # To connect with PostgreSQL
from sqlalchemy import  create_engine # To perform SQL operations

# FUNCTION DEFINITIONS

# Function to print descriptions of tables in ACS5 containing a specified keyword
def funcPrintACS5TableList(pKeyword, pAPIKey):

    # Fetch list of tables using the API key
    vACS5Tables = pAPIKey.acs5.tables()

    # Loop through the list of descriptions and only print unique descriptions
    for vIndex in range(len(vACS5Tables)):
        if (pKeyword.upper() in vACS5Tables[vIndex]['description']):
            print(vACS5Tables[vIndex]['name'] + " | " + vACS5Tables[vIndex]['description'])

# Function to fetch a data for all zip codes from US Census Bureau using the table name
def funcDownloadCensusACS5Data(pTableName, pAPIKey, pColumnNames):

    # Fetch the data from US Census Bureau using the table name
    lstData = pAPIKey.acs5.get(('NAME,group(' + pTableName + ')'), {'for': 'zip code tabulation area:*'})

    # Convert to data frame
    dfData = pd.DataFrame(lstData)

    # Keep only the zip code and the poverty estimate columns
    dfData = dfData[[pTableName + '_001E', 'zip code tabulation area']]

    dfData.columns = pColumnNames

    # Download to Excel
    dfData.to_excel('ACS5_' + pTableName + '.xlsx')

    return dfData

# Execute an SQL query on PostgreSQL
def funcExecuteQueryPostgreSQL(pQuery, pHost, pDatabase, pUser, pPassword):
    # Connect to the database
    vConnection = pg.connect(
        host = pHost,
        database = pDatabase,
        user = pUser,
        password = pPassword
    )

    # Create cursor
    vCursor = vConnection.cursor()

    # Execute a query
    vCursor.execute(pQuery)
    vRows = vCursor.fetchall()

    for vRow in vRows:
        print(vRow[0])

    # Commit changes (not needed for selection queries)
    vConnection.commit()

    # Close the cursor
    vCursor.close()

    # Close the connection after session
    vConnection.close()

# Store data in PostgreSQL database
def funcStoreDataPostgreSQL(pDataFrame, pSQLTableName, pHost, pDatabase, pUser, pPassword, pPort):
    vConnectionEngine = create_engine('postgresql://' + pUser + ':' + pPassword + '@' + pHost + ':' + pPort + '/' + pDatabase)
    pDataFrame.to_sql(pSQLTableName, vConnectionEngine)

# FETCHING DATA FROM US CENSUS

# Fetching Census API key
vAPIKey = Census("cf884e1ae8f96df20de94e59eeee27b0eb25ef6b")

# List down all the poverty-related data available and get all the table names (ACS5 2017)
funcPrintACS5TableList('poverty', vAPIKey)

# Download relevant tables using the API

# Total population (by zip code)
dfB01003 = funcDownloadCensusACS5Data('B01003', vAPIKey, ['population', 'zip_code'])

# Unweighted sample housing units (by zip code)
dfB00002 = funcDownloadCensusACS5Data('B00002', vAPIKey, ['housing_units', 'zip_code'])

# Poverty status in the past 12 months of families by household type by educational attainment of householder (by zip code)
# JUSTIFICATION: Research has consistently shown a relationship between education level and poverty
# SOURCE: Van der Berg, S. (2008). Poverty and education. Education policy series, 10, 28.
dfB17018 = funcDownloadCensusACS5Data('B17018', vAPIKey, ['poverty_status', 'zip_code'])

# Poverty status in the past 12 months of individuals by sex by work experience (by zip code)
# JUSTIFICATION: Work experience is directly correlated with income which determines poverty
# SOURCE: Sen, A. (2006). Conceptualizing and measuring poverty. Poverty and inequality, 30-46.
dfB17004 = funcDownloadCensusACS5Data('B17004', vAPIKey, ['poverty_status', 'zip_code'])

# Health insurance coverage status by ratio of income to poverty level in the past 12 months by age (by zip code)
# JUSTIFICATION: Smart insurance investments have shown to alleviate the harmful effects of poverty
# SOURCE: Hamid, S. A., Roberts, J., & Mosley, P. (2011). Can micro health insurance reduce poverty? Evidence from Bangladesh. Journal of risk and Insurance, 78(1), 57-82.
dfC27016 = funcDownloadCensusACS5Data('C27016', vAPIKey, ['insurance_income_poverty_ratio', 'zip_code'])

# Ratio of income to poverty level in the past 12 months by nativity of children under 18 years in families and subfamilies by living arrangements and nativity of parents (by zip code)
# JUSTIFICATION: Income and poverty are closely relarted and hence their ratio is a relevant indicator of poverty-levels
# SOURCE: Semega, J. L., Fontenot, K. R., & Kollar, M. A. (2017). Income and poverty in the United States: 2016. Current Population Reports, (P60-259).
dfB05010 = funcDownloadCensusACS5Data('B05010', vAPIKey, ['income_poverty_ratio', 'zip_code'])

# DATA PROCESSING

# Master zip code table

# Tables 'dfB01003' and 'dfB00002' will be combined and will be used as the master table for all zip codes in the US
dfZipCodePopulationHousing = dfB01003.merge(dfB00002, on='zip_code', how='left', indicator=True)

# Drop the last column that indicates if there are any missing zip codes from either table
dfZipCodePopulationHousing.drop(['_merge'], axis=1, inplace=True)

# Fill missing values with the average of the column
dfZipCodePopulationHousing['population'] = dfZipCodePopulationHousing['population'].fillna(dfZipCodePopulationHousing['population'].mean())
dfZipCodePopulationHousing['housing_units'] = dfZipCodePopulationHousing['housing_units'].fillna(dfZipCodePopulationHousing['housing_units'].mean())

# Change population and housing units to integer for better processing and memory
dfZipCodePopulationHousing = dfZipCodePopulationHousing.astype({"population": int, "housing_units": int})
dfZipCodePopulationHousing = dfZipCodePopulationHousing.astype({"zip_code": str})

# Check if zip codes are unique or not
print(dfZipCodePopulationHousing['zip_code'].value_counts())
print(dfZipCodePopulationHousing.head(3))

dfZipCodePopulationHousing.set_index('zip_code', inplace=True)

# Poverty tables based on various groupings

# Instead of top 10 zip codes, I have selected top 10 poverty values which has a lower chance of losing valuable data

# Smaller values indicate higher poverty levels
dfPovertyByHouseholdByEducationByZipTop10 = dfB17018.nsmallest(10, ['poverty_status'], keep='all')
dfPovertyByHouseholdByEducationByZipTop10.set_index('zip_code', inplace=True)

dfPovertyBySexByWorkByZipTop10 = dfB17004.nsmallest(10, ['poverty_status'], keep='all')
dfPovertyBySexByWorkByZipTop10.set_index('zip_code', inplace=True)

dfIncomePovertyRatioByZipTop10 = dfB05010.nsmallest(10, ['income_poverty_ratio'], keep='all')
dfIncomePovertyRatioByZipTop10.set_index('zip_code', inplace=True)

# Larger values indicate higher poverty levels
dfInsuranceByIncomePovertyRatioByZipTop10 = dfC27016.nlargest(10, ['insurance_income_poverty_ratio'], keep='all')
dfInsuranceByIncomePovertyRatioByZipTop10.set_index('zip_code', inplace=True)

# LOADING DATA TO POSTGRESQL

"""
POSTGRESQL COMMANDS:
- CREATE DATABASE enteraassessment;
- CREATE SCHEMA data_access_layer;
- CREATE SCHEMA data_analysis_layer_relational
"""

vHost = 'localhost'
vDatabase = 'enteraassessment'
vUser = 'postgres'
vPassword = 'supersecure'
vPort = '5432'

# Store dataframes into PostgreSQL
funcStoreDataPostgreSQL(dfZipCodePopulationHousing, 'tblZipCodePopulationHousing', vHost, vDatabase, vUser, vPassword, vPort)
funcStoreDataPostgreSQL(dfPovertyByHouseholdByEducationByZipTop10, 'tblPovertyByHouseholdByEducationByZipTop10', vHost, vDatabase, vUser, vPassword, vPort)
funcStoreDataPostgreSQL(dfPovertyBySexByWorkByZipTop10, 'tblPovertyBySexByWorkByZipTop10', vHost, vDatabase, vUser, vPassword, vPort)
funcStoreDataPostgreSQL(dfInsuranceByIncomePovertyRatioByZipTop10, 'tblInsuranceByIncomePovertyRatioByZipTop10', vHost, vDatabase, vUser, vPassword, vPort)
funcStoreDataPostgreSQL(dfIncomePovertyRatioByZipTop10, 'tblIncomePovertyRatioByZipTop10', vHost, vDatabase, vUser, vPassword, vPort)

"""
POSTGRESQL COMMANDS:
- Execute the SQL commands in the file 'PostgreSQLCode.sql'
"""

"""
RESOURCES -
- Downloading zip code-wise data: https://www2.census.gov/data/api-documentation/how-to-download-all-zip-code-tabulation-areas-from-the-census-api.pdf
- ACS5 data sets: https://api.census.gov/data/2017/acs/acs5/variables.html
- GitHub repository for US Census API: https://github.com/datamade/census
"""




