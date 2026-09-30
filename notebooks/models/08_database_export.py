import pandas as pd

# ============================================================
# AI SKILL GAP INTELLIGENCE PLATFORM
# STEP 8 - DATABASE EXPORT
# ============================================================

# ------------------------------------------------------------
# INPUT FILE PATHS
# ------------------------------------------------------------

CLEANED_JOBS_PATH = "data/processed/cleaned_job_postings.csv"

NORMALIZED_SKILLS_PATH = "data/processed/normalized_job_skills.csv"

JOB_DOMAINS_PATH = "data/processed/job_domains.csv"

SKILL_DEMAND_PATH = "data/processed/skill_demand.csv"

DOMAIN_SKILL_DEMAND_PATH = "data/processed/domain_skill_demand.csv"


# ------------------------------------------------------------
# OUTPUT FILE PATHS
# ------------------------------------------------------------

JOBS_OUTPUT = "database/jobs.csv"

SKILLS_OUTPUT = "database/skills.csv"

JOB_SKILLS_OUTPUT = "database/job_skills.csv"

DOMAINS_OUTPUT = "database/domains.csv"

JOB_DOMAINS_OUTPUT = "database/job_domains.csv"

SKILL_DEMAND_OUTPUT = "database/skill_demand.csv"

DOMAIN_SKILL_DEMAND_OUTPUT = "database/domain_skill_demand.csv"


# ------------------------------------------------------------
# START
# ------------------------------------------------------------

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 8 - DATABASE EXPORT")
print("=" * 70)


# ------------------------------------------------------------
# LOAD PROCESSED DATA
# ------------------------------------------------------------

print("\nLoading processed datasets...")


jobs_df = pd.read_csv(
    CLEANED_JOBS_PATH
)

skills_df = pd.read_csv(
    NORMALIZED_SKILLS_PATH
)

domains_df = pd.read_csv(
    JOB_DOMAINS_PATH
)

skill_demand_df = pd.read_csv(
    SKILL_DEMAND_PATH
)

domain_skill_demand_df = pd.read_csv(
    DOMAIN_SKILL_DEMAND_PATH
)


print("\nAll datasets loaded successfully.")


print(
    f"Cleaned jobs: {len(jobs_df):,}"
)

print(
    f"Normalized job-skill records: {len(skills_df):,}"
)

print(
    f"Job-domain records: {len(domains_df):,}"
)

print(
    f"Skill demand records: {len(skill_demand_df):,}"
)

print(
    f"Domain-skill demand records: "
    f"{len(domain_skill_demand_df):,}"
)


# ------------------------------------------------------------
# CREATE JOBS TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING JOBS TABLE")
print("=" * 70)


job_columns = [
    "jobId",
    "title",
    "companyName",
    "location",
    "experience",
    "salary",
    "jobDescription",
    "minimumSalary",
    "maximumSalary",
    "minimumExperience",
    "maximumExperience"
]


available_job_columns = [
    column
    for column in job_columns
    if column in jobs_df.columns
]


jobs = jobs_df[
    available_job_columns
].copy()


jobs = jobs.drop_duplicates(
    subset=["jobId"]
)


jobs = jobs.rename(
    columns={
        "jobId": "job_id",
        "companyName": "company_name",
        "jobDescription": "job_description",
        "minimumSalary": "minimum_salary",
        "maximumSalary": "maximum_salary",
        "minimumExperience": "minimum_experience",
        "maximumExperience": "maximum_experience"
    }
)


jobs.to_csv(
    JOBS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Jobs exported: {len(jobs):,}"
)


# ------------------------------------------------------------
# CREATE SKILLS TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING SKILLS TABLE")
print("=" * 70)


skills = (
    skills_df[
        ["normalized_skill"]
    ]
    .dropna()
    .drop_duplicates()
    .sort_values(
        "normalized_skill"
    )
    .reset_index(drop=True)
)


skills.insert(
    0,
    "skill_id",
    range(
        1,
        len(skills) + 1
    )
)


skills = skills.rename(
    columns={
        "normalized_skill": "skill_name"
    }
)


skills.to_csv(
    SKILLS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Skills exported: {len(skills):,}"
)


# ------------------------------------------------------------
# CREATE JOB-SKILLS TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING JOB-SKILLS TABLE")
print("=" * 70)


job_skills = skills_df[
    [
        "jobId",
        "normalized_skill"
    ]
].copy()


job_skills = job_skills.dropna(
    subset=[
        "jobId",
        "normalized_skill"
    ]
)


job_skills = job_skills.rename(
    columns={
        "jobId": "job_id",
        "normalized_skill": "skill_name"
    }
)


job_skills = job_skills.merge(
    skills,
    on="skill_name",
    how="left"
)


job_skills = job_skills[
    [
        "job_id",
        "skill_id"
    ]
]


job_skills = job_skills.dropna(
    subset=[
        "skill_id"
    ]
)


job_skills["skill_id"] = (
    job_skills["skill_id"]
    .astype(int)
)


job_skills = job_skills.drop_duplicates()


