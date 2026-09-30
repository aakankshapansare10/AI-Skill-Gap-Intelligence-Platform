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


SELECT *
FROM jobs
LIMIT 10;

DROP TABLE IF EXISTS job_skills_staging;

CREATE TABLE job_skills_staging (
    job_id BIGINT,
    skill_id INTEGER
);








