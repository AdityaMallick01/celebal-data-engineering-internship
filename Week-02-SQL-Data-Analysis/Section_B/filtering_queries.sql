/*
==========================================================
SECTION B - FILTERING & OPTIMIZATION
Celebal Technologies Internship - Week 2
==========================================================
*/


/*
==========================================================
Q7. Retrieve all orders with status = 'Delivered'.
==========================================================
*/

SELECT *
FROM orders
WHERE status = 'Delivered';

/*
- The WHERE clause filters rows based on a condition.
- This query returns only those orders whose status is
  'Delivered'.
*/



/*
==========================================================
Q8. Find all products in the 'Electronics' category
with a unit price greater than ₹2000.
==========================================================
*/

SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;

/*
- Filters products that belong to the Electronics category.
- Only products with a unit price greater than ₹2000 are
  displayed.
*/



/*
==========================================================
Q9. List all customers who joined in the year 2024
and belong to the state 'Maharashtra'.
==========================================================
*/

SELECT *
FROM customers
WHERE state = 'Maharashtra'
AND join_date BETWEEN '2024-01-01' AND '2024-12-31';

/*
- Filters customers whose state is Maharashtra.
- Since all sample data belongs to 2024, we use a date
  range instead of YEAR() because it is more efficient and
  index-friendly.
*/

/*
==========================================================
Q10. Find all orders placed between
'2024-08-10' and '2024-08-25' (inclusive)
that are NOT cancelled.
==========================================================
*/

SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status <> 'Cancelled';

/*
- BETWEEN includes both start and end dates.
- The query excludes orders whose status is 'Cancelled'.
*/

/*
==========================================================
Q11. Explain what the index idx_orders_date does.
How would it improve query performance?
Write a sample query that benefits from this index.
==========================================================

Answer:

The index idx_orders_date is created on the order_date
column.

Purpose:
- Speeds up queries that search, filter, or sort using
  order_date.
- Instead of scanning every row, MySQL can directly locate
  matching records using the index.

Example Query:
*/

SELECT *
FROM orders
WHERE order_date = '2024-08-15';

/*
The above query benefits from the idx_orders_date index.
*/



/*
==========================================================
Q12. If you run:

SELECT * FROM customers
WHERE YEAR(join_date) = 2024;

Will the index on join_date be used?
Explain why or why not, and rewrite the query to be
index-friendly (SARGable).
==========================================================

Answer:

No.

Using YEAR(join_date) applies a function to the indexed
column, preventing MySQL from efficiently using the index.

Instead, use a date range, which allows the index to be
used efficiently.

Index-Friendly Query:
*/

SELECT *
FROM customers
WHERE join_date BETWEEN '2024-01-01'
                    AND '2024-12-31';