import os
import pandas as pd
import psycopg2


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform"

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "job_skill_extraction_clean_v6.csv"
)

REPORT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "nlp_v6_validation_summary.txt"
)


# ============================================================
# POSTGRESQL CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5100,
    "database": "ai_skill_gaps",
    "user": "postgres",
    "password": "Postgres@5100"
}


# ============================================================
# LOAD EXTRACTION FILE
# ============================================================

print("=" * 70)
print("NLP VALIDATION - V6")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(
    f"\nRecords loaded: "
    f"{len(df):,}"
)


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("BASIC VALIDATION")
print("=" * 70)

total_records = len(df)

unique_jobs = df["job_id"].nunique()

unique_skills = df["skill_id"].nunique()

duplicate_pairs = df.duplicated(
    subset=["job_id", "skill_id"]
).sum()

print(
    f"Total records       : {total_records:,}"
)

print(
    f"Unique jobs         : {unique_jobs:,}"
)

print(
    f"Unique skills       : {unique_skills:,}"
)

print(
    f"Duplicate pairs     : {duplicate_pairs:,}"
)


# ============================================================
# SKILLS PER JOB
# ============================================================

skills_per_job = (
    df.groupby("job_id")
    .size()
)

print("\n" + "=" * 70)
print("SKILLS PER JOB")
print("=" * 70)

print(
    f"Minimum : {skills_per_job.min()}"
)

print(
    f"Maximum : {skills_per_job.max()}"
)

print(
    f"Average : {skills_per_job.mean():.2f}"
)

print(
    f"Median  : {skills_per_job.median():.0f}"
)

print(
    f"25%     : {skills_per_job.quantile(.25):.0f}"
)

print(
    f"75%     : {skills_per_job.quantile(.75):.0f}"
)


# ============================================================
# JOBS WITH MANY SKILLS
# ============================================================

print("\n" + "=" * 70)
print("JOBS WITH MORE THAN 100 SKILLS")
print("=" * 70)

jobs_over_100 = (
    skills_per_job > 100
).sum()

print(
    f"Jobs with >100 skills: "
    f"{jobs_over_100:,}"
)


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILLS")
print("=" * 70)

df["skill_name"] = (
    df["skill_name"]
    .astype(str)
    .str.strip()
)

short_df = df[
    df["skill_name"]
    .str.len()
    <= 3
]

print(
    f"Records with <=3 character skills: "
    f"{len(short_df):,}"
)

print("\nShort skill frequencies:")

short_counts = (
    short_df["skill_name"]
    .value_counts()
)

for skill, count in short_counts.items():

    print(
        f"  {skill}: {count}"
    )


# ============================================================
# TOP 100 SKILLS
# ============================================================

print("\n" + "=" * 70)
print("TOP 100 EXTRACTED SKILLS")
print("=" * 70)

top_100 = (
    df["skill_name"]
    .value_counts()
    .head(100)
)

for rank, (skill, count) in enumerate(
    top_100.items(),
    start=1
):

    print(
        f"{rank:3}. "
        f"{skill:<40} "
        f"{count:,}"
    )


# ============================================================
# SUSPICIOUS GENERIC TERMS
# ============================================================

suspicious_terms = [
    "skills",
    "skill",
    "strong",
    "good",
    "high",
    "maintain",
    "maintaining",
    "hiring",
    "problem",
    "cross",
    "selling",
    "year",
    "years",
    "written",
    "complex",
    "join",
    "targets",
    "equivalent",
    "delivery",
    "international",
    "professional",
    "responsibility",
    "responsibilities",
    "knowledge",
    "ability",
    "required",
    "candidate",
    "role",
    "work",
    "working",
    "people",
    "team",
    "management",
    "manager",
    "support",
    "communication",
    "sales",
    "customer",
    "client",
    "business",
    "technical",
    "technology",
    "software",
    "application",
    "development",
    "develop",
    "requirements",
    "planning",
    "documentation",
    "experience",
    "education",
    "qualification"
]


print("\n" + "=" * 70)
print("SUSPICIOUS / GENERIC TERMS")
print("=" * 70)

skill_counts = (
    df["skill_name"]
    .value_counts()
)

for term in suspicious_terms:

    matches = skill_counts[
        skill_counts.index.str.lower()
        == term.lower()
    ]

    if len(matches) > 0:

        print(
            f"{term:<30} "
            f"{int(matches.iloc[0]):,}"
        )


