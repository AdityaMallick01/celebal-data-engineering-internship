# Week 5 - Spark Theory and PySpark Answers

## Q1. What are the key limitations of traditional MapReduce that make Spark a preferred choice for modern big data processing?

### Answer

MapReduce processes data by reading and writing intermediate results to disk after every stage, making it slower for modern analytics. Its major limitations include:

- Disk-based processing increases I/O overhead.
- High latency due to repeated disk access.
- Poor performance for iterative algorithms such as machine learning.
- Complex programming model requiring Mapper and Reducer classes.
- Limited support for real-time processing.

Spark overcomes these issues by:

- Performing in-memory computation.
- Providing faster execution.
- Supporting DataFrames and SQL.
- Offering libraries like Spark SQL, MLlib, GraphX, and Structured Streaming.
- Recovering data using lineage for fault tolerance.

---

## Q2. Explain how Spark uses In-Memory Computing to speed up iterative machine learning algorithms compared to disk-based systems.

### Answer

Spark stores intermediate data in memory (RAM) instead of writing it to disk after every operation. Machine learning algorithms require multiple iterations over the same dataset. Since Spark keeps data in memory, repeated computations are much faster.

Advantages:

- Reduces disk I/O.
- Faster execution.
- Efficient for iterative algorithms.
- Better CPU utilization.
- Suitable for real-time analytics.

---

## Q3. Remove duplicate rows based on user_id and transaction_date.

```python
df = df.dropDuplicates(["user_id", "transaction_date"])
```

---

## Q4. Filter rows where region is "West" and calculate average sales by product category.

```python
from pyspark.sql.functions import avg

result = df_sales.filter(df_sales.region == "West") \
                 .groupBy("product_category") \
                 .agg(avg("sale_amount").alias("average_sales"))

result.show()
```

---

## Q5. Difference between `.na.drop()` and `.na.fill()`

### `.na.drop()`

Removes rows containing null values.

```python
df = df.na.drop()
```

### `.na.fill()`

Replaces null values with a specified value.

```python
df = df.na.fill({"status": "Unknown"})
```

---

## Q6. Find total records for each city where count is greater than 100.

```python
from pyspark.sql.functions import count

result = df.groupBy("city") \
           .agg(count("*").alias("total_records")) \
           .filter("total_records > 100")

result.show()
```

---

## Q7. How does DataFrame immutability affect data cleaning?

### Answer

Spark DataFrames are immutable, meaning existing DataFrames cannot be modified directly. Operations like dropping columns or renaming columns create a new DataFrame while leaving the original unchanged.

Example:

```python
new_df = df.drop("salary")
```

Original DataFrame remains unchanged.

---

## Q8. Filter users whose age is between 18 and 30 and subscription is Premium.

```python
result = df.filter(
    (df.age.between(18, 30)) &
    (df.subscription == "Premium")
)

result.show()
```

---

## Q9. Why handle null values before aggregation?

### Answer

Handling null values before aggregation ensures accurate results because missing values can affect calculations, reduce data quality, and produce misleading statistics.

Benefits:

- Improves accuracy.
- Prevents unexpected results.
- Ensures consistent calculations.
- Produces reliable reports.

---

## Q10. Cast raw_timestamp to TimestampType and rename it to event_time.

```python
from pyspark.sql.functions import col
from pyspark.sql.types import TimestampType

df = df.withColumn(
    "event_time",
    col("raw_timestamp").cast(TimestampType())
).drop("raw_timestamp")
```

---

## Q11. Explain Shuffle.

### Answer

Shuffle is the process of redistributing data across partitions during operations like groupBy(), join(), and distinct().

It is considered a wide transformation because data moves between partitions.

Shuffle increases:

- Network communication
- Disk usage
- Execution time

Therefore, minimizing shuffle improves Spark performance.

---

## Q12. Remove rows where email is null OR username is empty.

```python
from pyspark.sql.functions import col

result = df.filter(
    col("email").isNotNull() &
    (col("username") != "")
)

result.show()
```

---

## Q13. Calculate minimum, maximum, and average price.

```python
from pyspark.sql.functions import min, max, avg

df.agg(
    min("price").alias("Minimum Price"),
    max("price").alias("Maximum Price"),
    avg("price").alias("Average Price")
).show()
```

---

## Q14. What is the risk of using `inferSchema=True` with inconsistent date formats?

### Answer

Using `inferSchema=True` on inconsistent date formats may result in incorrect data types, parsing failures, or null values. Explicitly defining the schema provides more reliable and consistent data processing.

---

## Q15. Final processing pipeline.

```python
from pyspark.sql.functions import sum

result = (
    df.dropDuplicates()
      .na.fill({"price": 0})
      .groupBy("store_id")
      .agg(sum("price").alias("total_revenue"))
)

result.show()
```