DROP TABLE IF EXISTS skill_demand_staging;

CREATE TABLE skill_demand_staging (
    skill_id BIGINT,
    total_jobs BIGINT,
    total_job_postings BIGINT,
    demand_percentage NUMERIC
);

SELECT COUNT(*) AS invalid_skill_ids
FROM skill_demand_staging s
LEFT JOIN skills sk
    ON s.skill_id = sk.skill_id
WHERE sk.skill_id IS NULL;

INSERT INTO skill_demand (
    skill_id,
    rank,
    job_count,
    demand_percentage
)
SELECT
    s.skill_id,
    ROW_NUMBER() OVER (
        ORDER BY s.total_jobs DESC
    ) AS rank,
    s.total_jobs AS job_count,
    s.demand_percentage
FROM skill_demand_staging s
INNER JOIN skills sk
    ON s.skill_id = sk.skill_id;

SELECT COUNT(*) AS total_skill_demand
FROM skill_demand;


DROP TABLE IF EXISTS domain_skill_demand_staging;

CREATE TABLE domain_skill_demand_staging (
    domain_id BIGINT,
    skill_id BIGINT,
    rank INTEGER,
    job_count BIGINT,
    total_jobs BIGINT,
    demand_percentage NUMERIC
);




SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE d.domain_id IS NULL
    ) AS invalid_domain_ids,

    COUNT(*) FILTER (
        WHERE sk.skill_id IS NULL
    ) AS invalid_skill_ids

FROM domain_skill_demand_staging s

LEFT JOIN domains d
    ON s.domain_id = d.domain_id

LEFT JOIN skills sk
    ON s.skill_id = sk.skill_id;
-------------

INSERT INTO domain_skill_demand (
    domain_id,
    skill_id,
    rank,
    job_count,
    total_jobs,
    demand_percentage
)
SELECT
    s.domain_id,
    s.skill_id,
    s.rank,
    s.job_count,
    s.total_jobs,
    s.demand_percentage
FROM domain_skill_demand_staging s
INNER JOIN domains d
    ON s.domain_id = d.domain_id
INNER JOIN skills sk
    ON s.skill_id = sk.skill_id;


INSERT INTO domain_skill_demand (
    domain_id,
    skill_id,
    rank,
    job_count,
    total_jobs,
    demand_percentage
)
WITH skill_counts AS (
    SELECT
        jd.domain_id,
        js.skill_id,
        COUNT(DISTINCT jd.job_id) AS job_count
    FROM job_domains jd
    JOIN job_skills js
        ON jd.job_id = js.job_id
    GROUP BY jd.domain_id, js.skill_id
),
domain_totals AS (
    SELECT
        domain_id,
        COUNT(DISTINCT job_id) AS total_jobs
    FROM job_domains
    GROUP BY domain_id
)
SELECT
    sc.domain_id,
    sc.skill_id,
    ROW_NUMBER() OVER (
        PARTITION BY sc.domain_id
        ORDER BY sc.job_count DESC
    ) AS rank,
    sc.job_count,
    dt.total_jobs,
    ROUND(
        100.0 * sc.job_count / NULLIF(dt.total_jobs, 0),
        2
    ) AS demand_percentage
FROM skill_counts sc
JOIN domain_totals dt
    ON sc.domain_id = dt.domain_id;






SELECT COUNT(*) AS total_domain_skill_demand
FROM domain_skill_demand;








SELECT
    'jobs' AS table_name,
    COUNT(*) AS row_count
FROM jobs

UNION ALL

SELECT
    'skills',
    COUNT(*)
FROM skills

UNION ALL

SELECT
    'domains',
    COUNT(*)
FROM domains

UNION ALL

SELECT
    'job_skills',
    COUNT(*)
FROM job_skills

UNION ALL

SELECT
    'job_domains',
    COUNT(*)
FROM job_domains

UNION ALL

SELECT
    'skill_demand',
    COUNT(*)
FROM skill_demand

UNION ALL

SELECT
    'domain_skill_demand',
    COUNT(*)
FROM domain_skill_demand;



SELECT COUNT(*) AS invalid_job_skill_refs
FROM job_skills js
LEFT JOIN jobs j
    ON js.job_id = j.job_id
LEFT JOIN skills s
    ON js.skill_id = s.skill_id
WHERE j.job_id IS NULL
   OR s.skill_id IS NULL;