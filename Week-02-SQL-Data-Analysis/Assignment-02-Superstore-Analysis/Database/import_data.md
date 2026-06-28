# Importing the Dataset

## Database

```sql
CREATE DATABASE superstore_analysis;
USE superstore_analysis;
```

## Import Steps

1. Open MySQL Workbench.
2. Right-click the `superstore_analysis` database.
3. Select **Table Data Import Wizard**.
4. Choose `Sample - Superstore.csv`.
5. Create a new table named `superstore`.
6. Adjust the data types if necessary.
7. Finish the import.

## Verification

Run:

```sql
SELECT COUNT(*) FROM superstore;
```

Expected result:

```
9694
```
