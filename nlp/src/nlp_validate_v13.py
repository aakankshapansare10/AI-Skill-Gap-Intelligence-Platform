import pandas as pd
from pathlib import Path
from collections import Counter


# ============================================================
# V13 NLP EXTRACTION VALIDATION
# ============================================================

print("=" * 70)
print("V13 NLP EXTRACTION VALIDATION")
print("=" * 70)


# ------------------------------------------------------------
# 1. FILE PATH
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "job_skill_extraction_clean_v13.csv"
)


print("\nLoading extraction file...")
print(INPUT_FILE)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"\nRows loaded: {len(df):,}")

print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 3. BASIC DATA CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BASIC DATA CHECK")
print("=" * 70)

print(f"Total records: {len(df):,}")

print(f"Unique jobs: {df['job_id'].nunique():,}")

print(f"Unique skills: {df['skill_id'].nunique():,}")


# ------------------------------------------------------------
# 4. DUPLICATE JOB-SKILL PAIRS
# ------------------------------------------------------------

duplicate_pairs = df.duplicated(
    subset=["job_id", "skill_id"]
).sum()

print("\nDuplicate job-skill pairs:")
print(f"{duplicate_pairs:,}")


# ------------------------------------------------------------
# 5. SKILLS PER JOB
# ------------------------------------------------------------

skills_per_job = (
    df.groupby("job_id")
    .size()
    .sort_values()
)

print("\n" + "=" * 70)
print("SKILLS PER JOB")
print("=" * 70)

print(f"Minimum: {skills_per_job.min():,}")
print(f"Maximum: {skills_per_job.max():,}")
print(f"Average: {skills_per_job.mean():.2f}")
print(f"Median: {skills_per_job.median():.0f}")
print(f"25th percentile: {skills_per_job.quantile(0.25):.0f}")
print(f"75th percentile: {skills_per_job.quantile(0.75):.0f}")


# ------------------------------------------------------------
# 6. JOB DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("JOB SKILL DISTRIBUTION")
print("=" * 70)

buckets = {
    "1-5": ((skills_per_job >= 1) & (skills_per_job <= 5)).sum(),
    "6-10": ((skills_per_job >= 6) & (skills_per_job <= 10)).sum(),
    "11-20": ((skills_per_job >= 11) & (skills_per_job <= 20)).sum(),
    "21-30": ((skills_per_job >= 21) & (skills_per_job <= 30)).sum(),
    "31-50": ((skills_per_job >= 31) & (skills_per_job <= 50)).sum(),
    "51-100": ((skills_per_job >= 51) & (skills_per_job <= 100)).sum(),
    "101+": (skills_per_job >= 101).sum(),
}

for bucket, count in buckets.items():
    print(f"{bucket}: {count:,}")


# ------------------------------------------------------------
# 7. SHORT SKILL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SHORT SKILL CHECK")
print("=" * 70)

df["skill_name"] = df["skill_name"].astype(str).str.strip()

short_skills = df[
    df["skill_name"].str.len() <= 2
]

print(
    f"Skills <= 2 characters: "
    f"{len(short_skills):,}"
)

short_counts = (
    short_skills["skill_name"]
    .value_counts()
    .head(30)
)

print("\nMost frequent short skills:")

for skill, count in short_counts.items():
    print(f"{skill}: {count:,}")


# ------------------------------------------------------------
# 8. TOP SKILLS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 50 EXTRACTED SKILLS")
print("=" * 70)

skill_counts = (
    df["skill_name"]
    .value_counts()
    .head(50)
)

for skill, count in skill_counts.items():
    print(f"{skill}: {count:,}")


# ------------------------------------------------------------
# 9. SUSPICIOUS / GENERIC TERMS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUSPICIOUS / GENERIC SKILL CHECK")
print("=" * 70)

suspicious_terms = [
    "skills",
    "team",
    "teams",
    "management",
    "manage",
    "systems",
    "system",
    "data",
    "process",
    "business",
    "customer",
    "technical",
    "technology",
    "software",
    "application",
    "development",
    "develop",
    "requirements",
    "planning",
    "documentation",
    "leadership",
    "relationship",
    "service",
    "industry",
    "field",
    "experience",
    "education",
    "qualification",
    "strong",
    "high",
    "maintain",
    "hiring",
    "problem",
    "cross",
    "selling",
    "year",
    "written",
    "complex",
    "join",
    "targets",
    "equivalent",
    "delivery",
    "international",
    "voice",
    "digital",
    "execution",
    "assistant",
    "test",
    "learning",
    "platform",
    "naukri",
    "frameworks",
    "travel",
    "part",
    "health",
    "programming",
    "dynamic",
    "review",
    "resolve",
    "bank",
    "accounting",
    "accounts",
    "market",
    "growth",
    "reporting",
    "reports",
    "insurance",
    "certification",
    "integration",
    "analytical",
    "finance",
    "providing",
    "public",
    "clarity",
    "similar",
]


