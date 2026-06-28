/*
==========================================================
SECTION C - AGGREGATION FUNCTIONS
Celebal Technologies Internship - Week 2
==========================================================
*/


/*
==========================================================
Q13. Count the total number of customers.
==========================================================
*/

SELECT COUNT(*) AS total_customers
FROM customers;

/*
- COUNT(*) returns the total number of rows in the table.
*/

/*
==========================================================
Q14. Find the total sales amount from all orders.
==========================================================
*/

SELECT SUM(total_amount) AS total_sales
FROM orders;

/*
- SUM() calculates the total value of the total_amount
  column from all orders.
*/

/*
==========================================================
Q15. Calculate the average unit price of all products.
==========================================================
*/

SELECT AVG(unit_price) AS average_unit_price
FROM products;

/*
- AVG() returns the average value of the unit_price column.
*/

/*
==========================================================
Q16. Find the highest and lowest priced product.
==========================================================
*/

SELECT
    MAX(unit_price) AS highest_price,
    MIN(unit_price) AS lowest_price
FROM products;

/*
- MAX() returns the highest unit price.
- MIN() returns the lowest unit price.
*/

/*
==========================================================
Q17. Display the total sales amount for each order status.
==========================================================
*/

SELECT
    status,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY status;

/*
- GROUP BY groups records based on order status.
- SUM() calculates total sales for each status.
*/

/*
==========================================================
Q18. Show categories where the average product price
is greater than ₹2000.
==========================================================
*/

SELECT
    category,
    AVG(unit_price) AS average_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

/*
- GROUP BY creates groups for each category.
- AVG() calculates the average price.
- HAVING filters grouped results after aggregation.
*/