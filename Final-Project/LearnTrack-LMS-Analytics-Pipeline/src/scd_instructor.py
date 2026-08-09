"""SCD Type 2 instructor history using Delta MERGE.

Business key: instructor_id
Tracked attribute: instructor_name
"""
import argparse
import os

from delta.tables import DeltaTable
from pyspark.sql import functions as F

try:
    from src.config_utils import build_spark, load_config
except ImportError:
    from config_utils import build_spark, load_config


def main(config_path="config.yml", profile="local", stop_spark=True):
    cfg = load_config(config_path, profile)
    silver = cfg["paths"]["silver_dir"]
    scd_dir = cfg["paths"]["scd_dir"]
    spark = build_spark(cfg, profile)

    enriched = spark.read.format("delta").load(
        os.path.join(silver, "enrolments_enriched_delta")
    )

    # One current source row per instructor. Ignore unresolved instructor names.
    source = (
        enriched.filter(
            F.col("instructor_id").isNotNull()
            & F.col("instructor_name").isNotNull()
            & (F.col("instructor_name") != "")
        )
        .groupBy("instructor_id")
        .agg(F.first("instructor_name", ignorenulls=True).alias("instructor_name"))
        .withColumn("start_date", F.current_date())
        .withColumn("end_date", F.lit(None).cast("date"))
        .withColumn("current_flag", F.lit(True))
    )

    hist_path = os.path.join(scd_dir, "instructors_history_delta")

    if not DeltaTable.isDeltaTable(spark, hist_path):
        source.select(
            "instructor_id",
            "instructor_name",
            "start_date",
            "end_date",
            "current_flag",
        ).write.format("delta").mode("overwrite").option(
            "path", hist_path
        ).save()
        print("Initialized SCD Type 2 history:", hist_path)
    else:
        target = DeltaTable.forPath(spark, hist_path)
        current = target.toDF().filter(F.col("current_flag") == True).select(
            "instructor_id", "instructor_name"
        )

        changed = (
            source.alias("src")
            .join(current.alias("tgt"), "instructor_id", "inner")
            .filter(
                F.col("src.instructor_name") != F.col("tgt.instructor_name")
            )
            .select("src.*")
        )

        new_instructors = source.join(
            current.select("instructor_id"), "instructor_id", "left_anti"
        )

        changed_ids = [r["instructor_id"] for r in changed.select("instructor_id").collect()]
        new_ids = [r["instructor_id"] for r in new_instructors.select("instructor_id").collect()]

        if changed_ids:
            # MERGE row closes the old current version.
            close_rows = changed.withColumn("merge_key", F.col("instructor_id"))

            # A second copy with a NULL merge key forces insertion of the new version.
            insert_rows = changed.withColumn(
                "merge_key", F.lit(None).cast(source.schema["instructor_id"].dataType)
            )

            staged = close_rows.unionByName(insert_rows)

            (
                target.alias("tgt")
                .merge(
                    staged.alias("src"),
                    "tgt.instructor_id = src.merge_key AND tgt.current_flag = true",
                )
                .whenMatchedUpdate(
                    set={
                        "end_date": F.current_date(),
                        "current_flag": F.lit(False),
                    }
                )
                .whenNotMatchedInsert(
                    values={
                        "instructor_id": F.col("src.instructor_id"),
                        "instructor_name": F.col("src.instructor_name"),
                        "start_date": F.col("src.start_date"),
                        "end_date": F.col("src.end_date"),
                        "current_flag": F.col("src.current_flag"),
                    }
                )
                .execute()
            )

        if new_ids:
            # New instructors have no matching current row, so the MERGE inserts them.
            (
                target.alias("tgt")
                .merge(
                    new_instructors.alias("src"),
                    "tgt.instructor_id = src.instructor_id AND tgt.current_flag = true",
                )
                .whenNotMatchedInsert(
                    values={
                        "instructor_id": F.col("src.instructor_id"),
                        "instructor_name": F.col("src.instructor_name"),
                        "start_date": F.col("src.start_date"),
                        "end_date": F.col("src.end_date"),
                        "current_flag": F.col("src.current_flag"),
                    }
                )
                .execute()
            )

        print("SCD Type 2 validation:")
        print(" changed instructors:", len(changed_ids), changed_ids)
        print(" new instructors:", len(new_ids), new_ids)

    history = spark.read.format("delta").load(hist_path)
    print("SCD history rows:", history.count())
    print("Current instructor rows:", history.filter(F.col("current_flag") == True).count())

    if stop_spark:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--profile", default="local", choices=["local", "databricks"])
    args = parser.parse_args()
    main(args.config, args.profile)
