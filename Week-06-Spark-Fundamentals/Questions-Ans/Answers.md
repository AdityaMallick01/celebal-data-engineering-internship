# Week 6: Apache Spark Fundamentals

## Overview

This week's assignment focuses on understanding the fundamentals of **Apache Spark** and implementing common DataFrame operations using **PySpark**. The objective is to gain practical experience with Spark architecture, lazy evaluation, DataFrame transformations, file formats, and performance optimization techniques used in large-scale data processing.

The implementation uses the **Sample Superstore** dataset to demonstrate Spark concepts through hands-on examples.

---

## Objectives

- Understand Apache Spark Architecture
- Learn Driver, Cluster Manager, and Executor roles
- Understand Lazy Evaluation and DAG execution
- Read CSV files with schema inference
- Perform DataFrame transformations
- Select and filter data
- Rename columns and cast data types
- Add calculated columns
- Handle null values
- Understand Transformations and Actions
- Learn Wide Transformations and Shuffle
- Understand Predicate Pushdown
- Compare CSV and Parquet formats
- Build a simple ETL pipeline
- Apply Spark best practices

---

## Dataset

**Dataset Used:** Sample Superstore

The dataset contains sales information including:

- Order Details
- Customer Information
- Product Information
- Region
- Sales
- Quantity
- Discount
- Profit

---

# Assignment Questions & Answers

## Q1. Explain the roles of the Driver, Cluster Manager, and Executor in a Spark application.

### Answer

- **Driver:** The Driver is the main process that controls the Spark application. It creates the SparkSession, converts user code into tasks, builds the execution plan (DAG), and coordinates execution.

- **Cluster Manager:** The Cluster Manager allocates resources across the cluster and manages worker nodes. Examples include Standalone, YARN, Mesos, and Kubernetes.

- **Executors:** Executors run on worker nodes, execute the tasks assigned by the Driver, perform computations, and store intermediate results.

---

## Q2. How does Spark's Lazy Evaluation strategy improve performance when chain-processing large datasets?

### Answer

Spark does not execute transformations immediately. Instead, it records all transformations in a **Directed Acyclic Graph (DAG)** and waits until an action such as `show()` or `count()` is called.

This allows Spark to:

- Optimize execution plans
- Remove unnecessary operations
- Reduce data movement
- Improve overall performance

---

## Q3. Write a Spark command to read a CSV file located at `data/source.csv`, ensuring the first row is treated as a header and `inferSchema` is enabled.

```python
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/source.csv")
```

---

## Q4. What is the difference between CSV and Parquet in terms of storage and why does it matter for performance?

| CSV | Parquet |
|------|----------|
| Row-based storage | Column-based storage |
| Plain text | Binary format |
| Larger file size | Compressed storage |
| Slower analytical queries | Faster analytical queries |
| No Predicate Pushdown | Supports Predicate Pushdown |

### Answer

Parquet stores data in a columnar format, allowing Spark to read only the required columns instead of the entire dataset. This reduces disk I/O, memory usage, and query execution time.

---

## Q5. Given a DataFrame `df`, write a query to select the columns `product_id` and `price` where the category is `Electronics`.

```python
df.filter(df.category == "Electronics") \
  .select("product_id", "price")
```

---

## Q6. Rename the column `old_name` to `new_name` and cast the `price` column from String to Double.

```python
from pyspark.sql.functions import col

df = df.withColumnRenamed("old_name", "new_name") \
       .withColumn("price", col("price").cast("double"))
```

---

## Q7. How does Spark use the Lineage Graph (DAG) to provide fault tolerance if a worker node fails?

### Answer

Spark records every transformation in a **Lineage Graph (DAG)**.

If a worker node fails and loses a partition, Spark recomputes only the lost partition using the stored lineage instead of recomputing the entire dataset. This provides efficient fault tolerance.

---

## Q8. Write a query to filter a DataFrame `df_orders` for rows where the status is `Completed` AND the amount is greater than `1000`.

```python
df_orders.filter(
    (df_orders.status == "Completed") &
    (df_orders.amount > 1000)
)
```

---

## Q9. Explain the concept of Predicate Pushdown in Parquet and how it affects the amount of data loaded into memory.

### Answer

Predicate Pushdown is a Spark optimization technique where filter conditions are pushed down to the Parquet storage layer.

Instead of reading the complete dataset, Spark reads only the rows that satisfy the filter condition.

Benefits include:

- Reduced disk I/O
- Lower memory usage
- Faster query execution
- Improved performance

---

## Q10. Write a code snippet to add a new column `final_price` which is the `base_price` multiplied by `1.18` (18% tax).

```python
from pyspark.sql.functions import col

df = df.withColumn(
    "final_price",
    col("base_price") * 1.18
)
```

---

## Q11. What is the difference between Transformations and Actions? Provide two examples of each.

| Transformations | Actions |
|-----------------|----------|
| Lazy operations | Trigger execution |
| Return a new DataFrame | Return results or write output |

### Examples

**Transformations**

- `filter()`
- `select()`

**Actions**

- `show()`
- `count()`

---

## Q12. Write the Spark command to load a Parquet file from `"path/to/input"`, filter out any rows where `user_id` is null, and save the result as a CSV at `"path/to/output"`.

```python
df = spark.read.parquet("path/to/input")

df.filter(df.user_id.isNotNull()) \
  .write \
  .mode("overwrite") \
  .option("header", True) \
  .csv("path/to/output")
```

---

## Q13. In Spark Architecture, what is the difference between Client Mode and Cluster Mode?

| Client Mode | Cluster Mode |
|-------------|--------------|
| Driver runs on the client machine | Driver runs inside the cluster |
| Suitable for development | Suitable for production |
| Client must remain connected | Continues running even if the client disconnects |

---

## Q14. Write a query to filter a dataset for rows where the `region` is `North` OR the `priority` is `High`.

```python
df.filter(
    (df.region == "North") |
    (df.priority == "High")
)
```

---

## Q15. When exploring a dataset, why is it safer to use `.show(5)` instead of `.collect()` on a multi-terabyte dataset?

### Answer

The `.show(5)` function retrieves only a few rows for display, making it memory-efficient.

The `.collect()` function transfers the entire dataset from the cluster to the Driver.

For very large datasets, using `.collect()` may consume excessive memory and can cause the Driver application to crash due to an OutOfMemory error.

Therefore, `.show(5)` is the recommended approach for inspecting large datasets.

---

## Conclusion

This assignment provided practical exposure to Apache Spark fundamentals and DataFrame operations using PySpark. Key concepts such as Spark Architecture, Lazy Evaluation, DAG, Transformations, Actions, Wide Transformations, Shuffle, and Predicate Pushdown were explored alongside hands-on data processing tasks.

The implementation demonstrated reading CSV files, handling schemas, transforming and filtering data, managing null values, comparing CSV and Parquet formats, and building a simple ETL pipeline. These concepts form the foundation of scalable data engineering workflows and efficient big data processing using Apache Spark.