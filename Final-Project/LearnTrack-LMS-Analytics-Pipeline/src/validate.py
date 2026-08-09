"""Validation for Bronze datasets."""
import argparse
import os

from pyspark.sql.functions import col

try:
    from src.config_utils import build_spark, load_config
except ImportError:
    from config_utils import build_spark, load_config


def col_null_stats(df):
    stats = {}
    for c in df.columns:
        stats[c] = df.filter(col(c).isNull() | (col(c) == "")).count()
    return stats


def main(config_path="config.yml", profile="local", stop_spark=True):
    cfg = load_config(config_path, profile)
    bronze = cfg["paths"]["bronze_dir"]
    spark = build_spark(cfg, profile)

    learners = spark.read.format("delta").load(os.path.join(bronze, "learners_delta"))
    courses = spark.read.format("delta").load(os.path.join(bronze, "courses_delta"))
    enrol = spark.read.format("delta").load(os.path.join(bronze, "enrolment_delta"))

    print("Bronze validation summary:")
    print(" learners:", learners.count())
    print(" courses:", courses.count())
    print(" enrolments:", enrol.count())

    dup_count = (
        enrol.groupBy("enrolment_id")
        .count()
        .filter(col("count") > 1)
        .count()
    )
    print(" duplicate enrolment_id count:", dup_count)

    print(" course null/blank counts:", col_null_stats(courses))

    for c in ["actual_completion_date", "assessment_score", "last_activity_date", "feedback_rating"]:
        print(f" enrolment {c} null/blank:", enrol.filter(col(c).isNull() | (col(c) == "")).count())

    if stop_spark:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--profile", default="local", choices=["local", "databricks"])
    args = parser.parse_args()
    main(args.config, args.profile)
