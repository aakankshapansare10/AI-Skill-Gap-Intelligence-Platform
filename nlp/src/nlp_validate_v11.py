import os
import pandas as pd


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v11.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("V11 NLP EXTRACTION VALIDATION")
print("=" * 70)

print("\nLoading V11 extraction...")

df = pd.read_csv(INPUT_FILE)

print(f"Records loaded: {len(df):,}")


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("BASIC VALIDATION")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Unique jobs: {df['job_id'].nunique():,}")
print(
    f"Unique skills: "
    f"{df['canonical_skill_name'].nunique():,}"
)

duplicate_pairs = df.duplicated(
    subset=["job_id", "skill_id"]
).sum()

print(
    f"Duplicate job-skill pairs: "
    f"{duplicate_pairs:,}"
)


# ============================================================
# SKILLS PER JOB
# ============================================================

print("\n" + "=" * 70)
print("SKILLS PER JOB DISTRIBUTION")
print("=" * 70)

skills_per_job = (
    df.groupby("job_id")
    .size()
)

print(f"Minimum: {skills_per_job.min()}")
print(f"Maximum: {skills_per_job.max()}")
print(f"Average: {skills_per_job.mean():.2f}")
print(f"Median: {skills_per_job.median():.0f}")
print(
    f"25th percentile: "
    f"{skills_per_job.quantile(0.25):.0f}"
)
print(
    f"75th percentile: "
    f"{skills_per_job.quantile(0.75):.0f}"
)


# ============================================================
# DISTRIBUTION BUCKETS
# ============================================================

print("\n" + "=" * 70)
print("SKILLS PER JOB BUCKETS")
print("=" * 70)

buckets = pd.cut(
    skills_per_job,
    bins=[0, 5, 10, 20, 30, 50, 100, float("inf")],
    labels=[
        "1-5",
        "6-10",
        "11-20",
        "21-30",
        "31-50",
        "51-100",
        "101+"
    ]
)

print(
    buckets.value_counts()
    .sort_index()
    .to_string()
)


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILL VALIDATION")
print("=" * 70)

df["skill_length"] = (
    df["canonical_skill_name"]
    .astype(str)
    .str.len()
)

short_df = df[
    df["skill_length"] <= 2
]

print(
    f"Records with skills <= 2 characters: "
    f"{len(short_df):,}"
)

if not short_df.empty:

    print("\nShort skill frequencies:")

    print(
        short_df["canonical_skill_name"]
        .value_counts()
        .to_string()
    )


# ============================================================
# TOP 50 SKILLS
# ============================================================

print("\n" + "=" * 70)
print("TOP 50 EXTRACTED SKILLS")
print("=" * 70)

top_skills = (
    df["canonical_skill_name"]
    .value_counts()
    .head(50)
)

print(top_skills.to_string())


# ============================================================
# TECHNICAL SKILLS
# ============================================================

print("\n" + "=" * 70)
print("TECHNICAL SKILL COUNTS")
print("=" * 70)

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

skill_counts = (
    df["canonical_skill_name"]
    .value_counts()
)

for skill in technical_skills:

    print(
        f"{skill}: "
        f"{skill_counts.get(skill, 0):,}"
    )


# ============================================================
# GENERIC / SUSPICIOUS SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SUSPICIOUS / GENERIC TERM CHECK")
print("=" * 70)

suspicious_terms = [
    "Data",
    "ProFile",
    "CLOUD",
    "TESTING",
    "REPORTS",
    "FRESHERS",
    "implement",
    "Insurance",
    "Certification",
    "Reporting",
    "Analytical",
    "FINANCE",
    "INTEGRATION",
    "developing",
    "equivalent",
    "Problem-Solving",
    "Market",
    "Growth",
    "TECH",
    "full time",
    "Monitor",
    "Call",
    "code"
]

for term in suspicious_terms:

    count = skill_counts.get(term, 0)

    if count > 0:

        print(
            f"{term}: {count:,}"
        )


# ============================================================
# HIGH SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("HIGH-SKILL JOB VALIDATION")
print("=" * 70)

for threshold in [50, 75, 100, 150]:

    count = (
        skills_per_job > threshold
    ).sum()

    print(
        f"Jobs with more than "
        f"{threshold} skills: {count:,}"
    )


# ============================================================
# TOP HIGH-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("TOP 20 JOBS BY EXTRACTED SKILL COUNT")
print("=" * 70)

top_jobs = (
    skills_per_job
    .sort_values(ascending=False)
    .head(20)
)

print(
    top_jobs.to_string()
)


# ============================================================
# PROBLEMATIC JOB
# ============================================================

print("\n" + "=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)

problem_job_id = 240925000000

problem = df[
    df["job_id"] == problem_job_id
]

print(
    f"Job ID: {problem_job_id}"
)

print(
    f"Extracted skills: {len(problem)}"
)

if not problem.empty:

    print(
        problem[
            [
                "skill_id",
                "skill_name",
                "canonical_skill_name"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# ZERO SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)

# Total jobs are known from PostgreSQL
TOTAL_JOBS = 21031

jobs_with_skills = (
    df["job_id"]
    .nunique()
)

zero_skill_jobs = (
    TOTAL_JOBS - jobs_with_skills
)

print(
    f"Total jobs: {TOTAL_JOBS:,}"
)

print(
    f"Jobs with skills: "
    f"{jobs_with_skills:,}"
)

print(
    f"Jobs with zero skills: "
    f"{zero_skill_jobs:,}"
)


# ============================================================
# DATA QUALITY CHECKS
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECKS")
print("=" * 70)

print(
    "Missing job_id:",
    df["job_id"].isna().sum()
)

print(
    "Missing skill_id:",
    df["skill_id"].isna().sum()
)

print(
    "Missing skill name:",
    df["skill_name"].isna().sum()
)

print(
    "Missing canonical skill:",
    df["canonical_skill_name"].isna().sum()
)

print(
    "Empty canonical skill:",
    (
        df["canonical_skill_name"]
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("V11 VALIDATION COMPLETED")
print("=" * 70)

print("\nPostgreSQL was NOT modified.")
print("=" * 70)