# Databricks notebook source
# LearnTrack LMS Analytics Pipeline
# Execute all cells from top to bottom on Databricks Serverless.

# COMMAND ----------
# 1. Locate repository and load the Databricks profile
import os
import sys
from pathlib import Path
import yaml

from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()

def find_repo_root():
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "config.yml").exists() and (candidate / "src").is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not locate the LearnTrack repository root containing config.yml and src/."
    )

REPO_ROOT = find_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONFIG_PATH = str(REPO_ROOT / "config.yml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    base_cfg = yaml.safe_load(f)

cfg = dict(base_cfg)
cfg["paths"] = {
    **base_cfg["paths"],
    **base_cfg["profiles"]["databricks"]["paths"],
}

print("Repository:", REPO_ROOT)
print("Raw:", cfg["paths"]["raw_dir"])
print("Bronze:", cfg["paths"]["bronze_dir"])
print("Silver:", cfg["paths"]["silver_dir"])
print("SCD:", cfg["paths"]["scd_dir"])
print("Gold:", cfg["paths"]["gold_dir"])

# COMMAND ----------
# 2. Validate raw input files
from pathlib import Path

required_files = [
    cfg["files"]["learners"],
    cfg["files"]["courses"],
    cfg["files"]["enrolment_activity"],
]

for filename in required_files:
    path = Path(cfg["paths"]["raw_dir"]) / filename
    print(f"{filename}: {'FOUND' if path.exists() else 'MISSING'}")
    if not path.exists():
        raise FileNotFoundError(f"Missing raw input: {path}")

# COMMAND ----------
# 3. Bronze ingestion
from src.bronze import main as run_bronze

run_bronze(CONFIG_PATH, profile="databricks", stop_spark=False)

# COMMAND ----------
# 4. Bronze validation
from src.validate import main as run_validate

run_validate(CONFIG_PATH, profile="databricks", stop_spark=False)

# COMMAND ----------
# 5. Silver transformation
from src.silver import main as run_silver

run_silver(CONFIG_PATH, profile="databricks", stop_spark=False)

# COMMAND ----------
# 6. SCD Type 2 instructor history
from src.scd_instructor import main as run_scd

run_scd(CONFIG_PATH, profile="databricks", stop_spark=False)

# COMMAND ----------
# 7. Gold analytics
from src.gold import main as run_gold

run_gold(CONFIG_PATH, profile="databricks", stop_spark=False)

# COMMAND ----------
# 8. Final validation and row counts
import os

output_paths = {
    "bronze_learners": os.path.join(cfg["paths"]["bronze_dir"], "learners_delta"),
    "bronze_courses": os.path.join(cfg["paths"]["bronze_dir"], "courses_delta"),
    "bronze_enrolments": os.path.join(cfg["paths"]["bronze_dir"], "enrolment_delta"),
    "silver_enrolments": os.path.join(cfg["paths"]["silver_dir"], "enrolments_enriched_delta"),
    "scd_instructors": os.path.join(cfg["paths"]["scd_dir"], "instructors_history_delta"),
    "gold_course_completion": os.path.join(cfg["paths"]["gold_dir"], "course_completion_delta"),
    "gold_learner_engagement": os.path.join(cfg["paths"]["gold_dir"], "learner_engagement_delta"),
    "gold_instructor_performance": os.path.join(cfg["paths"]["gold_dir"], "instructor_performance_delta"),
    "gold_assessment_performance": os.path.join(cfg["paths"]["gold_dir"], "assessment_performance_delta"),
    "gold_dropout": os.path.join(cfg["paths"]["gold_dir"], "dropout_delta"),
    "gold_reenrolment": os.path.join(cfg["paths"]["gold_dir"], "re_enrolments_delta"),
}

for name, path in output_paths.items():
    count = spark.read.format("delta").load(path).count()
    print(f"{name}: {count}")

# COMMAND ----------
# 9. Representative Gold results
print("Top courses by completion rate")
spark.read.format("delta").load(
    output_paths["gold_course_completion"]
).orderBy("completion_rate", ascending=False).show(10, truncate=False)

print("Instructor performance")
spark.read.format("delta").load(
    output_paths["gold_instructor_performance"]
).orderBy("rank").show(10, truncate=False)

print("Assessment performance")
spark.read.format("delta").load(
    output_paths["gold_assessment_performance"]
).orderBy("avg_score").show(10, truncate=False)

print("Disengaged learners")
spark.read.format("delta").load(
    output_paths["gold_learner_engagement"]
).filter("engagement_status = 'Disengaged'").show(10, truncate=False)

# COMMAND ----------
# 10. Final schema check
for name in [
    "gold_course_completion",
    "gold_learner_engagement",
    "gold_instructor_performance",
    "gold_assessment_performance",
    "gold_dropout",
    "gold_reenrolment",
]:
    df = spark.read.format("delta").load(output_paths[name])
    print(f"\n{name} columns:")
    print(df.columns)

print("\nLearnTrack pipeline execution completed successfully.")
