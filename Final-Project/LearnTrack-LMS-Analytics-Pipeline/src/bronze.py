"""Bronze ingestion: read raw CSVs and write Delta tables."""
import argparse
import os

try:
    from src.config_utils import build_spark, load_config
except ImportError:
    from config_utils import build_spark, load_config


def read_csv_preserve(spark, path):
    return (
        spark.read.option("header", True)
        .option("inferSchema", False)
        .option("multiLine", False)
        .csv(path)
    )


def main(config_path="config.yml", profile="local", stop_spark=True):
    cfg = load_config(config_path, profile)
    raw = cfg["paths"]["raw_dir"]
    bronze = cfg["paths"]["bronze_dir"]
    spark = build_spark(cfg, profile)

    files = cfg["files"]

    sources = [
        ("learners", files["learners"], "learners_delta"),
        ("courses", files["courses"], "courses_delta"),
        ("enrolment_activity", files["enrolment_activity"], "enrolment_delta"),
    ]

    print(f"Bronze ingestion using profile: {profile}")
    for name, filename, table_name in sources:
        source_path = os.path.join(raw, filename)
        df = read_csv_preserve(spark, source_path)
        output_path = os.path.join(bronze, table_name)

        df.write.format("delta").mode("overwrite").option("path", output_path).save()

        written_count = spark.read.format("delta").load(output_path).count()
        print(f"  {name}: source={source_path} rows={written_count}")

    print("Bronze ingestion completed.")

    if stop_spark:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--profile", default="local", choices=["local", "databricks"])
    args = parser.parse_args()
    main(args.config, args.profile)
