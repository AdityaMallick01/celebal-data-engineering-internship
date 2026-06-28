/*
==========================================================
MODULE 2 - FILTERING DATA
Superstore SQL Analysis
==========================================================
*/


/*
==========================================================
Q1. Display all orders from the South region.
==========================================================
*/

SELECT *
FROM superstore
WHERE Region = 'South';

/*
Explanation:

- WHERE filters rows based on a condition.
- Returns only orders from the South region.
*/



/*
==========================================================
Q2. Display all products in the Technology category.
==========================================================
*/

SELECT *
FROM superstore
WHERE Category = 'Technology';

/*
Explanation:

- Filters records belonging only to the Technology category.
*/



/*
==========================================================
Q3. Display all orders where Sales are greater than 1000.
==========================================================
*/

SELECT *
FROM superstore
WHERE Sales > 1000;

/*
Explanation:

- Displays orders whose sales amount exceeds ₹1000.
*/



/*
==========================================================
Q4. Display all orders where Profit is negative.
==========================================================
*/

SELECT *
FROM superstore
WHERE Profit < 0;

/*
Explanation:

- Finds loss-making orders.
*/



/*
==========================================================
Q5. Display orders placed between
01/01/2016 and 31/12/2016.
==========================================================
*/

SELECT *
FROM superstore
WHERE STR_TO_DATE(`Order Date`, '%m/%d/%Y')
BETWEEN '2016-01-01' AND '2016-12-31';

/*
Explanation:

- STR_TO_DATE converts text into DATE format.
- BETWEEN includes both start and end dates.
*/



/*
==========================================================
Q6. Display all orders from California.
==========================================================
*/

SELECT *
FROM superstore
WHERE State = 'California';

/*
Explanation:

- Filters records where the State is California.
*/



/*
==========================================================
Q7. Display all Furniture products with Sales
greater than 500.
==========================================================
*/

SELECT *
FROM superstore
WHERE Category = 'Furniture'
AND Sales > 500;

/*
Explanation:

- AND combines multiple conditions.
- Both conditions must be true.
*/



/*
==========================================================
Q8. Display all orders from the East or West region.
==========================================================
*/

SELECT *
FROM superstore
WHERE Region IN ('East','West');

/*
Explanation:

- IN checks multiple possible values.
- More readable than multiple OR conditions.
*/



/*
==========================================================
Q9. Display customers whose name starts with 'A'.
==========================================================
*/

SELECT *
FROM superstore
WHERE `Customer Name` LIKE 'A%';

/*
Explanation:

- LIKE performs pattern matching.
- A% means names beginning with A.
*/



/*
==========================================================
Q10. Display all orders with Discount greater than 0.
==========================================================
*/

SELECT *
FROM superstore
WHERE Discount > 0;

/*
Explanation:

- Returns all orders where a discount was applied.
*/