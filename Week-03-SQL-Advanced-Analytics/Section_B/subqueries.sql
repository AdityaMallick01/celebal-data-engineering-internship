/*
==========================================================
SECTION B - SUBQUERIES
Week 3 - SQL Advanced Analytics
==========================================================
*/


/*
==========================================================
Q1. Display all orders where the sales amount is
greater than the average sales.
==========================================================
*/

SELECT *
FROM orders
WHERE Sales >
(
    SELECT AVG(Sales)
    FROM orders
);

/*
Explanation:

- The subquery calculates the average sales.
- The outer query returns orders whose sales exceed
  the average sales value.
*/



/*
==========================================================
Q2. Display the order(s) with the highest sales.
==========================================================
*/

SELECT *
FROM orders
WHERE Sales =
(
    SELECT MAX(Sales)
    FROM orders
);

/*
Explanation:

- The subquery finds the maximum sales value.
- The outer query returns the corresponding order(s).
*/



/*
==========================================================
Q3. Display customers whose total sales are greater
than the average customer sales.
==========================================================
*/

SELECT
    `Customer ID`,
    `Customer Name`,
    SUM(Sales) AS total_sales
FROM superstore_raw
GROUP BY `Customer ID`, `Customer Name`
HAVING SUM(Sales) >
(
    SELECT AVG(customer_sales)
    FROM
    (
        SELECT SUM(Sales) AS customer_sales
        FROM superstore_raw
        GROUP BY `Customer ID`
    ) AS avg_sales
);

/*
Explanation:

- Inner subquery calculates sales for every customer.
- Outer subquery calculates the average customer sales.
- HAVING filters customers above that average.
*/



/*
==========================================================
Q4. Display products whose average sales are greater
than the overall average sales.
==========================================================
*/

SELECT
    `Product ID`,
    `Product Name`,
    AVG(Sales) AS average_sales
FROM superstore_raw
GROUP BY `Product ID`, `Product Name`
HAVING AVG(Sales) >
(
    SELECT AVG(Sales)
    FROM superstore_raw
);

/*
Explanation:

- Compares each product's average sales with the
  overall average sales.
*/



/*
==========================================================
Q5. Display customers who have placed more than
one order.
==========================================================
*/

SELECT
    `Customer ID`,
    `Customer Name`,
    COUNT(DISTINCT `Order ID`) AS total_orders
FROM superstore_raw
GROUP BY `Customer ID`, `Customer Name`
HAVING COUNT(DISTINCT `Order ID`) >
(
    SELECT 1
);

/*
Explanation:

- Groups data by customer.
- Returns customers having more than one unique order.
*/