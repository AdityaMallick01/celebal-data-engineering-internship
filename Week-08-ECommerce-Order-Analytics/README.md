# Week 08 - E-Commerce Order Analytics System

## Project Overview

This final project builds an end-to-end e-commerce analytics workflow using Python, SQLite, and SQL. It generates realistic order data, cleans intentional data issues, loads the cleaned data into SQLite, runs 16 analytics queries, exposes a small CLI reporting tool, and checks edge cases with tests.

---

## Objective

To simulate a messy e-commerce dataset and turn it into a working analytics system that supports cleaning, validation, reporting, and SQL-based business analysis.

---

## Technologies Used

- Python
- SQLite
- SQL
- `sqlite3`
- Standard library modules

---

## Dataset Description

Four CSV files are generated with at least 500 rows each:

| File | Rows |
|---|---:|
| `customers.csv` | 600 |
| `products.csv` | 600 |
| `orders.csv` | 2288 |
| `order_items.csv` | 6696 |

The data spans multiple months and years and supports revenue, retention, cohort, ranking, and product-pair analysis.

---

## Project Structure

```text
Week-08-ECommerce-Order-Analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
│   └── ecommerce.db
│
├── reports/
│   └── data_quality_report.txt
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── run_analytics.py
│   └── cli_report.py
│
├── sql/
│   └── analytics.sql
│
├── tests/
│   └── test_edge_cases.py
│
└── README.md
```

---

## Data Generation

`generate_data.py` creates realistic customers, products, orders, and order items using a fixed random seed.

---

## Intentional Data Issues

- About 5% of orders have missing `customer_id`
- Some `order_date` values are written as `DD-MM-YYYY`
- About 3% of `order_items` have negative quantity
- Some product names contain extra spaces or mixed case
- About 2% of customer emails are invalid

---

## Data Cleaning

Implemented functions:

- `clean_orders()`
- `clean_products()`
- `validate_emails()`
- `check_referential_integrity()`

Cleaning results:

- Orders cleaned: 2288
- Dates corrected: 105
- Missing customer IDs preserved: 106
- Product names normalized: 93

---

## Data Validation

Validation checks were run on the generated data and written to the quality report.

- Invalid emails: 12
- Referential integrity issues: 0
- Zero quantity rows: 0
- Future orders in raw data: 0

---

## Data Quality Report

The report is saved at:

```text
reports/data_quality_report.txt
```

It is based on the actual generated and cleaned data.

---

## SQLite Database

The cleaned CSV files are loaded into:

```text
database/ecommerce.db
```

Tables:

- `customers`
- `products`
- `orders`
- `order_items`

---

## SQL Analysis

All 16 required analyses are implemented in `sql/analytics.sql` and executed successfully:

1. Revenue per category
2. Top 10 customers by order value
3. Month-wise order count for last 12 months
4. Customers who ordered but never had anything delivered
5. Products with more returns than purchases
6. Return rate per category
7. Running total by region
8. `DENSE_RANK` product ranking
9. `LAG()` order-gap analysis
10. Multi-level CTE customer categorization
11. `NTILE(4)` segmentation
12. Year-over-year comparison
13. First/last purchased category
14. Cumulative distribution
15. Cohort analysis
16. Frequently bought together product pairs

---

## CLI Reporting

The CLI is implemented in `scripts/cli_report.py`.

Example output:

```text
Week 8 Daily Report
Date range: 2026-01-01 to 2026-01-31
Total orders: 115
Revenue: 163446.74
Unique customers: 100
```

It supports:

- `daily`
- `weekly`
- `monthly`

---

## Edge Case Testing

`tests/test_edge_cases.py` verifies:

- invalid `order_id` in `order_items`
- `discount_percent > 100`
- `quantity = 0`
- future `order_date`

Test result:

```text
Ran 4 tests in 0.091s
OK
```

---

## How to Run

```bash
python scripts/generate_data.py
python scripts/clean_data.py
python scripts/load_database.py
python scripts/run_analytics.py
python scripts/cli_report.py daily 2026-01-01 2026-01-31
python -m unittest tests.test_edge_cases
```

---

## SQL Concepts Demonstrated

- JOINs
- Aggregations
- CTEs
- Window functions
- `LAG()`
- `DENSE_RANK()`
- `NTILE()`
- `FIRST_VALUE()`
- `ROW_NUMBER()`
- Cohort logic
- Cumulative sums
- Self joins
- Year-over-year comparison

---

## Results / Sample Output

### Data quality

| Check | Result |
|---|---:|
| Missing customer IDs | 106 |
| Wrong-format dates corrected | 105 |
| Negative quantity rows | 173 |
| Invalid emails | 12 |
| Referential integrity issues | 0 |

### Analytics sample

| Query | Example result |
|---|---|
| Top category revenue | Electronics |
| Top customer | `C0317` |
| Product pairs | `Usb-C Hub` + `Usb-C Hub Pro` |

---

## Conclusion

This project completes the internship with a full Python + SQLite analytics pipeline. It generates realistic messy data, cleans and validates it, loads it into SQLite, runs all required SQL analytics, and exposes a CLI summary tool.

