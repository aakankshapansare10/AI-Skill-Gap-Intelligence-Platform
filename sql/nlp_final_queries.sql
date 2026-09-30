-- ============================================
-- AI SKILL GAPS INTELLIGENCE PLATFORM
-- MEMBER 2 - NLP FINAL QUERIES
-- ============================================

-- 1. Check final job_skills statistics
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT job_id) AS unique_jobs,
    COUNT(DISTINCT skill_id) AS unique_skills
FROM job_skills;

-- 2. Check for duplicate job-skill pairs
SELECT COUNT(*) AS duplicate_pairs
FROM (
    SELECT
        job_id,
        skill_id,
        COUNT(*)
    FROM job_skills
    GROUP BY job_id, skill_id
    HAVING COUNT(*) > 1
) x;

-- 3. Check for invalid job IDs
SELECT COUNT(*) AS invalid_job_ids
FROM job_skills js
LEFT JOIN jobs j
    ON js.job_id = j.job_id
WHERE j.job_id IS NULL;

-- 4. Check for invalid skill IDs
SELECT COUNT(*) AS invalid_skill_ids
FROM job_skills js
LEFT JOIN skills s
    ON js.skill_id = s.skill_id
WHERE s.skill_id IS NULL;

-- 5. Check jobs with no extracted skills
SELECT COUNT(*) AS jobs_without_skills
FROM jobs j
LEFT JOIN job_skills js
    ON j.job_id = js.job_id
WHERE js.job_id IS NULL;

-- 6. Skill distribution per job
SELECT
    MIN(skill_count) AS minimum_skills,
    MAX(skill_count) AS maximum_skills,
    ROUND(AVG(skill_count), 2) AS average_skills,
    PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY skill_count) AS median_skills
FROM (
    SELECT
        job_id,
        COUNT(*) AS skill_count
    FROM job_skills
    GROUP BY job_id
) x;

-- 7. Create ML-ready view
CREATE OR REPLACE VIEW ml_job_skills AS
SELECT
    j.job_id,
    j.title AS job_title,
    s.skill_id,
    s.skill_name
FROM job_skills js
JOIN jobs j
    ON js.job_id = j.job_id
JOIN skills s
    ON js.skill_id = s.skill_id;

-- 8. Verify ML-ready view
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT job_id) AS unique_jobs,
    COUNT(DISTINCT skill_id) AS unique_skills
FROM ml_job_skills;

-- 9. Preview ML-ready data
SELECT *
FROM ml_job_skills
ORDER BY job_id
LIMIT 20;