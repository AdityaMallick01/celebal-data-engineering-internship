-- LearnTrack LMS Analytics - Gold layer queries
-- Databricks Serverless / Unity Catalog Volume paths

-- 1) Top courses by completion rate
WITH cm AS (
    SELECT
        course_id,
        course_title,
        category,
        difficulty_level,
        enrolled_learners,
        completed_learners,
        completion_rate,
        completion_class
    FROM delta.`/Volumes/workspace/default/learntrack_lms/gold/course_completion_delta`
)
SELECT *
FROM cm
ORDER BY completion_rate DESC
LIMIT 20;

-- 2) Instructor ranking
SELECT
    instructor_id,
    instructor_name,
    learners_taught,
    enrolment_count,
    completed_count,
    avg_assessment_score,
    completion_rate,
    rank
FROM delta.`/Volumes/workspace/default/learntrack_lms/gold/instructor_performance_delta`
ORDER BY rank, instructor_name
LIMIT 50;

-- 3) Learners currently classified as disengaged
SELECT
    learner_id,
    learner_name,
    email,
    last_activity_date,
    days_since_last_activity,
    avg_progress_pct,
    active_enrolments,
    engagement_status
FROM delta.`/Volumes/workspace/default/learntrack_lms/gold/learner_engagement_delta`
WHERE engagement_status = 'Disengaged'
ORDER BY days_since_last_activity DESC;

-- 4) Re-enrolment detection
SELECT
    enrolment_id,
    learner_id,
    learner_name,
    course_id,
    course_title,
    enrol_date,
    status,
    enrol_count,
    re_enrolment_flag,
    prev_enrolment_id,
    prev_enrol_date,
    prev_status
FROM delta.`/Volumes/workspace/default/learntrack_lms/gold/re_enrolments_delta`
WHERE re_enrolment_flag = true
ORDER BY learner_id, course_id, enrol_date DESC;

-- 5) Assessment performance by course
SELECT
    course_id,
    course_title,
    avg_score,
    attempted_count,
    pass_count,
    pass_rate,
    missing_scores
FROM delta.`/Volumes/workspace/default/learntrack_lms/gold/assessment_performance_delta`
ORDER BY avg_score ASC;
