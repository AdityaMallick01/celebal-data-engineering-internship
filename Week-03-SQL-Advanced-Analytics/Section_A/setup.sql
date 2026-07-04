/*
==========================================================
SECTION A - SETUP
Week 3 - SQL Advanced Analytics
==========================================================
*/


/*
==========================================================
Q1. Create the customers table using DISTINCT records
from the superstore_raw table.
==========================================================
*/

CREATE TABLE customers AS
SELECT DISTINCT
    `Customer ID`,
    `Customer Name`,
    Segment,
    Country,
    City,
    State,
    `Postal Code`,
    Region
FROM superstore_raw;

/*
Explanation:

- SELECT DISTINCT removes duplicate customer records.
- Each customer appears only once in the customers table.
*/

SELECT COUNT(*) AS total_customers
FROM customers;



/*
==========================================================
Q2. Create the products table using DISTINCT records
from the superstore_raw table.
==========================================================
*/

CREATE TABLE products AS
SELECT DISTINCT
    `Product ID`,
    Category,
    `Sub-Category`,
    `Product Name`
FROM superstore_raw;

/*
Explanation:

- Stores unique product information.
- Eliminates duplicate product records.
*/

SELECT COUNT(*) AS total_products
FROM products;



/*
==========================================================
Q3. Create the orders table using DISTINCT records
from the superstore_raw table.
==========================================================
*/

CREATE TABLE orders AS
SELECT DISTINCT
    `Order ID`,
    `Order Date`,
    `Ship Date`,
    `Ship Mode`,
    `Customer ID`,
    Sales,
    Quantity,
    Discount,
    Profit
FROM superstore_raw;

/*
Explanation:

- Stores order-level information.
- DISTINCT removes duplicate rows.
*/

SELECT COUNT(*) AS total_orders
FROM orders;



/*
==========================================================
Q4. Verify that all required tables have been created.
==========================================================
*/

SHOW TABLES;

/*
Explanation:

- Displays all tables available in the database.
- Confirms successful creation of all required tables.
*/



/*
==========================================================
Q5. Display the first five records from each table.
==========================================================
*/

SELECT *
FROM customers
LIMIT 5;

SELECT *
FROM products
LIMIT 5;

SELECT *
FROM orders
LIMIT 5;

/*
Explanation:

- Displays sample records from each table.
- Confirms that the data has been populated correctly.
*/