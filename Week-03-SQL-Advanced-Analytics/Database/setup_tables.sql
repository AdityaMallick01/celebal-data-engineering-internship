USE week3_sql_advanced;

/*
==========================================================
Create the staging table: superstore_raw
==========================================================
*/

CREATE TABLE superstore_raw AS
SELECT *
FROM superstore_analysis.superstore;