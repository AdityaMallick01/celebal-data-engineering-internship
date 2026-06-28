/*
==========================================================
SECTION D - JOINS
Celebal Technologies Internship - Week 2
==========================================================
*/


/*
==========================================================
Q19. Display each order along with the customer's
first name, last name, and order date.
==========================================================
*/

SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders AS o
INNER JOIN customers AS c
ON o.customer_id = c.customer_id;

/*
- INNER JOIN combines the orders and customers tables.
- The customer_id column is used to match records.
- Only matching records from both tables are returned.
*/
  

/*
==========================================================
Q20. Display each order item with its product name,
quantity, unit price, and discount percentage.
==========================================================
*/

SELECT
    oi.item_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct
FROM order_items AS oi
INNER JOIN products AS p
ON oi.product_id = p.product_id;

/*
- INNER JOIN combines order_items and products.
- The product_id column links both tables.
*/


/*
==========================================================
Q21. Display every customer along with their orders.
Include customers even if they have not placed any orders.
==========================================================
*/

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.status
FROM customers AS c
LEFT JOIN orders AS o
ON c.customer_id = o.customer_id;

/*
- LEFT JOIN returns all customers.
- Matching orders are displayed where available.
- Customers without orders will show NULL values for
  order-related columns.
*/


/*
==========================================================
Q22. Display the order ID, customer name,
product name, quantity, and total amount for every order.
==========================================================
*/

SELECT
    o.order_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    p.product_name,
    oi.quantity,
    o.total_amount
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
INNER JOIN products AS p
ON oi.product_id = p.product_id;

/*
- This query joins four related tables.
- customers -> orders -> order_items -> products
- It provides a complete view of each purchased product.
*/


/*
==========================================================
Q23. Explain the difference between INNER JOIN
and LEFT JOIN with examples from this database.
==========================================================

Answer:

INNER JOIN
-----------
- Returns only matching rows from both tables.
- Customers without orders are excluded.

Example:

SELECT
    c.first_name,
    o.order_id
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id;


LEFT JOIN
----------
- Returns all rows from the left table.
- Matching rows from the right table are included.
- If no match exists, NULL values are returned.

Example:

SELECT
    c.first_name,
    o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

In this dataset every customer has an order,
so both queries currently return the same number of rows.
If a customer had no orders, only the LEFT JOIN
would include that customer.
*/