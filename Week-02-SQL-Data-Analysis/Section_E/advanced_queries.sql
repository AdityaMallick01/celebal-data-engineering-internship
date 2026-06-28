/*
==========================================================
SECTION E - ADVANCED SQL
Celebal Technologies Internship - Week 2
==========================================================
*/


/*
==========================================================
Q24. Use a CASE statement to classify orders into:

High Value   -> total_amount >= 5000
Medium Value -> total_amount between 2000 and 4999
Low Value    -> total_amount < 2000
==========================================================

Explanation:
- CASE is used for conditional logic.
- Each order is categorized based on its total amount.
*/

SELECT
    order_id,
    total_amount,
    CASE
        WHEN total_amount >= 5000 THEN 'High Value'
        WHEN total_amount BETWEEN 2000 AND 4999 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_category
FROM orders;

/*
- CASE is used for conditional logic.
- Each order is categorized based on its total amount.
*/


/*
==========================================================
Q25. Start a transaction.
Increase the stock quantity of product_id = 201 by 50.
Commit the transaction.
==========================================================
*/

START TRANSACTION;

UPDATE products
SET stock_qty = stock_qty + 50
WHERE product_id = 201;

COMMIT;

-- Verify the update

SELECT *
FROM products
WHERE product_id = 201;

/*
- START TRANSACTION begins a transaction.
- UPDATE modifies the stock quantity.
- COMMIT permanently saves the changes.
*/


/*
==========================================================
Q26. Start another transaction.
Reduce the stock quantity of product_id = 202 by 100.
Instead of committing, roll back the transaction.
Verify that the data remains unchanged.
==========================================================
*/

START TRANSACTION;

UPDATE products
SET stock_qty = stock_qty - 100
WHERE product_id = 202;

ROLLBACK;

-- Verify the rollback

SELECT *
FROM products
WHERE product_id = 202;

/*
- ROLLBACK cancels all changes made during
  the current transaction.
*/


/*
==========================================================
Q27. Explain the ACID properties of transactions.
==========================================================

Answer:

1. Atomicity
- A transaction is treated as a single unit.
- Either all operations succeed or none do.

2. Consistency
- A transaction moves the database from one
  valid state to another.

3. Isolation
- Multiple transactions execute independently
  without interfering with each other.

4. Durability
- Once COMMIT is executed, changes are
  permanently stored, even if the system crashes.
*/