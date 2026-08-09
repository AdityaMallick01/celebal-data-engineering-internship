"""Shared configuration and Spark helpers for the LearnTrack pipeline."""
from copy import deepcopy
import yaml
from pyspark.sql import SparkSession


def load_config(config_path="config.yml", profile="local"):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    cfg = deepcopy(cfg)
    if profile != "local":
        profiles = cfg.get("profiles", {})
        if profile not in profiles:
            raise ValueError(
                f"Unknown profile '{profile}'. Available profiles: {['local', *profiles.keys()]}"
            )
        cfg["paths"] = {
            **cfg.get("paths", {}),
            **profiles[profile].get("paths", {}),
        }
    return cfg


def build_spark(cfg, profile="local"):
    builder = SparkSession.builder.appName(cfg["spark"]["app_name"])

    # Databricks/Serverless owns the Spark session. Never override it with .master().
    if profile == "local":
        builder = builder.master(cfg["spark"]["master"])

    spark = builder.getOrCreate()
    spark.conf.set("spark.sql.shuffle.partitions", "4")
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    return spark