skill_lower = (
    df["skill_name"]
    .str.lower()
)

found_suspicious = []

for term in suspicious_terms:
    count = (skill_lower == term.lower()).sum()

    if count > 0:
        found_suspicious.append(
            (term, int(count))
        )

if found_suspicious:

    print("\nSuspicious terms found:")

    for term, count in sorted(
        found_suspicious,
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{term}: {count:,}")

else:

    print("\nNo explicitly blocked generic terms found.")


# ------------------------------------------------------------
# 10. REQUIRED TECHNICAL SKILLS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TECHNICAL SKILL CHECK")
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
    "Git",
]

skill_count_map = (
    df.groupby("skill_name")
    .size()
)

for skill in technical_skills:

    count = skill_count_map.get(skill, 0)

    print(f"{skill}: {count:,}")


# ------------------------------------------------------------
# 11. HIGH-SKILL JOBS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("HIGH-SKILL JOB CHECK")
print("=" * 70)

print(
    f"Jobs >50 skills: "
    f"{(skills_per_job > 50).sum():,}"
)

print(
    f"Jobs >75 skills: "
    f"{(skills_per_job > 75).sum():,}"
)

print(
    f"Jobs >100 skills: "
    f"{(skills_per_job > 100).sum():,}"
)

print(
    f"Jobs >150 skills: "
    f"{(skills_per_job > 150).sum():,}"
)


# ------------------------------------------------------------
# 12. TOP 20 JOBS WITH MOST SKILLS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 20 JOBS WITH MOST EXTRACTED SKILLS")
print("=" * 70)

top_jobs = skills_per_job.sort_values(
    ascending=False
).head(20)

for job_id, count in top_jobs.items():

    print(
        f"Job ID: {job_id} | "
        f"Skills: {count:,}"
    )


# ------------------------------------------------------------
# 13. PROBLEMATIC JOB CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)

problem_job = 240925000000

problem_skills = df[
    df["job_id"] == problem_job
]["skill_name"].tolist()

print(f"Job ID: {problem_job}")

print(
    f"Extracted skills: "
    f"{len(problem_skills)}"
)

if problem_skills:

    print("Skills:")

    for skill in sorted(problem_skills):
        print(f" - {skill}")

else:

    print("No skills extracted.")


# ------------------------------------------------------------
# 14. ZERO-SKILL JOBS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)

# There are 21,031 jobs in PostgreSQL.
# The extraction file only contains jobs where at least
# one skill was extracted.

TOTAL_JOBS = 21031

jobs_with_skills = df["job_id"].nunique()

zero_skill_jobs = TOTAL_JOBS - jobs_with_skills

print(f"Total jobs: {TOTAL_JOBS:,}")
print(f"Jobs with skills: {jobs_with_skills:,}")
print(f"Jobs with zero skills: {zero_skill_jobs:,}")


# ------------------------------------------------------------
# 15. MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUE CHECK")
print("=" * 70)

print(
    df[
        ["job_id", "skill_id", "skill_name"]
    ]
    .isnull()
    .sum()
)


# ------------------------------------------------------------
# 16. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("V13 VALIDATION SUMMARY")
print("=" * 70)

print(f"Records: {len(df):,}")
print(f"Unique jobs: {df['job_id'].nunique():,}")
print(f"Unique skills: {df['skill_id'].nunique():,}")
print(f"Duplicate pairs: {duplicate_pairs:,}")
print(f"Minimum skills/job: {skills_per_job.min():,}")
print(f"Maximum skills/job: {skills_per_job.max():,}")
print(f"Average skills/job: {skills_per_job.mean():.2f}")
print(f"Median skills/job: {skills_per_job.median():.0f}")
print(f"Jobs with zero skills: {zero_skill_jobs:,}")
print(f"Jobs with >100 skills: {(skills_per_job > 100).sum():,}")

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)