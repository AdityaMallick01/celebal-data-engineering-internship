/*
==========================================================
MODULE 1 - SCHEMA EXPLORATION
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Display all records from the Superstore table.
==========================================================
*/

SELECT *
FROM superstore;

/*
Explanation:

- Displays every column and every record.
- Used to understand the complete dataset.
*/



/*
==========================================================
Q2. Display the first 10 records.
==========================================================
*/

SELECT *
FROM superstore
LIMIT 10;

/*
Explanation:

- LIMIT restricts the output.
- Helps quickly inspect sample records.
*/



/*
==========================================================
Q3. Count the total number of records.
==========================================================
*/

SELECT COUNT(*) AS total_records
FROM superstore;

/*
Explanation:

- COUNT(*) returns the total number of rows.
*/



/*
==========================================================
Q4. Display the table structure.
==========================================================
*/

DESCRIBE superstore;

/*
Explanation:

- Shows every column along with its data type.
*/



/*
==========================================================
Q5. Display all unique product categories.
==========================================================
*/

SELECT DISTINCT Category
FROM superstore;

/*
Explanation:

- DISTINCT removes duplicate values.
- Shows all available product categories.
*/



/*
==========================================================
Q6. Display all unique regions.
==========================================================
*/

SELECT DISTINCT Region
FROM superstore;

/*
Explanation:

- Lists all sales regions present in the dataset.
*/



/*
==========================================================
Q7. Display all unique customer segments.
==========================================================
*/

SELECT DISTINCT Segment
FROM superstore;

/*
Explanation:

- Shows different customer segments.
*/



/*
==========================================================
Q8. Display all available shipping modes.
==========================================================
*/

SELECT DISTINCT `Ship Mode`
FROM superstore;

/*
Explanation:

- Lists all shipping methods used.
*/



/*
==========================================================
Q9. Find the earliest and latest order dates.
==========================================================
*/

SELECT
    MIN(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) AS earliest_order,
    MAX(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) AS latest_order
FROM superstore;

/*
Explanation:

- STR_TO_DATE converts text into DATE format.
- MIN() returns the earliest order.
- MAX() returns the latest order.
*/



/*
==========================================================
Q10. Count the total number of unique customers.
==========================================================
*/

SELECT COUNT(DISTINCT `Customer ID`) AS unique_customers
FROM superstore;

/*
Explanation:

- Counts distinct customers instead of total orders.
*/