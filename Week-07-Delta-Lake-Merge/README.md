# Week 07: Delta Lake MERGE Operations using Apache Spark

## 📌 Project Overview

The objective of this week's assignment was to understand and implement **Delta Lake MERGE operations** using **Apache Spark** on **Databricks**.

The project demonstrates how to:

- Load and clean a CSV dataset
- Create a Delta Lake table
- Prepare incremental data
- Perform UPSERT operations using the `MERGE` command
- Validate the final merged dataset

---

## 🎯 Objectives

- Learn Delta Lake fundamentals
- Create Delta tables from Spark DataFrames
- Perform data cleaning before storage
- Implement incremental data loading
- Execute MERGE (UPSERT) operations
- Validate merged data

---

## 🛠️ Technologies Used

- Apache Spark (PySpark)
- Delta Lake
- Databricks Free Edition
- Python
- Git & GitHub

---

## 📂 Project Structure

```
Week-07-Delta-Lake-Merge-Operations/
│
├── README.md
├── delta_merge_assignment.ipynb
├── dataset/
│   └── Sample - Superstore.csv
└── screenshots/
    ├── 01_dataset_loaded.png
    ├── 02_schema_inference.png
    ├── 03_null_value_validation.png
    ├── 04_cleaned_dataset_schema.png
    ├── 05_duplicate_validation.png
    ├── 06_cleaned_dataset_null_check.png
    ├── 07_cleaned_dataset_preview.png
    ├── 08_delta_table_preview.png
    ├── 09_incremental_data_prepared.png
    ├── 10_delta_merge_execution.png
    ├── 11_final_delta_table.png
    ├── 12_merge_validation.png
    └── 13_assignment_summary.png
```

---

## 📊 Dataset

**Dataset Used:** Sample Superstore Dataset

The dataset contains retail sales information including:

- Order Details
- Customer Information
- Product Information
- Sales
- Profit
- Quantity
- Discount

---

## 🔄 Workflow

### Step 1 – Load Dataset

- Read CSV file using Spark
- Infer schema automatically
- Display the dataset

📷 Screenshot

`01_dataset_loaded.png`

---

### Step 2 – Verify Schema

- Check inferred data types
- Validate column structure

📷 Screenshot

`02_schema_inference.png`

---

### Step 3 – Validate Missing Values

- Count NULL values in every column
- Ensure data completeness

📷 Screenshot

`03_null_value_validation.png`

---

### Step 4 – Data Cleaning

Performed the following operations:

- Removed spaces from column names
- Converted numeric columns to proper data types
- Standardized schema

📷 Screenshot

`04_cleaned_dataset_schema.png`

---

### Step 5 – Duplicate Validation

Verified that no duplicate records exist after cleaning.

📷 Screenshot

`05_duplicate_validation.png`

---

### Step 6 – Final Data Validation

Performed another NULL check after cleaning.

📷 Screenshot

`06_cleaned_dataset_null_check.png`

---

### Step 7 – Preview Clean Dataset

Displayed the cleaned Spark DataFrame.

📷 Screenshot

`07_cleaned_dataset_preview.png`

---

### Step 8 – Create Delta Table

Stored the cleaned DataFrame in Delta format.

📷 Screenshot

`08_delta_table_preview.png`

---

### Step 9 – Prepare Incremental Data

Created sample incremental records including:

- New customer records
- Existing records for update

📷 Screenshot

`09_incremental_data_prepared.png`

---

### Step 10 – Perform MERGE Operation

Executed Delta Lake MERGE using:

- `whenMatchedUpdateAll()`
- `whenNotMatchedInsertAll()`

📷 Screenshot

`10_delta_merge_execution.png`

---

### Step 11 – Verify Final Delta Table

Loaded the updated Delta table and verified the results.

📷 Screenshot

`11_final_delta_table.png`

---

### Step 12 – Validate MERGE Results

Checked duplicate Order IDs and validated merged data.

📷 Screenshot

`12_merge_validation.png`

---

### Step 13 – Assignment Summary

Displayed final statistics including:

- Original Rows
- Cleaned Rows
- Incremental Rows
- Final Rows
- Duplicate Order IDs
- MERGE Status

📷 Screenshot

`13_assignment_summary.png`

---

## 📈 Final Results

| Metric | Value |
|---------|-------|
| Original Records | 9994 |
| Records After Cleaning | 9994 |
| Incremental Records | 10 |
| Final Records After MERGE | 9999 |
| Duplicate Order IDs | 0 |
| MERGE Status | Successful |

---

## 📚 Key Concepts Learned

- Apache Spark DataFrames
- Schema Inference
- Data Cleaning
- Delta Lake
- Delta Table Creation
- Incremental Data Loading
- UPSERT using MERGE
- Data Validation
- Databricks Notebook Workflow

---

## ✅ Conclusion

This project demonstrates an end-to-end implementation of **Delta Lake MERGE operations** using Apache Spark.

The workflow successfully:

- Loaded retail sales data
- Cleaned and validated the dataset
- Created a Delta table
- Simulated incremental data
- Executed UPSERT operations using MERGE
- Verified the integrity of the final dataset

The project provides practical experience with one of the most commonly used data engineering operations in modern data lake architectures.

---

## 👨‍💻 Author

**Aditya Mallick**

Celebal Technologies Data Engineering Internship (CEI 2026)