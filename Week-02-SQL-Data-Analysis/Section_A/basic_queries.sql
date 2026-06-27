/*
==========================================================
SECTION A - SQL BASICS
Celebal Technologies Internship - Week 2
==========================================================
*/


/*
==========================================================
Q1. Display all columns and rows from the customers table.
==========================================================
*/

SELECT *
FROM customers;

/*
- SELECT * retrieves all columns.
- FROM customers specifies the source table.
- This query displays every customer record stored in the
  customers table.
*/


/*
==========================================================
Q2. Retrieve only the first_name, last_name, and city
of all customers.
==========================================================
*/

SELECT
    first_name,
    last_name,
    city
FROM customers;

/*
- Instead of retrieving every column, we select only the
  required columns.
- This improves readability and reduces unnecessary data.
*/


/*
==========================================================
Q3. List all unique categories available in the
products table.
==========================================================
*/

SELECT DISTINCT category
FROM products;

/*
- DISTINCT removes duplicate values.
- Since multiple products belong to the same category,
  DISTINCT returns each category only once.
*/


/*
==========================================================
Q4. Identify the Primary Key of each table.
Explain why a Primary Key must be unique and NOT NULL.
==========================================================

Answer:

customers     -> customer_id

products      -> product_id

orders        -> order_id

order_items   -> item_id

A Primary Key:
- Uniquely identifies each record.
- Cannot contain duplicate values.
- Cannot contain NULL values.
- Is used to establish relationships between tables
  using Foreign Keys.
*/



/*
==========================================================
Q5. What constraints are applied to the email column
in the customers table?
What happens if you insert a duplicate email?
==========================================================

Answer:

Constraints:

1. NOT NULL
   Every customer must have an email.

2. UNIQUE
   Duplicate email addresses are not allowed.

If a duplicate email is inserted,
MySQL returns a Duplicate Entry error because of the
UNIQUE constraint.
*/



/*
==========================================================
Q6. Try inserting a product with unit_price = -50.
What happens and which constraint prevents it?
==========================================================
*/

INSERT INTO products
VALUES
(
    301,
    'Invalid Product',
    'Electronics',
    'TestBrand',
    -50,
    100
);
/*
The CHECK constraint

CHECK(unit_price > 0)

does not allow negative prices.

Therefore, this INSERT statement should fail.

Expected Result:

ERROR:
CHECK constraint violated because unit_price
must be greater than zero.
*/