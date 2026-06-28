/*
==========================================================
MODULE 5 - BUSINESS QUERIES
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Display monthly sales trends.
==========================================================
*/

SELECT
    DATE_FORMAT(STR_TO_DATE(`Order Date`, '%m/%d/%Y'), '%Y-%m') AS month,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY month
ORDER BY month;

/*
Explanation:

- Groups sales by month.
- Helps analyze monthly sales trends.
*/



/*
==========================================================
Q2. Display the top 5 customers based on total sales.
==========================================================
*/

SELECT
    `Customer Name`,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY `Customer Name`
ORDER BY total_sales DESC
LIMIT 5;

/*
Explanation:

- Identifies customers contributing the highest sales.
*/



/*
==========================================================
Q3. Display the top 5 products based on total sales.
==========================================================
*/

SELECT
    `Product Name`,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY `Product Name`
ORDER BY total_sales DESC
LIMIT 5;

/*
Explanation:

- Finds the best-selling products.
*/



/*
==========================================================
Q4. Display total sales and profit for each region.
==========================================================
*/

SELECT
    Region,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Region
ORDER BY total_sales DESC;

/*
Explanation:

- Compares sales and profit across regions.
*/



/*
==========================================================
Q5. Display the most profitable product category.
==========================================================
*/

SELECT
    Category,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Category
ORDER BY total_profit DESC;

/*
Explanation:

- Identifies the category generating the highest profit.
*/