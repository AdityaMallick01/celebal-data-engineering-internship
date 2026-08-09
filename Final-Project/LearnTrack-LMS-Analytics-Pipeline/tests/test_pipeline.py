import pytest

try:
    from pyspark.sql import SparkSession
    import pyspark.sql.functions as F
    from pyspark.sql.functions import col
except Exception as e:
    pytest.skip(
        f"Skipping tests: pyspark import failed ({e}). "
        "Run tests in Databricks with pyspark+delta-spark.",
        allow_module_level=True
    )


@pytest.fixture(scope="module")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("TestLearnTrack")
        .getOrCreate()
    )
    yield spark
    spark.stop()


def test_duplicate_removal_logic(spark):
    # Small example to test dedup logic used in silver.py.
    df = spark.createDataFrame(
        [
            ("ENR1", "LRN1", "CRS1", "2024-01-01"),
            ("ENR1", "LRN1", "CRS1", "2024-01-02"),
            ("ENR2", "LRN2", "CRS2", "2024-01-05"),
        ],
        schema=["enrolment_id", "learner_id", "course_id", "enrol_date"],
    )

    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number

    w = Window.partitionBy("enrolment_id").orderBy(
        col("enrol_date").desc()
    )

    dedup = (
        df.withColumn("rn", row_number().over(w))
        .filter(col("rn") == 1)
    )

    ids = [
        r["enrolment_id"]
        for r in dedup.select("enrolment_id").collect()
    ]

    assert set(ids) == {"ENR1", "ENR2"}
    assert dedup.count() == 2


def test_learning_duration_calc(spark):
    df = spark.createDataFrame(
        [
            ("ENR1", "2024-01-01", "2024-01-10"),
            ("ENR2", "2024-01-05", None),
        ],
        schema=[
            "enrolment_id",
            "enrol_date",
            "actual_completion_date",
        ],
    )

    from pyspark.sql.functions import to_date, datediff, when

    df2 = (
        df
        .withColumn("enrol_date", to_date(col("enrol_date")))
        .withColumn(
            "actual_completion_date",
            to_date(col("actual_completion_date")),
        )
    )

    df3 = df2.withColumn(
        "learning_duration",
        when(
            col("actual_completion_date").isNotNull(),
            datediff(
                col("actual_completion_date"),
                col("enrol_date"),
            ),
        ).otherwise(None),
    )

    rows = {
        r["enrolment_id"]: r["learning_duration"]
        for r in df3.select(
            "enrolment_id",
            "learning_duration",
        ).collect()
    }

    assert rows["ENR1"] == 9
    assert rows["ENR2"] is None


def test_instructor_name_resolution(spark):
    from pyspark.sql.functions import when, first

    courses = spark.createDataFrame(
        [
            ("C1", "I1", "Alice"),
            ("C2", "I1", None),
            ("C3", "I2", None),
        ],
        schema=[
            "course_id",
            "instructor_id",
            "instructor_name",
        ],
    )

    instr_lookup = (
        courses
        .filter(
            col("instructor_name").isNotNull()
            & (col("instructor_name") != "")
        )
        .groupBy("instructor_id")
        .agg(
            first("instructor_name").alias(
                "resolved_instructor_name"
            )
        )
    )

    courses_joined = courses.join(
        instr_lookup,
        on="instructor_id",
        how="left",
    )

    courses_resolved = (
        courses_joined
        .withColumn(
            "instructor_name",
            when(
                col("instructor_name").isNull()
                | (col("instructor_name") == ""),
                col("resolved_instructor_name"),
            ).otherwise(col("instructor_name")),
        )
        .drop("resolved_instructor_name")
    )

    vals = {
        r["course_id"]: r["instructor_name"]
        for r in courses_resolved.select(
            "course_id",
            "instructor_name",
        ).collect()
    }

    assert vals["C1"] == "Alice"
    assert vals["C2"] == "Alice"
    assert vals["C3"] is None


