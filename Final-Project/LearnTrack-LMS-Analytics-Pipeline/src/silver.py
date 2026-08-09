"""Silver transformations: clean, type, deduplicate, resolve instructors, enrich."""
import argparse
import os

from pyspark.sql.functions import (
    avg, col, datediff, first, lit, row_number, to_date, when
)
from pyspark.sql.window import Window

try:
    from src.config_utils import build_spark, load_config
except ImportError:
    from config_utils import build_spark, load_config


def main(config_path="config.yml", profile="local", stop_spark=True):
    cfg = load_config(config_path, profile)
    bronze = cfg["paths"]["bronze_dir"]
    silver = cfg["paths"]["silver_dir"]
    spark = build_spark(cfg, profile)

    learners = spark.read.format("delta").load(os.path.join(bronze, "learners_delta"))
    courses = spark.read.format("delta").load(os.path.join(bronze, "courses_delta"))
    enrol = spark.read.format("delta").load(os.path.join(bronze, "enrolment_delta"))

    enrol_clean = (
        enrol
        .withColumn("enrol_date", to_date(col("enrol_date"), "yyyy-MM-dd"))
        .withColumn("expected_completion_date", to_date(col("expected_completion_date"), "yyyy-MM-dd"))
        .withColumn("actual_completion_date", to_date(col("actual_completion_date"), "yyyy-MM-dd"))
        .withColumn("last_activity_date", to_date(col("last_activity_date"), "yyyy-MM-dd"))
        .withColumn("progress_pct", col("progress_pct").cast("double"))
        .withColumn("assessment_score", col("assessment_score").cast("double"))
        .withColumn("attempts", col("attempts").cast("int"))
        .withColumn("feedback_rating", col("feedback_rating").cast("double"))
    )

    # Keep the latest record when the same enrolment_id occurs more than once.
    w = Window.partitionBy("enrolment_id").orderBy(col("enrol_date").desc_nulls_last())
    enrol_dedup = (
        enrol_clean.withColumn("rn", row_number().over(w))
        .filter(col("rn") == 1)
        .drop("rn")
    )

    # Resolve blank instructor names from another course sharing the same instructor_id.
    instr_lookup = (
        courses
        .filter(col("instructor_name").isNotNull() & (col("instructor_name") != ""))
        .groupBy("instructor_id")
        .agg(first("instructor_name", ignorenulls=True).alias("resolved_instructor_name"))
    )

    courses_resolved = (
        courses.join(instr_lookup, "instructor_id", "left")
        .withColumn(
            "instructor_name",
            when(
                col("instructor_name").isNull() | (col("instructor_name") == ""),
                col("resolved_instructor_name"),
            ).otherwise(col("instructor_name")),
        )
        .drop("resolved_instructor_name")
    )

    enriched = (
        enrol_dedup
        .join(learners, "learner_id", "left")
        .join(courses_resolved, "course_id", "left")
        .withColumn(
            "learning_duration_days",
            when(
                col("actual_completion_date").isNotNull(),
                datediff(col("actual_completion_date"), col("enrol_date")),
            ),
        )
    )

    # Latest enrolment for each learner/course is used by Gold completion/dropout metrics.
    w2 = Window.partitionBy("learner_id", "course_id").orderBy(
        col("enrol_date").desc_nulls_last()
    )
    enriched = (
        enriched.withColumn("enrol_row_number", row_number().over(w2))
        .withColumn("is_latest_enrolment", col("enrol_row_number") == 1)
    )

    output_path = os.path.join(silver, "enrolments_enriched_delta")
    enriched.write.format("delta").mode("overwrite").option("path", output_path).save()

    print("Silver validation summary:")
    print(" raw enrolment rows:", enrol.count())
    print(" deduplicated rows:", enrol_dedup.count())
    print(" enriched rows:", enriched.count())
    print(
        " unresolved instructor names:",
        courses_resolved.filter(col("instructor_name").isNull() | (col("instructor_name") == "")).count(),
    )
    print(
        " null last activity:",
        enriched.filter(col("last_activity_date").isNull()).count(),
    )

    if stop_spark:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--profile", default="local", choices=["local", "databricks"])
    args = parser.parse_args()
    main(args.config, args.profile)
