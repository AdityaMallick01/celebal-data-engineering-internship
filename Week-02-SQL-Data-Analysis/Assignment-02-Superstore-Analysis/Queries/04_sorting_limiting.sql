/*
==========================================================
MODULE 4 - SORTING & LIMITING
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Display the top 10 highest sales orders.
==========================================================
*/

SELECT *
FROM superstore
ORDER BY Sales DESC
LIMIT 10;

/*
Explanation:

- ORDER BY Sales DESC sorts the records from highest to lowest sales.
- LIMIT 10 displays only the top 10 records.
*/



/*
==========================================================
Q2. Display the top 10 most profitable orders.
==========================================================
*/

SELECT *
FROM superstore
ORDER BY Profit DESC
LIMIT 10;

/*
Explanation:

- Orders are sorted based on Profit in descending order.
- LIMIT returns the top 10 profitable orders.
*/



/*
==========================================================
Q3. Display the top 10 customers based on total sales.
==========================================================
*/

SELECT
    `Customer Name`,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY `Customer Name`
ORDER BY total_sales DESC
LIMIT 10;

/*
Explanation:

- Calculates total sales for each customer.
- Results are sorted in descending order.
- Displays only the top 10 customers.
*/



/*
==========================================================
Q4. Display the top 10 products based on total sales.
==========================================================
*/

SELECT
    `Product Name`,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY `Product Name`
ORDER BY total_sales DESC
LIMIT 10;

/*
Explanation:

- Groups records by Product Name.
- Calculates total sales for each product.
- Displays the top 10 selling products.
*/



/*
==========================================================
Q5. Display the top 5 states with the highest sales.
==========================================================
*/

SELECT
    State,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY State
ORDER BY total_sales DESC
LIMIT 5;

/*
Explanation:

- Calculates total sales for each state.
- Sorts the states by total sales.
- Displays the top 5 states.
*/



/*
==========================================================
Q6. Display the top 5 cities with the highest profit.
==========================================================
*/

SELECT
    City,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY City
ORDER BY total_profit DESC
LIMIT 5;

/*
Explanation:

- Calculates total profit for each city.
- Displays the five most profitable cities.
*/



/*
==========================================================
Q7. Display the bottom 10 products based on profit.
==========================================================
*/

SELECT
    `Product Name`,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY `Product Name`
ORDER BY total_profit ASC
LIMIT 10;

/*
Explanation:

- Sorts products from lowest profit to highest.
- Helps identify products with poor performance.
*/



/*
==========================================================
Q8. Display the top 5 categories based on total quantity sold.
==========================================================
*/

SELECT
    Category,
    SUM(Quantity) AS total_quantity
FROM superstore
GROUP BY Category
ORDER BY total_quantity DESC
LIMIT 5;

/*
Explanation:

- Calculates total quantity sold for each category.
- Displays categories with the highest sales volume.
*/