# ============================================================
# PROBLEMATIC JOB
# ============================================================

problem_job_id = 240925000000

problem_job = df[
    df["job_id"]
    == problem_job_id
]

print("\n" + "=" * 70)
print("PROBLEMATIC JOB")
print("=" * 70)

print(
    f"Job ID: {problem_job_id}"
)

print(
    f"Extracted skills: "
    f"{len(problem_job)}"
)

for _, row in problem_job.iterrows():

    print(
        f"  {row['skill_name']}"
    )


# ============================================================
# CONNECT TO POSTGRESQL
# ============================================================

print("\n" + "=" * 70)
print("ZERO-SKILL JOB ANALYSIS")
print("=" * 70)

connection = psycopg2.connect(
    **DB_CONFIG
)

jobs_df = pd.read_sql(
    """
    SELECT
        job_id,
        title
    FROM jobs
    ORDER BY job_id;
    """,
    connection
)

connection.close()


# ============================================================
# ZERO SKILL JOBS
# ============================================================

all_job_ids = set(
    jobs_df["job_id"]
)

extracted_job_ids = set(
    df["job_id"]
)

zero_skill_ids = sorted(
    all_job_ids
    - extracted_job_ids
)

print(
    f"Total jobs in PostgreSQL : "
    f"{len(all_job_ids):,}"
)

print(
    f"Jobs with extracted skills: "
    f"{len(extracted_job_ids):,}"
)

print(
    f"Jobs with zero skills     : "
    f"{len(zero_skill_ids):,}"
)

if zero_skill_ids:

    zero_jobs = jobs_df[
        jobs_df["job_id"]
        .isin(zero_skill_ids)
    ]

    print("\nZero-skill jobs:")

    for _, row in (
        zero_jobs.iterrows()
    ):

        print(
            f"  {row['job_id']} - "
            f"{row['title']}"
        )


# ============================================================
# TECHNICAL SKILL CHECK
# ============================================================

technical_skills = [
    "Python",
    "SQL",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "React",
    "Angular",
    "Node.js",
    "Power BI",
    "Tableau",
    "Excel",
    "Git"
]

print("\n" + "=" * 70)
print("TECHNICAL SKILL CHECK")
print("=" * 70)

for skill in technical_skills:

    matches = skill_counts[
        skill_counts.index.str.lower()
        == skill.lower()
    ]

    if len(matches) > 0:

        print(
            f"{skill:<20} "
            f"{int(matches.iloc[0]):,}"
        )

    else:

        print(
            f"{skill:<20} "
            f"0"
        )


# ============================================================
# SAVE REPORT
# ============================================================

report_lines = []

report_lines.append(
    "NLP V6 VALIDATION SUMMARY"
)

report_lines.append(
    "=" * 70
)

report_lines.append(
    f"Total records: {total_records:,}"
)

report_lines.append(
    f"Unique jobs: {unique_jobs:,}"
)

report_lines.append(
    f"Unique skills: {unique_skills:,}"
)

report_lines.append(
    f"Duplicate pairs: {duplicate_pairs:,}"
)

report_lines.append(
    f"Min skills/job: {skills_per_job.min()}"
)

report_lines.append(
    f"Max skills/job: {skills_per_job.max()}"
)

report_lines.append(
    f"Average skills/job: {skills_per_job.mean():.2f}"
)

report_lines.append(
    f"Median skills/job: {skills_per_job.median():.0f}"
)

report_lines.append(
    f"Jobs >100 skills: {jobs_over_100:,}"
)

report_lines.append(
    f"Short skill records <=3 chars: {len(short_df):,}"
)

report_lines.append(
    f"Zero-skill jobs: {len(zero_skill_ids):,}"
)

report_lines.append(
    "\nTOP 100 SKILLS"
)

for rank, (skill, count) in enumerate(
    top_100.items(),
    start=1
):

    report_lines.append(
        f"{rank}. {skill}: {count:,}"
    )

report_lines.append(
    "\nTECHNICAL SKILL CHECK"
)

for skill in technical_skills:

    matches = skill_counts[
        skill_counts.index.str.lower()
        == skill.lower()
    ]

    count = (
        int(matches.iloc[0])
        if len(matches) > 0
        else 0
    )

    report_lines.append(
        f"{skill}: {count:,}"
    )

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(report_lines)
    )


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

print(
    "\nValidation report saved to:"
)

print(REPORT_FILE)

print(
    "\nPostgreSQL data was NOT modified."
)

print("=" * 70)