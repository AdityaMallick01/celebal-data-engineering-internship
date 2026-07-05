# Week 3 - SQL Advanced Analytics

## Overview

This project focuses on applying advanced SQL concepts to analyze the Superstore dataset. It demonstrates the use of **Subqueries**, **Common Table Expressions (CTEs)**, **Window Functions**, and **JOINs** to solve real-world business problems and generate meaningful customer sales insights.

---

## Objectives

- Import the Superstore dataset into a staging table (`superstore_raw`)
- Create normalized tables using `SELECT DISTINCT`
- Apply Subqueries for advanced filtering and analysis
- Use Common Table Expressions (CTEs) for intermediate calculations
- Implement Window Functions for ranking and segmentation
- Generate customer sales insights using advanced SQL techniques

---

## Dataset

- **Dataset:** Sample Superstore
- **Source:** Kaggle
- **Database:** MySQL 8.0
- **Records:** 9,694

---

## Project Structure

```text
Week-03-SQL-Advanced-Analytics/
│
├── Database/
│   ├── create_database.sql
│   └── setup_tables.sql
│
├── Section_A/
│   └── setup.sql
│
├── Section_B/
│   └── subqueries.sql
│
├── Section_C/
│   └── ctes.sql
│
├── Section_D/
│   └── window_functions.sql
│
├── Section_E/
│   └── customer_sales_insights.sql
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

## Topics Covered

### Section A - Database Setup

- Create staging table (`superstore_raw`)
- Create `customers`, `orders`, and `products` tables
- Populate tables using `SELECT DISTINCT`

### Section B - Subqueries

- Above-average sales
- Highest sales orders
- Customer sales analysis
- Product sales analysis

### Section C - Common Table Expressions (CTEs)

- Customer sales aggregation
- Region-wise analysis
- Category-wise profit analysis
- Above-average customer sales

### Section D - Window Functions

- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- PARTITION BY
- Customer ranking

### Section E - Customer Sales Insights

- Top 5 customers
- Bottom 5 customers
- Single-order customers
- Above-average customers
- Final sales ranking using JOIN + CTE + Window Functions

---

## Learning Outcomes

Through this project, I learned to:

- Work with staging tables
- Normalize data using SQL
- Write nested Subqueries
- Use Common Table Expressions (CTEs)
- Apply Window Functions for ranking
- Combine JOINs, CTEs, and Window Functions
- Generate business insights using SQL

---

## Technologies Used

- MySQL 8.0
- SQL
- MySQL Workbench
- Visual Studio Code
- Git & GitHub

---

## Author

**Aditya Mallick**

Celebal Technologies Data Engineering Internship (CEI 2026)