"""Gold aggregations and business analytics."""
import argparse
import os

from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql.window import Window

try:
    from src.config_utils import build_spark, load_config
except ImportError:
    from config_utils import build_spark, load_config


def main(config_path="config.yml", profile="local", stop_spark=True):
    cfg = load_config(config_path, profile)
    silver = cfg["paths"]["silver_dir"]
    gold = cfg["paths"]["gold_dir"]
    thresholds = cfg["thresholds"]
    spark = build_spark(cfg, profile)

    enrol = spark.read.format("delta").load(
        os.path.join(silver, "enrolments_enriched_delta")
    )

    latest = enrol.filter(col("is_latest_enrolment") == True)

    # 1. Course completion
    course_metrics = latest.groupBy(
        "course_id", "course_title", "category", "difficulty_level"
    ).agg(
        F.countDistinct("learner_id").alias("enrolled_learners"),
        F.sum(F.when(col("status") == "Completed", 1).otherwise(0)).alias(
            "completed_learners"
        ),
    )

    course_metrics = (
        course_metrics.withColumn(
            "completion_rate",
            F.when(
                col("enrolled_learners") > 0,
                F.round(
                    col("completed_learners") / col("enrolled_learners"), 4
                ),
            ),
        )
        .withColumn(
            "completion_class",
            F.when(
                col("completion_rate") >= thresholds["completion_high"],
                "High Completion",
            )
            .when(
                col("completion_rate") >= thresholds["completion_moderate"],
                "Moderate",
            )
            .otherwise("At Risk"),
        )
    )

    course_metrics.write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "course_completion_delta")
    ).save()

    # 2. Learner engagement
    learner_engagement = enrol.groupBy(
        "learner_id", "learner_name", "email"
    ).agg(
        F.max("last_activity_date").alias("last_activity_date"),
        F.round(F.avg("progress_pct"), 2).alias("avg_progress_pct"),
        F.count("course_id").alias("active_enrolments"),
    )

    inactivity_days = int(thresholds.get("inactivity_days", 14))
    learner_engagement = (
        learner_engagement.withColumn(
            "days_since_last_activity",
            F.when(
                col("last_activity_date").isNotNull(),
                F.datediff(F.current_date(), col("last_activity_date")),
            ),
        )
        .withColumn(
            "engagement_status",
            F.when(
                col("last_activity_date").isNull(), "No Activity"
            )
            .when(
                col("days_since_last_activity") <= inactivity_days, "Active"
            )
            .otherwise("Disengaged"),
        )
    )

    learner_engagement.write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "learner_engagement_delta")
    ).save()

    # 3. Instructor performance
    instructor_metrics = latest.groupBy(
        "instructor_id", "instructor_name"
    ).agg(
        F.countDistinct("learner_id").alias("learners_taught"),
        F.count("enrolment_id").alias("enrolment_count"),
        F.sum(F.when(col("status") == "Completed", 1).otherwise(0)).alias(
            "completed_count"
        ),
        F.round(F.avg("assessment_score"), 2).alias("avg_assessment_score"),
    )

    instructor_metrics = instructor_metrics.withColumn(
        "completion_rate",
        F.when(
            col("learners_taught") > 0,
            F.round(col("completed_count") / col("learners_taught"), 4),
        ),
    )

    rank_window = Window.orderBy(col("completion_rate").desc_nulls_last())
    instructor_metrics = instructor_metrics.withColumn(
        "rank", F.dense_rank().over(rank_window)
    )

    instructor_metrics.write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "instructor_performance_delta")
    ).save()

    # 4. Assessment performance
    assessment_perf = enrol.groupBy("course_id", "course_title").agg(
        F.round(F.avg("assessment_score"), 2).alias("avg_score"),
        F.count("assessment_score").alias("attempted_count"),
        F.sum(
            F.when(
                col("assessment_score") >= thresholds["pass_score"], 1
            ).otherwise(0)
        ).alias("pass_count"),
        F.sum(
            F.when(col("assessment_score").isNull(), 1).otherwise(0)
        ).alias("missing_scores"),
    )

    assessment_perf = assessment_perf.withColumn(
        "pass_rate",
        F.when(
            col("attempted_count") > 0,
            F.round(col("pass_count") / col("attempted_count"), 4),
        ),
    )

    assessment_perf.write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "assessment_performance_delta")
    ).save()

    # 5. Dropout detection
    dropout = latest.filter(col("status") == "Dropped").join(
        learner_engagement.select(
            "learner_id", "engagement_status", "days_since_last_activity"
        ),
        "learner_id",
        "left",
    )

    dropout.write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "dropout_delta")
    ).save()

    # 6. Re-enrolment detection
    re_window = Window.partitionBy("learner_id", "course_id").orderBy(
        col("enrol_date").desc_nulls_last()
    )
    count_window = Window.partitionBy("learner_id", "course_id")

    re_enrol = (
        enrol.withColumn("enrol_rank", F.row_number().over(re_window))
        .withColumn("enrol_count", F.count("enrolment_id").over(count_window))
        .withColumn(
            "re_enrolment_flag", col("enrol_count") > 1
        )
        .withColumn(
            "prev_enrolment_id",
            F.lag("enrolment_id").over(re_window),
        )
        .withColumn(
            "prev_enrol_date",
            F.lag("enrol_date").over(re_window),
        )
        .withColumn(
            "prev_status",
            F.lag("status").over(re_window),
        )
    )

    re_enrol.select(
        "enrolment_id",
        "learner_id",
        "learner_name",
        "course_id",
        "course_title",
        "enrol_date",
        "status",
        "attempts",
        "re_enrolment_flag",
        "enrol_count",
        "prev_enrolment_id",
        "prev_enrol_date",
        "prev_status",
    ).write.format("delta").mode("overwrite").option(
        "path", os.path.join(gold, "re_enrolments_delta")
    ).save()

    print("Gold tables written:")
    for table in [
        "course_completion_delta",
        "learner_engagement_delta",
        "instructor_performance_delta",
        "assessment_performance_delta",
        "dropout_delta",
        "re_enrolments_delta",
    ]:
        print(" -", table)

    if stop_spark:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--profile", default="local", choices=["local", "databricks"])
    args = parser.parse_args()
    main(args.config, args.profile)
