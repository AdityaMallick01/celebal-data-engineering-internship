# LearnTrack — LMS Analytics Pipeline

## Overview

LearnTrack is an end-to-end Learning Management System (LMS) analytics data engineering project built using a Medallion Architecture:

**Raw CSV → Bronze Delta → Silver Delta → SCD Type 2 → Gold Delta → SQL Analytics**

The project processes LMS learner, course, and enrolment activity data and transforms it into analytics-ready datasets for understanding learner engagement, course completion, instructor performance, assessments, dropout patterns, and re-enrolments.

### Technologies

- Python
- PySpark
- Delta Lake
- Databricks Serverless
- Unity Catalog Volumes
- Spark SQL
- PyYAML
- pytest

---

## Project Structure

```text
LearnTrack-LMS-Analytics-Pipeline/
├── data/
│   └── raw/
│       ├── courses.csv
│       ├── enrolment_activity.csv
│       └── learners.csv
│
├── notebooks/
│   └── pipeline_notebook.py
│
├── src/
│   ├── config_utils.py
│   ├── bronze.py
│   ├── validate.py
│   ├── run_light_validation.py
│   ├── silver.py
│   ├── scd_instructor.py
│   └── gold.py
│
├── sql/
│   └── analytics_queries.sql
│
├── tests/
│   └── test_pipeline.py
│
├── docs/
│   ├── architecture.md
│   └── validation_report.md
│
├── config.yml
├── requirements.txt
└── README.md
```

---

## Databricks Serverless Execution

Databricks Serverless is the primary runtime for the final project.

The pipeline is orchestrated through the Databricks notebook:

```text
notebooks/pipeline_notebook.py
```

The notebook executes the complete pipeline from raw input validation through Gold-layer analytics.

### 1. Databricks Git Folder

The final project is part of the Celebal Data Engineering Internship repository.

Navigate to:

```text
Final-Project/LearnTrack-LMS-Analytics-Pipeline/
```

Open:

```text
Final-Project/LearnTrack-LMS-Analytics-Pipeline/notebooks/pipeline_notebook.py
```

### 2. Compute

Use Databricks Serverless compute.

The pipeline does not override the Databricks Spark master. The shared Spark configuration helper only applies the local Spark master when running locally.

### 3. Unity Catalog Volume

The project uses the following Unity Catalog Volume:

```text
/Volumes/workspace/default/learntrack_lms
```

**Raw Input Files**

```text
/Volumes/workspace/default/learntrack_lms/learners.csv
/Volumes/workspace/default/learntrack_lms/courses.csv
/Volumes/workspace/default/learntrack_lms/enrolment_activity.csv
```

**Bronze Outputs**

```text
/Volumes/workspace/default/learntrack_lms/bronze/
├── learners_delta
├── courses_delta
└── enrolment_delta
```

**Silver Outputs**

```text
/Volumes/workspace/default/learntrack_lms/silver/
└── enrolments_enriched_delta
```

**SCD Type 2 Output**

```text
/Volumes/workspace/default/learntrack_lms/scd/
└── instructors_history_delta
```

**Gold Outputs**

```text
/Volumes/workspace/default/learntrack_lms/gold/
├── course_completion_delta
├── learner_engagement_delta
├── instructor_performance_delta
├── assessment_performance_delta
├── dropout_delta
└── re_enrolments_delta
```

### 4. Pipeline Execution Order

Run all notebook cells from top to bottom.

The notebook performs the following steps:

1. Repository and configuration discovery
2. Databricks profile loading
3. Raw input validation
4. Bronze ingestion
5. Bronze data validation
6. Silver transformation and enrichment
7. SCD Type 2 instructor history processing
8. Gold analytics generation
9. Final row-count validation
10. Representative Gold result previews
11. Gold schema validation

The complete flow is:

```text
Raw CSV
   │
   ▼
Bronze Delta
   │
   ▼
Bronze Validation
   │
   ▼
Silver Delta
   │
   ▼
SCD Type 2
   │
   ▼
Gold Delta
   │
   ▼
SQL Analytics
```

---

## Medallion Architecture

### Bronze Layer

The Bronze layer ingests the raw CSV files into Delta format.

Outputs:

- `learners_delta`
- `courses_delta`
- `enrolment_delta`

The Bronze layer preserves the source data in a structured Delta representation.

### Silver Layer

The Silver layer performs data cleaning, deduplication, enrichment, and business-rule preparation.

Key operations include:

- Duplicate enrolment removal
- Instructor-name resolution
- Data enrichment
- Learning-duration calculation
- Latest enrolment identification
- Data-quality validation

The resulting dataset is stored as:

```text
enrolments_enriched_delta
```

### SCD Type 2 Layer

Instructor history is maintained using Slowly Changing Dimension Type 2 logic.

| Attribute | Value |
|---|---|
| Business Key | `instructor_id` |
| Tracked Attribute | `instructor_name` |
| SCD Columns | `start_date`, `end_date`, `current_flag` |

When an instructor's tracked attribute changes:

1. The previous current record is closed.
2. `end_date` is populated.
3. `current_flag` becomes `False`.
4. A new version is inserted.
5. The new version becomes the current record.

New instructors are inserted as current records.

### Gold Layer

The Gold layer contains analytics-ready Delta tables designed for business analysis.

It includes:

- Course completion
- Learner engagement
- Instructor performance
- Assessment performance
- Dropout detection
- Re-enrolment analysis

---

## Business Rules

### Course Completion

Course completion uses the latest enrolment for each learner/course combination.

This prevents multiple enrolments or re-enrolments from causing double counting in completion calculations.

### Learner Engagement

Learner engagement is classified using the configured inactivity threshold.

