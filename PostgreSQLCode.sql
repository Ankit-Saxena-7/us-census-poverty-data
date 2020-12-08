-- Database: enteraassignment

-- Check for existence of schemas
SELECT	*
FROM		information_schema.schemata;

-- Check if tables have been loaded from the Python program
SELECT	*
FROM		pg_catalog.pg_tables
WHERE		schemaname = 'data_access_layer';

-- Assign the newly loaded tables to the 'data_access_layer' schema

ALTER TABLE "tblZipCodePopulationHousing"
	SET SCHEMA data_access_layer;
ALTER TABLE "tblIncomePovertyRatioByZipTop10"
	SET SCHEMA data_access_layer;
ALTER TABLE "tblPovertyByHouseholdByEducationByZipTop10"
	SET SCHEMA data_access_layer;
ALTER TABLE "tblPovertyBySexByWorkByZipTop10"
	SET SCHEMA data_access_layer;
ALTER TABLE "tblInsuranceByIncomePovertyRatioByZipTop10"
	SET SCHEMA data_access_layer;

-- Explore the loaded data in the 'data_access_layer' schema
SELECT	*
FROM		data_access_layer."tblZipCodePopulationHousing";

SELECT	*
FROM		data_access_layer."tblIncomePovertyRatioByZipTop10"
ORDER BY income_poverty_ratio DESC;

SELECT	*
FROM		data_access_layer."tblPovertyByHouseholdByEducationByZipTop10"
ORDER BY poverty_status DESC;

SELECT	*
FROM		data_access_layer."tblPovertyBySexByWorkByZipTop10"
ORDER BY poverty_status DESC;

SELECT	*
FROM		data_access_layer."tblInsuranceByIncomePovertyRatioByZipTop10"
ORDER BY insurance_income_poverty_ratio DESC;

DROP TABLE data_analysis_layer_relational.tblZipCodeMetaData;

-- Create a relational data set in the 'data_analysis_layer_relational' schema
CREATE TABLE IF NOT EXISTS data_analysis_layer_relational.tblZipCodeMetaData
(
zip_code														TEXT,
population													BIGINT,
housing_units												BIGINT,
poverty_household_education					FLOAT8,
poverty_household_education_rank		FLOAT8,
insurance_income_poverty_ratio			FLOAT8,
insurance_income_poverty_ratio_rank	FLOAT8,
poverty_sex_work										FLOAT8,
poverty_sex_work_rank								FLOAT8,
income_poverty_ratio								FLOAT8,
income_poverty_ratio_rank						FLOAT8
);

DELETE
FROM		data_analysis_layer_relational.tblZipCodeMetaData;

-- Insert values from the 'data_access_layer' into the relational schema 'data_analysis_layer_relational'
INSERT INTO	data_analysis_layer_relational.tblZipCodeMetaData
(
SELECT	tbl1.zip_code AS zip_code,
				tbl1.population AS population,
				tbl1.housing_units AS housing_units,
				tbl2.poverty_status AS poverty_household_education,
				CASE
					WHEN tbl2.poverty_status IS NOT NULL THEN
					DENSE_RANK() OVER(ORDER BY tbl2.poverty_status ASC)
					ELSE NULL
				END AS poverty_household_education_rank,
				tbl3.insurance_income_poverty_ratio	AS insurance_income_poverty_ratio,
				CASE
					WHEN tbl3.insurance_income_poverty_ratio IS NOT NULL THEN
					DENSE_RANK() OVER(ORDER BY tbl3.insurance_income_poverty_ratio ASC)
					ELSE NULL
				END AS insurance_income_poverty_ratio_rank,
				tbl4.poverty_status AS poverty_sex_work,
				CASE
					WHEN tbl4.poverty_status IS NOT NULL THEN
					DENSE_RANK() OVER(ORDER BY tbl4.poverty_status ASC)
					ELSE NULL
				END	 AS poverty_sex_work_rank,
				tbl5.income_poverty_ratio AS income_poverty_ratio,
				CASE
					WHEN tbl5.income_poverty_ratio IS NOT NULL THEN
					DENSE_RANK() OVER(ORDER BY tbl5.income_poverty_ratio ASC)
					ELSE NULL
				END AS income_poverty_ratio_rank
FROM		data_access_layer."tblZipCodePopulationHousing" AS tbl1
LEFT JOIN	data_access_layer."tblPovertyByHouseholdByEducationByZipTop10" AS tbl2
ON			tbl1.zip_code = tbl2.zip_code
LEFT JOIN	data_access_layer."tblInsuranceByIncomePovertyRatioByZipTop10" AS tbl3
ON			tbl1.zip_code = tbl3.zip_code
LEFT JOIN	data_access_layer."tblPovertyBySexByWorkByZipTop10" AS tbl4
ON			tbl1.zip_code = tbl4.zip_code
LEFT JOIN	data_access_layer."tblIncomePovertyRatioByZipTop10" AS tbl5
ON			tbl1.zip_code = tbl5.zip_code
);

-- Check if insert was performed correctly (33120 rows need to be inserted)
SELECT	COUNT(*)
FROM		data_analysis_layer_relational.tblZipCodeMetaData;

SELECT	*
FROM		data_analysis_layer_relational.tblZipCodeMetaData
LIMIT		10;
