# Week 5: Apache Spark Data Processing

## 📌 Project Overview

This week's assignment focused on learning the fundamentals of **Apache Spark** and implementing a complete data processing workflow using **PySpark**.

The project demonstrates how Spark efficiently processes large datasets by performing data cleaning, transformation, filtering, aggregation, and grouping operations using DataFrames. It also explores Spark concepts such as **lazy evaluation**, **immutability**, and **wide transformations (shuffle)**.

---

## 🎯 Objectives

- Understand Apache Spark architecture and core concepts.
- Learn the limitations of traditional MapReduce.
- Perform data cleaning using PySpark.
- Apply filtering and transformation operations.
- Perform aggregation and group-by analysis.
- Understand wide transformations and shuffle.
- Build an end-to-end Spark data processing pipeline.
- Export the processed dataset as a CSV file.

---

## 🛠️ Technologies Used

- Python 3.13
- Apache Spark (PySpark 4.2.0)
- Hadoop (Local Windows Configuration)
- Jupyter Notebook
- VS Code

---

## 📂 Project Structure

```
Week-05-Spark-Data-Processing/
│── data/
│   └── Sample - Superstore.csv
│
│── notebook/
│   └── Spark_Data_Processing.ipynb
│
│── output/
│   └── final_results.csv
│
│── docs/
│   └── Spark_Theory_Answers.md
│
│── README.md
│── requirements.txt
```

---

## 📊 Dataset

**Dataset Used:** Sample Superstore Dataset

The dataset contains retail sales information, including:

- Orders
- Customers
- Products
- Sales
- Profit
- Quantity
- Region
- Category
- Order Date
- Ship Date

---

## ⚙️ Tasks Performed

### 1. Spark Session Creation

- Created a SparkSession.
- Loaded the CSV dataset into a Spark DataFrame.

### 2. Data Exploration

- Displayed sample records.
- Printed schema.
- Checked row and column counts.

### 3. Data Cleaning

- Removed duplicate records.
- Checked for missing values.
- Handled null values where applicable.

### 4. Data Transformation

- Renamed columns.
- Converted date columns to proper date format.
- Verified updated schema.

### 5. Data Filtering

Applied multiple filters such as:

- Region-based filtering
- Category-based filtering
- Sales greater than a threshold
- Multiple-condition filtering
- Positive profit records

### 6. Aggregation

Calculated:

- Total Sales
- Average Sales
- Minimum Sales
- Maximum Sales
- Profit statistics
- Quantity statistics

### 7. GroupBy Operations

Performed analysis by:

- Category
- Region
- State
- City

### 8. Wide Transformation

Used **groupBy()** to demonstrate Spark's shuffle mechanism and explain wide transformations.

### 9. Complete Data Pipeline

Implemented a complete Spark pipeline consisting of:

- Data Cleaning
- Data Transformation
- Filtering
- Aggregation
- Sorting
- Exporting Results

---

## 📝 Theory Questions

The assignment also includes answers to all Spark theory questions covering:

- Spark vs MapReduce
- In-Memory Computing
- Duplicate Removal
- Filtering
- Handling Missing Values
- GroupBy
- Aggregations
- Immutability
- Schema Modification
- Shuffle
- End-to-End Spark Pipeline

Theory answers are available in:

```
docs/Spark_Theory_Answers.md
```

---

## 📈 Output

The processed dataset is exported to:

```
output/final_results.csv
```

---

## 📚 Learning Outcomes

Through this assignment, I learned:

- Apache Spark fundamentals
- Spark DataFrames
- Lazy Evaluation
- Spark Transformations and Actions
- Data Cleaning using PySpark
- Filtering and Aggregations
- GroupBy Operations
- Shuffle and Wide Transformations
- Building an end-to-end Spark data processing pipeline

---

## ▶️ How to Run

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Open the notebook:

```
notebook/Spark_Data_Processing.ipynb
```

3. Run all notebook cells sequentially.

4. The processed dataset will be generated inside the `output` directory.

---
