/*
==========================================================
SECTION C - COMMON TABLE EXPRESSIONS (CTEs)
Week 3 - SQL Advanced Analytics
==========================================================
*/


/*
==========================================================
Q1. Calculate the total sales for each customer.
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

SELECT *
FROM customer_sales;

/*
Explanation:

- The CTE calculates the total sales for each customer.
- The main query displays the result.
*/



/*
==========================================================
Q2. Display customers whose total sales exceed 5000.
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

SELECT *
FROM customer_sales
WHERE total_sales > 5000;

/*
Explanation:

- The CTE computes customer sales.
- The main query filters customers with sales above 5000.
*/



/*
==========================================================
Q3. Display the average sales for each region.
==========================================================
*/

WITH region_sales AS
(
    SELECT
        Region,
        AVG(Sales) AS average_sales
    FROM superstore_raw
    GROUP BY Region
)

SELECT *
FROM region_sales;

/*
Explanation:

- The CTE calculates the average sales for each region.
- The main query displays the aggregated results.
*/



/*
==========================================================
Q4. Display the total profit for each category.
==========================================================
*/

WITH category_profit AS
(
    SELECT
        Category,
        SUM(Profit) AS total_profit
    FROM superstore_raw
    GROUP BY Category
)

SELECT *
FROM category_profit;

/*
Explanation:

- The CTE calculates the total profit for each category.
- The main query displays category-wise profit.
*/



/*
==========================================================
Q5. Display customers whose total sales are greater
than the average customer sales.
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

SELECT *
FROM customer_sales
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

/*
Explanation:

- The CTE calculates total sales for each customer.
- The subquery computes the average customer sales.
- The main query returns customers above the average.
*/