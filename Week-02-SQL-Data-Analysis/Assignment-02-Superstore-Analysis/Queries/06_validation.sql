/*
==========================================================
MODULE 6 - DATA VALIDATION
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Count the total number of records.
==========================================================
*/

SELECT COUNT(*) AS total_records
FROM superstore;

/*
Explanation:

- Verifies the total number of imported records.
*/



/*
==========================================================
Q2. Check for NULL values in Sales.
==========================================================
*/

SELECT COUNT(*) AS null_sales
FROM superstore
WHERE Sales IS NULL;

/*
Explanation:

- Checks whether the Sales column contains NULL values.
*/



/*
==========================================================
Q3. Find duplicate Order IDs.
==========================================================
*/

SELECT
    `Order ID`,
    COUNT(*) AS occurrences
FROM superstore
GROUP BY `Order ID`
HAVING COUNT(*) > 1;

/*
Explanation:

- Identifies Order IDs that appear multiple times.
- Multiple rows are expected because one order can contain multiple products.
*/



/*
==========================================================
Q4. Find records with negative profit.
==========================================================
*/

SELECT *
FROM superstore
WHERE Profit < 0;

/*
Explanation:

- Identifies orders that resulted in a loss.
*/



/*
==========================================================
Q5. Check for missing Postal Codes.
==========================================================
*/

SELECT COUNT(*) AS missing_postal_codes
FROM superstore
WHERE `Postal Code` IS NULL;

/*
Explanation:

- Checks whether any postal codes are missing.
*/