| Status | Condition |
|---|---|
| No Activity | The learner has no recorded last activity date. |
| Active | The learner's inactivity period is within the configured threshold. |
| Disengaged | The learner's inactivity period exceeds the configured threshold. |

The threshold is configured in:

```yaml
thresholds:
  inactivity_days: 14
```

### Assessment Performance

Assessment performance includes:

- Attempted count
- Pass count
- Pass rate
- Average score

`attempted_count` counts non-null assessment scores.

Missing assessment scores are treated as missing values rather than automatically being classified as failed attempts.

The pass threshold is configurable through:

```yaml
thresholds:
  pass_score: 50.0
```

### Dropout Detection

Dropout analysis uses the latest enrolment state and identifies learners whose latest enrolment status is:

```text
Dropped
```

These records are combined with learner engagement information to support dropout analysis.

### Re-enrolment Detection

Re-enrolment analysis uses window functions to identify multiple enrolments for the same learner/course context.

The pipeline calculates:

- Enrolment count
- Enrolment rank
- Previous enrolment information
- Re-enrolment flag

---

## SQL Analytics

Analytics queries are available in:

```text
sql/analytics_queries.sql
```

The queries target the Gold Delta tables stored in the Unity Catalog Volume.

The SQL analysis uses concepts including:

- Common Table Expressions (CTEs)
- Aggregations
- JOIN operations
- Window functions
- Ranking
- Business-oriented analytics

---

## Configuration

Pipeline configuration is maintained in:

```text
config.yml
```

The configuration supports both local and Databricks execution profiles.

**Local Paths**

```yaml
paths:
  raw_dir: data/raw
  bronze_dir: data/bronze
  silver_dir: data/silver
  gold_dir: data/gold
  scd_dir: data/scd
```

**Databricks Paths**

```yaml
profiles:
  databricks:
    paths:
      raw_dir: /Volumes/workspace/default/learntrack_lms
      bronze_dir: /Volumes/workspace/default/learntrack_lms/bronze
      silver_dir: /Volumes/workspace/default/learntrack_lms/silver
      gold_dir: /Volumes/workspace/default/learntrack_lms/gold
      scd_dir: /Volumes/workspace/default/learntrack_lms/scd
```

The profile system allows the same pipeline code to be used in different execution environments without changing the business logic.

---

## Local Development

Local execution is supported through the default configuration.

Run the pipeline stages individually:

```bash
python src/bronze.py --config config.yml
python src/validate.py --config config.yml
python src/silver.py --config config.yml
python src/scd_instructor.py --config config.yml
python src/gold.py --config config.yml
```

Databricks-style paths can also be selected through the profile option:

```bash
python src/bronze.py --config config.yml --profile databricks
```

The final production-style validation and execution were performed using Databricks Serverless.

---

## Validation and Testing

The repository contains multiple validation mechanisms.

### Bronze Validation

```text
src/validate.py
```

Validates Bronze-layer:

- Row counts
- Duplicate enrolment IDs
- Null and blank values
- Course data quality
- Enrolment data quality

### Transformation Tests

```text
tests/test_pipeline.py
```

Tests include assertions for:

- Duplicate removal
- Learning-duration calculation
- Instructor-name resolution
- Engagement classification
- Dropout detection
- Re-enrolment detection
- Assessment pass-rate logic

### Validation Report

Initial source-data validation results are documented in:

```text
docs/validation_report.md
```

Initial source validation identified:

- 500 learners
- 60 courses
- 2,000 enrolment rows
- 10 duplicated enrolment IDs
- 6 blank course instructor names
- 330 blank last-activity dates
- 1,179 blank assessment scores

These conditions are handled by the pipeline's validation, cleaning, enrichment, and transformation logic.

### Final Databricks Validation

The complete pipeline was successfully executed on Databricks Serverless.

The final runtime validation confirmed:

| Output | Records |
|---|---|
| Learners | 500 |
| Courses | 60 |
| Bronze enrolments | 2,000 |
| Silver enrolments | 1,990 |
| SCD Type 2 instructor records | 14 |
| Course completion | 60 |
| Learner engagement | 495 |
| Instructor performance | 14 |
| Assessment performance | 60 |
| Dropout | 393 |
| Re-enrolment | 1,990 |

Additional validation confirmed:

- 0 unresolved instructor names
- Bronze duplicate detection working correctly
- Silver deduplication working correctly
- SCD Type 2 history maintained correctly
- Gold Delta tables successfully created
- Gold Delta tables successfully queried
- Gold schemas successfully validated
- Representative Gold analytics successfully displayed

The pipeline was successfully executed in the following order:

```text
Raw → Bronze → Validation → Silver → SCD Type 2 → Gold → Final Validation
```

A subsequent rerun with the same source data also confirmed that the SCD Type 2 process detected:

- 0 changed instructors
- 0 new instructors

This confirms that the pipeline does not create unnecessary SCD versions when no tracked instructor attributes have changed.

---

## Project Status

The LearnTrack LMS Analytics Pipeline is **completed and validated**.

The final implementation includes:

- End-to-end Medallion Architecture
- Delta Lake Bronze, Silver, and Gold layers
- Data-quality validation
- Silver-layer transformations and enrichment
- SCD Type 2 instructor history
- Learner engagement analytics
- Course completion analytics
- Instructor performance analytics
- Assessment analytics
- Dropout detection
- Re-enrolment detection
- SQL analytics queries
- Configurable execution profiles
- Databricks Serverless notebook orchestration
- Unity Catalog Volume storage
- Transformation tests
- Documentation and validation reports

The final project is maintained under:

```text
celebal-data-engineering-internship/
└── Final-Project/
    └── LearnTrack-LMS-Analytics-Pipeline/
```

---

## Author

**Aditya Mallick**
Celebal Technologies Data Engineering Internship (CEI 2026)
