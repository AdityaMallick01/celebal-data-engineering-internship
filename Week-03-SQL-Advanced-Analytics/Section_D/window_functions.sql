/*
==========================================================
SECTION D - WINDOW FUNCTIONS
Week 3 - SQL Advanced Analytics
==========================================================
*/


/*
==========================================================
Q1. Assign a unique row number to each customer
based on total sales.
==========================================================
*/

WITH customer_sales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)

SELECT
    ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS row_number,
    `Customer ID`,
    `Customer Name`,
    total_sales
FROM customer_sales;

/*
Explanation:

- ROW_NUMBER() assigns a unique sequential number.
- No two customers receive the same row number.
*/



/*
==========================================================
Q2. Rank customers based on total sales using RANK().
==========================================================
*/

WITH customer_sales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)

SELECT
    RANK() OVER (ORDER BY total_sales DESC) AS customer_rank,
    `Customer ID`,
    `Customer Name`,
    total_sales
FROM customer_sales;

/*
Explanation:

- RANK() assigns the same rank to tied values.
- The next rank is skipped after a tie.
*/



/*
==========================================================
Q3. Rank customers based on total sales using
DENSE_RANK().
==========================================================
*/

WITH customer_sales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)

SELECT
    DENSE_RANK() OVER (ORDER BY total_sales DESC) AS dense_rank,
    `Customer ID`,
    `Customer Name`,
    total_sales
FROM customer_sales;

/*
Explanation:

- DENSE_RANK() assigns the same rank to tied values.
- No ranks are skipped after a tie.
*/



/*
==========================================================
Q4. Display the highest sales order for each customer
using ROW_NUMBER().
==========================================================
*/

WITH ranked_orders AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        `Order ID`,
        Sales,
        ROW_NUMBER() OVER
        (
            PARTITION BY `Customer ID`
            ORDER BY Sales DESC
        ) AS row_num
    FROM superstore_raw
)

SELECT
    `Customer ID`,
    `Customer Name`,
    `Order ID`,
    Sales
FROM ranked_orders
WHERE row_num = 1;

/*
Explanation:

- PARTITION BY groups records customer-wise.
- ROW_NUMBER() identifies the highest sales order
  for each customer.
*/



/*
==========================================================
Q5. Display customer sales ranking by combining
CTE and RANK().
==========================================================
*/

WITH customer_sales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS total_sales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)

SELECT
    `Customer ID`,
    `Customer Name`,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales;

/*
Explanation:

- Combines a CTE with the RANK() window function.
- Produces customer sales rankings from highest to lowest.
*/