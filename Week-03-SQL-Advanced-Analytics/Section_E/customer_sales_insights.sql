/*
==========================================================
SECTION E - CUSTOMER SALES INSIGHTS
Week 3 - SQL Advanced Analytics
==========================================================
*/


/*
==========================================================
Q1. Display the Top 5 customers based on total sales.
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
    total_sales
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 5;

/*
Explanation:

- Calculates total sales for each customer.
- Displays the top 5 customers based on sales.
*/



/*
==========================================================
Q2. Display the Bottom 5 customers based on total sales.
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
    total_sales
FROM customer_sales
ORDER BY total_sales
LIMIT 5;

/*
Explanation:

- Displays the customers with the lowest total sales.
*/



/*
==========================================================
Q3. Display customers who have placed only one order.
==========================================================
*/

SELECT
    `Customer ID`,
    `Customer Name`,
    COUNT(DISTINCT `Order ID`) AS total_orders
FROM superstore_raw
GROUP BY `Customer ID`, `Customer Name`
HAVING COUNT(DISTINCT `Order ID`) = 1;

/*
Explanation:

- Finds customers who have placed exactly one order.
*/



/*
==========================================================
Q4. Display customers whose total sales are above
the average customer sales.
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
    total_sales
FROM customer_sales
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

/*
Explanation:

- Compares each customer's total sales with the
  average customer sales.
*/



/*
==========================================================
Q5. Final Combined Query
(Customer Name, Total Sales, Rank)
Using JOIN + CTE + Window Function.
==========================================================
*/

WITH customer_sales AS
(
    SELECT
        `Customer ID`,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY `Customer ID`
)

SELECT
    c.`Customer Name`,
    cs.total_sales,
    RANK() OVER (ORDER BY cs.total_sales DESC) AS rnk
FROM customers c
INNER JOIN customer_sales cs
ON c.`Customer ID` = cs.`Customer ID`
ORDER BY rnk;

/*
Explanation:

- The CTE calculates total sales for each customer.
- INNER JOIN combines customer details with sales.
- RANK() assigns rankings based on total sales.
- Produces the final customer sales report.
*/