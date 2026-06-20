# Week 1 - Data Exploration and Cleaning using Pandas

## Objective

The objective of this assignment was to perform data exploration and cleaning on the Shopping Dataset using Python and Pandas. Multiple CSV files were loaded, combined into a single dataset, cleaned, transformed, and exported for further analysis.

---

## Dataset

**Dataset:** Shopping Dataset

The dataset consists of multiple CSV files containing product-related information such as product details, ratings, prices, discounts, categories, seller information, and customer reviews.

---

## Tools and Technologies

- Python
- Pandas
- Jupyter Notebook
- VS Code
- Git & GitHub

---

## Project Structure

```text
Week-01-Data-Exploration/
│
├── data/
│   └── CSV dataset files
│
├── notebooks/
│   └── Shopping_Data_Exploration.ipynb
│
├── output/
│   └── cleaned_combined_dataset.csv
│
└── README.md
```

---

## Tasks Performed

### 1. Data Loading

- Loaded all CSV files from the dataset directory.
- Combined multiple files into a single Pandas DataFrame.

### 2. Data Exploration

Performed exploratory analysis using:

- `head()`
- `tail()`
- `shape`
- `columns`
- `dtypes`
- `info()`
- `describe()`

---

### 3. Handling Missing Values

- Identified missing values using `isnull()`.
- Filled missing categorical values with `"Unknown"`.
- Filled missing numerical values with `0`.
- Demonstrated the use of `dropna()` for critical fields.

---

### 4. Removing Duplicate Records

- Checked for duplicate rows.
- Removed duplicate records using `drop_duplicates()`.

---

### 5. Data Type Conversion

- Converted price columns from text format to numeric format.
- Removed currency symbols and commas before conversion.

---

### 6. Basic Data Operations

Performed:

- Column selection
- Row filtering
- Data inspection

Example:

- Selected relevant columns such as product title and prices.
- Filtered products based on price conditions.

---

### 7. Feature Engineering

The dataset did not contain a quantity column, so the example feature:

```python
total_amount = price * quantity
```

could not be created.

Instead, a new derived feature named **estimated_savings** was created using:

```python
estimated_savings = initial_price * discount / 100
```

---

### 8. Exporting Cleaned Dataset

The cleaned and transformed dataset was exported as:

```text
output/cleaned_combined_dataset.csv
```

---

## Output Files

### Jupyter Notebook

```text
notebooks/Shopping_Data_Exploration.ipynb
```

Contains:

- Data loading
- Data exploration
- Data cleaning
- Data transformation
- Feature engineering
- Final summary

### Cleaned Dataset

```text
output/cleaned_combined_dataset.csv
```

---

## Key Learnings

Through this assignment, I learned:

- Loading and combining multiple CSV files
- Data exploration using Pandas
- Handling missing values
- Removing duplicate records
- Data type conversion
- Feature engineering
- Exporting processed datasets
- Maintaining a structured Data Engineering project repository

---

## Conclusion

The Shopping Dataset was successfully explored, cleaned, transformed, and exported using Pandas. The final dataset is free from duplicate records, contains handled missing values, includes a derived feature (`estimated_savings`), and is ready for further analysis and processing.