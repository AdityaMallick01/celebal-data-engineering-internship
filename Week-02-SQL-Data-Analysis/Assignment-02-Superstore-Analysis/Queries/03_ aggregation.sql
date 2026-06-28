/*
==========================================================
MODULE 3 - AGGREGATION
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Calculate the total sales.
==========================================================
*/

SELECT
    SUM(Sales) AS total_sales
FROM superstore;

/*
Explanation:

- SUM() calculates the total sales of all orders.
*/



/*
==========================================================
Q2. Calculate the total profit.
==========================================================
*/

SELECT
    SUM(Profit) AS total_profit
FROM superstore;

/*
Explanation:

- SUM() adds all profit values.
- Gives the overall profit earned.
*/



/*
==========================================================
Q3. Calculate the average sales per order.
==========================================================
*/

SELECT
    AVG(Sales) AS average_sales
FROM superstore;

/*
Explanation:

- AVG() calculates the average sales amount.
*/



/*
==========================================================
Q4. Count the total number of orders.
==========================================================
*/

SELECT
    COUNT(*) AS total_orders
FROM superstore;

/*
Explanation:

- COUNT(*) returns the total number of records.
*/



/*
==========================================================
Q5. Display total sales for each category.
==========================================================
*/

SELECT
    Category,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY Category;

/*
Explanation:

- GROUP BY groups rows by Category.
- SUM() calculates total sales for each category.
*/



/*
==========================================================
Q6. Display average profit for each region.
==========================================================
*/

SELECT
    Region,
    AVG(Profit) AS average_profit
FROM superstore
GROUP BY Region;

/*
Explanation:

- Groups records by Region.
- AVG() calculates the average profit.
*/



/*
==========================================================
Q7. Display total quantity sold for each sub-category.
==========================================================
*/

SELECT
    `Sub-Category`,
    SUM(Quantity) AS total_quantity
FROM superstore
GROUP BY `Sub-Category`;

/*
Explanation:

- Calculates total quantity sold for each sub-category.
*/



/*
==========================================================
Q8. Display the number of orders in each segment.
==========================================================
*/

SELECT
    Segment,
    COUNT(*) AS total_orders
FROM superstore
GROUP BY Segment;

/*
Explanation:

- Counts orders for each customer segment.
*/



/*
==========================================================
Q9. Display categories where total sales exceed 500000.
==========================================================
*/

SELECT
    Category,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY Category
HAVING SUM(Sales) > 500000;

/*
Explanation:

- HAVING filters grouped results.
- Returns only categories whose sales exceed 500000.
*/



/*
==========================================================
Q10. Display regions where average profit is greater than 25.
==========================================================
*/

SELECT
    Region,
    AVG(Profit) AS average_profit
FROM superstore
GROUP BY Region
HAVING AVG(Profit) > 25;

/*
Explanation:

- HAVING filters aggregated results.
- Returns only regions with average profit greater than 25.
*/