# LearnTrack Medallion Architecture

## Bronze
Raw CSV ingestion. The original string values, duplicates, nulls, and source formatting are preserved in Delta tables.

## Silver
The pipeline:
- parses date columns
- casts numeric fields
- removes duplicate `enrolment_id` rows while keeping the latest enrolment-date record
- resolves blank instructor names using `instructor_id`
- joins learners, courses, and enrolments
- calculates `learning_duration_days`
- flags the latest enrolment per learner/course

## Gold
Business-focused Delta tables:
- course completion
- learner engagement
- instructor performance
- assessment performance
- dropout detection
- re-enrolment detection

## SCD Type 2
Instructor history is stored separately under the configured `scd_dir` using Delta `MERGE`.
The business key is `instructor_id`; the tracked attribute is `instructor_name`.
History columns are `start_date`, `end_date`, and `current_flag`.

## Databricks
Databricks Serverless is the primary execution environment. Raw inputs are stored in the Unity Catalog Volume:

`/Volumes/workspace/default/learntrack_lms`

The pipeline writes Bronze, Silver, SCD, and Gold Delta outputs below the same Volume.