def test_engagement_classification_logic(spark):
    from pyspark.sql.functions import current_date, datediff

    data = [
        ("L1", 7, 80.0),       # Active: 7 days ago
        ("L2", 30, 20.0),      # Disengaged: 30 days ago
        ("L3", None, 0.0),     # No Activity
    ]

    df = spark.createDataFrame(
        data,
        schema=[
            "learner_id",
            "days_ago",
            "progress_pct",
        ],
    )

    df = df.withColumn(
        "last_activity_date",
        F.when(
            col("days_ago").isNotNull(),
            F.date_sub(current_date(), col("days_ago")),
        ),
    )

    agg = (
        df.groupBy("learner_id")
        .agg(
            F.max(col("last_activity_date")).alias(
                "last_activity_date"
            ),
            F.round(
                F.avg(col("progress_pct")),
                2,
            ).alias("avg_progress_pct"),
        )
    )

    inactivity_days = 14

    agg = agg.withColumn(
        "days_since_last_activity",
        F.when(
            col("last_activity_date").isNotNull(),
            datediff(
                current_date(),
                col("last_activity_date"),
            ),
        ).otherwise(None),
    )

    agg = agg.withColumn(
        "engagement_status",
        F.when(
            col("last_activity_date").isNull(),
            F.lit("No Activity"),
        )
        .when(
            col("days_since_last_activity")
            <= inactivity_days,
            F.lit("Active"),
        )
        .otherwise(F.lit("Disengaged")),
    )

    res = {
        r["learner_id"]: r["engagement_status"]
        for r in agg.select(
            "learner_id",
            "engagement_status",
        ).collect()
    }

    assert res["L1"] == "Active"
    assert res["L2"] == "Disengaged"
    assert res["L3"] == "No Activity"


def test_dropout_and_reenrolment_logic(spark):
    from pyspark.sql.functions import row_number
    from pyspark.sql.window import Window

    enrol = spark.createDataFrame(
        [
            (
                "E1",
                "L1",
                "C1",
                "2024-01-01",
                "Dropped",
                1,
            ),
            (
                "E2",
                "L1",
                "C1",
                "2024-02-01",
                "Completed",
                1,
            ),
            (
                "E3",
                "L2",
                "C2",
                "2024-03-01",
                "Dropped",
                1,
            ),
        ],
        schema=[
            "enrolment_id",
            "learner_id",
            "course_id",
            "enrol_date",
            "status",
            "attempts",
        ],
    )

    w = Window.partitionBy(
        "learner_id",
        "course_id",
    ).orderBy(
        col("enrol_date").desc()
    )

    ew = (
        enrol
        .withColumn(
            "enrol_rank",
            row_number().over(w),
        )
        .withColumn(
            "enrol_count",
            F.count("enrolment_id").over(
                Window.partitionBy(
                    "learner_id",
                    "course_id",
                )
            ),
        )
    )

    re_enrol = ew.withColumn(
        "re_enrolment_flag",
        F.when(
            col("enrol_count") > 1,
            F.lit(True),
        ).otherwise(F.lit(False)),
    )

    flags = {
        r["enrolment_id"]: r["re_enrolment_flag"]
        for r in re_enrol.select(
            "enrolment_id",
            "re_enrolment_flag",
        ).collect()
    }

    assert flags["E1"] is True
    assert flags["E2"] is True
    assert flags["E3"] is False

    # Dropout on latest enrolments.
    latest = ew.filter(
        col("enrol_rank") == 1
    )

    drops = [
        r["enrolment_id"]
        for r in latest
        .filter(col("status") == "Dropped")
        .select("enrolment_id")
        .collect()
    ]

    assert "E3" in drops


def test_assessment_performance_logic(spark):
    df = spark.createDataFrame(
        [
            ("E1", "C1", 85.0),
            ("E2", "C1", 55.0),
            ("E3", "C1", None),
            ("E4", "C2", 70.0),
        ],
        schema=[
            "enrolment_id",
            "course_id",
            "assessment_score",
        ],
    )

    # Use the configured production threshold.
    pass_score = 50.0

    ap = df.groupBy("course_id").agg(
        F.round(
            F.avg(col("assessment_score")),
            2,
        ).alias("avg_score"),
        F.count(
            col("assessment_score")
        ).alias("attempted_count"),
        F.sum(
            F.when(
                col("assessment_score") >= pass_score,
                1,
            ).otherwise(0)
        ).alias("pass_count"),
        F.sum(
            F.when(
                col("assessment_score").isNull(),
                1,
            ).otherwise(0)
        ).alias("missing_scores"),
    )

    res = {
        r["course_id"]: (
            r["attempted_count"],
            r["pass_count"],
        )
        for r in ap.select(
            "course_id",
            "attempted_count",
            "pass_count",
        ).collect()
    }

    assert res["C1"][0] == 2
    assert res["C1"][1] == 2
    assert res["C2"][0] == 1
    assert res["C2"][1] == 1