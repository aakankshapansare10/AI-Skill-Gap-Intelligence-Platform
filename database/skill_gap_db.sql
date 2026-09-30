CREATE TABLE IF NOT EXISTS jobs (
    job_id BIGINT PRIMARY KEY,
    title TEXT,
    company_name TEXT,
    location TEXT,
    experience TEXT,
    salary TEXT,
    job_description TEXT,
    minimum_salary NUMERIC,
    maximum_salary NUMERIC,
    minimum_experience NUMERIC,
    maximum_experience NUMERIC
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY,
    skill_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS domains (
    domain_id INTEGER PRIMARY KEY,
    domain_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id BIGINT NOT NULL,
    skill_id INTEGER NOT NULL,

    PRIMARY KEY (job_id, skill_id),

    FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_domains (
    job_id BIGINT PRIMARY KEY,
    domain_id INTEGER NOT NULL,

    FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    FOREIGN KEY (domain_id)
        REFERENCES domains(domain_id)
        ON DELETE CASCADE
);

SELECT COUNT(*) AS current_rows
FROM job_skills;

CREATE TABLE IF NOT EXISTS skill_demand (
    skill_id INTEGER PRIMARY KEY,
    rank INTEGER,
    job_count INTEGER,
    demand_percentage NUMERIC,

    FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS domain_skill_demand (
    domain_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    rank INTEGER,
    job_count INTEGER,
    total_jobs INTEGER,
    demand_percentage NUMERIC,

    PRIMARY KEY (domain_id, skill_id),

    FOREIGN KEY (domain_id)
        REFERENCES domains(domain_id)
        ON DELETE CASCADE,

    FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE
);

SELECT COUNT(*) AS total_jobs
FROM jobs;

SELECT COUNT(*) AS total_skills
FROM skills;

SELECT COUNT(*) AS total_domains
FROM domains;

SELECT COUNT(*) AS current_rows
FROM job_skills;

COPY job_skills (
    job_id,
    skill_id
)
FROM 'C:/skill_gap_data/job_skills.csv'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '"',
    ENCODING 'UTF8'
);

SELECT COUNT(*) AS missing_job_references
FROM job_skills js
LEFT JOIN jobs j
    ON js.job_id = j.job_id
WHERE j.job_id IS NULL;

SELECT COUNT(*) AS total_jobs
FROM jobs;

DROP TABLE IF EXISTS job_skills_staging;

CREATE TABLE job_skills_staging (
    job_id BIGINT,
    skill_id BIGINT
);

SELECT COUNT(*) AS staging_rows
FROM job_skills_staging;

SELECT COUNT(*) AS invalid_job_ids
FROM job_skills_staging s
LEFT JOIN jobs j
    ON s.job_id = j.job_id
WHERE j.job_id IS NULL;

INSERT INTO job_skills (job_id, skill_id)
SELECT s.job_id, s.skill_id
FROM job_skills_staging s
INNER JOIN jobs j
    ON s.job_id = j.job_id;
	SELECT COUNT(*) AS total_job_skills
FROM job_skills;

SELECT COUNT(*) AS total_job_skills
FROM job_skills;

SELECT COUNT(*) AS invalid_references
FROM job_skills js
LEFT JOIN jobs j
    ON js.job_id = j.job_id
WHERE j.job_id IS NULL;

DROP TABLE IF EXISTS job_domains_staging;

CREATE TABLE job_domains_staging (
    job_id BIGINT,
    domain_id BIGINT
);

SELECT COUNT(*) AS invalid_job_ids
FROM job_domains_staging s
LEFT JOIN jobs j
    ON s.job_id = j.job_id
WHERE j.job_id IS NULL;

SELECT COUNT(*) AS invalid_domain_ids
FROM job_domains_staging s
LEFT JOIN domains d
    ON s.domain_id = d.domain_id
WHERE d.domain_id IS NULL;

INSERT INTO job_domains (job_id, domain_id)
SELECT s.job_id, s.domain_id
FROM job_domains_staging s
INNER JOIN jobs j
    ON s.job_id = j.job_id
INNER JOIN domains d
    ON s.domain_id = d.domain_id;

	SELECT COUNT(*) AS total_job_domains
FROM job_domains;

SELECT COUNT(*) AS invalid_references
FROM job_domains jd
LEFT JOIN jobs j
    ON jd.job_id = j.job_id
LEFT JOIN domains d
    ON jd.domain_id = d.domain_id
WHERE j.job_id IS NULL
   OR d.domain_id IS NULL;

DROP TABLE IF EXISTS skill_demand_staging;

CREATE TABLE skill_demand_staging (
    skill_id BIGINT,
    total_jobs BIGINT,
    total_job_postings BIGINT,
    demand_percentage NUMERIC
);

SELECT COUNT(*) AS staging_rows
FROM skill_demand_staging;

SELECT COUNT(*) AS invalid_skill_ids
FROM skill_demand_staging s
LEFT JOIN skills sk
    ON s.skill_id = sk.skill_id
WHERE sk.skill_id IS NULL;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'skill_demand'
ORDER BY ordinal_position;

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
    s.total_jobs,
    s.total_job_postings,
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
    total_jobs BIGINT,
    demand_percentage NUMERIC
);

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'domain_skill_demand'
ORDER BY ordinal_position;

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
        SUM(job_count) AS total_jobs
    FROM skill_counts
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
LEFT JOIN jobs j ON js.job_id = j.job_id
LEFT JOIN skills s ON js.skill_id = s.skill_id
WHERE j.job_id IS NULL
   OR s.skill_id IS NULL;

SELECT COUNT(*) AS invalid_job_domain_refs
FROM job_domains jd
LEFT JOIN jobs j ON jd.job_id = j.job_id
LEFT JOIN domains d ON jd.domain_id = d.domain_id
WHERE j.job_id IS NULL
   OR d.domain_id IS NULL;

SELECT COUNT(*) AS invalid_skill_demand_refs
FROM skill_demand sd
LEFT JOIN skills s ON sd.skill_id = s.skill_id
WHERE s.skill_id IS NULL;

SELECT COUNT(*) AS invalid_domain_skill_refs
FROM domain_skill_demand dsd
LEFT JOIN domains d ON dsd.domain_id = d.domain_id
LEFT JOIN skills s ON dsd.skill_id = s.skill_id
WHERE d.domain_id IS NULL
   OR s.skill_id IS NULL;w