job_skills.to_csv(
    JOB_SKILLS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Job-skill relationships exported: "
    f"{len(job_skills):,}"
)


# ------------------------------------------------------------
# CREATE DOMAINS TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING DOMAINS TABLE")
print("=" * 70)


domains = (
    domains_df[
        ["domain"]
    ]
    .dropna()
    .drop_duplicates()
    .sort_values(
        "domain"
    )
    .reset_index(drop=True)
)


domains.insert(
    0,
    "domain_id",
    range(
        1,
        len(domains) + 1
    )
)


domains.to_csv(
    DOMAINS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Domains exported: {len(domains):,}"
)


# ------------------------------------------------------------
# CREATE JOB-DOMAINS TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING JOB-DOMAINS TABLE")
print("=" * 70)


job_domains = domains_df[
    [
        "jobId",
        "domain"
    ]
].copy()


job_domains = job_domains.dropna(
    subset=[
        "jobId",
        "domain"
    ]
)


job_domains = job_domains.rename(
    columns={
        "jobId": "job_id"
    }
)


job_domains = job_domains.merge(
    domains,
    on="domain",
    how="left"
)


job_domains = job_domains[
    [
        "job_id",
        "domain_id"
    ]
]


job_domains = job_domains.dropna(
    subset=[
        "domain_id"
    ]
)


job_domains["domain_id"] = (
    job_domains["domain_id"]
    .astype(int)
)


job_domains = job_domains.drop_duplicates(
    subset=[
        "job_id"
    ]
)


job_domains.to_csv(
    JOB_DOMAINS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Job-domain relationships exported: "
    f"{len(job_domains):,}"
)


# ------------------------------------------------------------
# CREATE SKILL DEMAND TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING SKILL DEMAND TABLE")
print("=" * 70)


skill_demand = skill_demand_df.copy()


skill_demand = skill_demand.rename(
    columns={
        "normalized_skill": "skill_name"
    }
)


skill_demand = skill_demand.merge(
    skills,
    on="skill_name",
    how="left"
)


skill_demand = skill_demand[
    [
        "skill_id",
        "rank",
        "job_count",
        "demand_percentage"
    ]
]


skill_demand = skill_demand.dropna(
    subset=[
        "skill_id"
    ]
)


skill_demand["skill_id"] = (
    skill_demand["skill_id"]
    .astype(int)
)


skill_demand.to_csv(
    SKILL_DEMAND_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Skill demand records exported: "
    f"{len(skill_demand):,}"
)


# ------------------------------------------------------------
# CREATE DOMAIN-SKILL DEMAND TABLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING DOMAIN-SKILL DEMAND TABLE")
print("=" * 70)


domain_skill_demand = (
    domain_skill_demand_df.copy()
)


domain_skill_demand = (
    domain_skill_demand.rename(
        columns={
            "normalized_skill": "skill_name"
        }
    )
)


domain_skill_demand = (
    domain_skill_demand.merge(
        skills,
        on="skill_name",
        how="left"
    )
)


domain_skill_demand = (
    domain_skill_demand.merge(
        domains,
        on="domain",
        how="left"
    )
)


domain_skill_demand = domain_skill_demand[
    [
        "domain_id",
        "skill_id",
        "rank",
        "job_count",
        "total_jobs",
        "demand_percentage"
    ]
]


domain_skill_demand = (
    domain_skill_demand.dropna(
        subset=[
            "domain_id",
            "skill_id"
        ]
    )
)


domain_skill_demand["domain_id"] = (
    domain_skill_demand["domain_id"]
    .astype(int)
)


domain_skill_demand["skill_id"] = (
    domain_skill_demand["skill_id"]
    .astype(int)
)


domain_skill_demand.to_csv(
    DOMAIN_SKILL_DEMAND_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Domain-skill demand records exported: "
    f"{len(domain_skill_demand):,}"
)


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATABASE EXPORT COMPLETED")
print("=" * 70)


print("\nFiles created:")

print(
    f"1. {JOBS_OUTPUT}"
)

print(
    f"2. {SKILLS_OUTPUT}"
)

print(
    f"3. {JOB_SKILLS_OUTPUT}"
)

print(
    f"4. {DOMAINS_OUTPUT}"
)

print(
    f"5. {JOB_DOMAINS_OUTPUT}"
)

print(
    f"6. {SKILL_DEMAND_OUTPUT}"
)

print(
    f"7. {DOMAIN_SKILL_DEMAND_OUTPUT}"
)


print("\nFinal record counts:")

print(
    f"Jobs: {len(jobs):,}"
)

print(
    f"Skills: {len(skills):,}"
)

print(
    f"Job-skill relationships: "
    f"{len(job_skills):,}"
)

print(
    f"Domains: {len(domains):,}"
)

print(
    f"Job-domain relationships: "
    f"{len(job_domains):,}"
)

print(
    f"Skill demand records: "
    f"{len(skill_demand):,}"
)

print(
    f"Domain-skill demand records: "
    f"{len(domain_skill_demand):,}"
)


print("\nStep 8 completed successfully.")

print("=" * 70)