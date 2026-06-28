# Week 2 – SQL Data Analysis

## Objective

The objective of this assignment is to analyze an E-Commerce Sales Database using SQL by applying filtering, aggregation, joins, and advanced SQL concepts. The project demonstrates fundamental database design, query optimization, and data analysis techniques.

---

## Technologies Used

* MySQL
* SQL
* Visual Studio Code
* MySQL Workbench
* Git & GitHub

---

## Project Structure

```text
Week-02-SQL-Data-Analysis/
│
├── Database/
│   ├── create_tables.sql
│   ├── create_indexes.sql
│   └── insert_data.sql
│
├── Section_A/
│   └── basic_queries.sql
│
├── Section_B/
│   └── filtering_queries.sql
│
├── Section_C/
│   └── aggregation_queries.sql
│
├── Section_D/
│   └── joins_queries.sql
│
├── Section_E/
│   └── advanced_queries.sql
│
├── Results/
│   ├── Section_A/
│   ├── Section_B/
│   ├── Section_C/
│   ├── Section_D/
│   └── Section_E/
│
└── README.md
```

---

## Database Schema

The database consists of four related tables:

* **customers** – Stores customer information.
* **products** – Stores product details and inventory.
* **orders** – Stores order information.
* **order_items** – Stores individual products within each order.

The relationships are maintained using **Primary Keys** and **Foreign Keys**.

---

## Topics Covered

### Section A – SQL Basics

* SELECT
* DISTINCT
* Primary Keys
* Constraints
* CHECK Constraint Validation

### Section B – Filtering

* WHERE
* AND
* BETWEEN
* Index-Friendly Queries
* Query Optimization

### Section C – Aggregation

* COUNT()
* SUM()
* AVG()
* MAX()
* MIN()
* GROUP BY
* HAVING

### Section D – Joins

* INNER JOIN
* LEFT JOIN
* Multi-table JOINs

### Section E – Advanced SQL

* CASE Statements
* Transactions
* COMMIT
* ROLLBACK
* ACID Properties

---

## Results

Each section includes:

* SQL queries
* Query execution results
* Output screenshots

The screenshots are organized inside the **Results** folder for easy reference.

---

## Learning Outcomes

Through this assignment, I learned:

* Database creation and normalization
* SQL filtering and aggregation
* Working with joins across multiple tables
* Index creation and query optimization
* Transaction management
* Writing clean, well-documented SQL scripts
* Organizing SQL projects using GitHub

