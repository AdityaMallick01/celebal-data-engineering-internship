# Week 6: Apache Spark Fundamentals

## 📌 Project Overview

The objective of this week's assignment was to understand the fundamentals of **Apache Spark** and perform distributed data processing using **PySpark DataFrames**.

The project demonstrates Spark's execution model, DataFrame transformations, lazy evaluation, schema handling, performance optimization techniques, and a simple ETL pipeline using the **Sample Superstore** dataset.

---

## 🎯 Objectives

- Understand Apache Spark Architecture
- Learn the roles of Driver, Cluster Manager, and Executors
- Explore Lazy Evaluation and DAG execution
- Read CSV files with schema inference
- Perform DataFrame transformations
- Select and filter data
- Rename columns and cast data types
- Add calculated columns
- Handle null values
- Understand Transformations and Actions
- Learn Wide Transformations and Shuffle
- Explore Predicate Pushdown
- Compare CSV and Parquet file formats
- Build a simple ETL pipeline
- Follow Spark performance best practices

---

## 📂 Dataset

**Dataset Used:** Sample Superstore

The dataset contains retail sales information including:

- Order Details
- Customer Information
- Product Details
- Region
- Sales
- Quantity
- Discount
- Profit

---

## 🛠️ Technologies Used

- Apache Spark
- PySpark
- Python
- Jupyter Notebook

---

## 📚 Concepts Covered

### Spark Fundamentals

- Spark Architecture
- Driver, Cluster Manager & Executors
- Client Mode vs Cluster Mode
- Lazy Evaluation
- Directed Acyclic Graph (DAG)

### DataFrame Operations

- Reading CSV Files
- Schema Inference
- Column Selection
- Filtering Data
- Renaming Columns
- Type Casting
- Creating New Columns
- Handling Null Values

### Spark Performance

- Transformations
- Actions
- Narrow Transformations
- Wide Transformations
- Shuffle
- Predicate Pushdown

### Data Engineering

- CSV vs Parquet
- Read → Transform → Filter → Write Pipeline
- Writing CSV Files
- Writing Parquet Files

---

## 📁 Project Structure

```text
Week-06-Spark-Fundamentals/
│
├── Week6_Spark_Fundamentals.ipynb
├── README.md
├── Answers.md
├── data/
│   └── Sample - Superstore.csv
│
└── output/
    ├── csv/
    └── parquet/
```

---

## 🚀 Workflow

```
Read CSV
      │
      ▼
Infer Schema
      │
      ▼
Transform Data
      │
      ▼
Filter Records
      │
      ▼
Handle Null Values
      │
      ▼
Create New Columns
      │
      ▼
Write CSV
      │
      ▼
Write Parquet
```

---

## 📊 Key Learning Outcomes

- Understood Apache Spark architecture and distributed computing concepts.
- Learned how Spark executes jobs using Lazy Evaluation and DAG.
- Performed common DataFrame transformations using PySpark.
- Explored filtering, schema handling, type casting, and column operations.
- Understood the difference between Transformations and Actions.
- Learned how Shuffle and Predicate Pushdown affect Spark performance.
- Compared CSV and Parquet storage formats.
- Built a simple ETL pipeline using Spark DataFrames.
- Applied Spark best practices for scalable data processing.

---

## 📌 Conclusion

This assignment provided practical exposure to Apache Spark and PySpark by implementing common DataFrame operations on the Sample Superstore dataset. It covered essential concepts such as Spark Architecture, Lazy Evaluation, DAG execution, Transformations, Actions, Shuffle, Predicate Pushdown, and file format optimization.

The project also demonstrated a complete ETL workflow by reading raw data, applying transformations, filtering records, handling schema changes, and writing the processed data to both CSV and Parquet formats. These concepts form the foundation of scalable data engineering and big data processing using Apache Spark.