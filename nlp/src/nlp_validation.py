import os
import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

EXTRACTION_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "job_skill_extraction_clean_v4.csv"
)


# ============================================================
# POSTGRESQL CONNECTION
# ============================================================

DATABASE_URL = (
    "postgresql+psycopg2://postgres:"
    "Postgres%405100"
    "@localhost:5100/ai_skill_gaps"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("NLP V4 DETAILED VALIDATION")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(EXTRACTION_FILE):
    raise FileNotFoundError(
        f"\nExtraction file not found:\n{EXTRACTION_FILE}"
    )

print("\nLoading V4 extraction file...")

df = pd.read_csv(EXTRACTION_FILE)

print(f"Records loaded: {len(df):,}")


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC VALIDATION")
print("=" * 70)

print(
    f"\nUnique jobs: "
    f"{df['job_id'].nunique():,}"
)

print(
    f"Unique skills: "
    f"{df['skill_id'].nunique():,}"
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

skills_per_job = (
    df.groupby("job_id")
    .size()
)

print("\nSkills per job:")

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


# ============================================================
# 2. TOP EXTRACTED SKILLS
# ============================================================

print("\n" + "=" * 70)
print("2. TOP 50 EXTRACTED SKILLS")
print("=" * 70)

top_skills = (
    df["skill_name"]
    .value_counts()
    .head(50)
)

print(
    top_skills.to_string()
)


# ============================================================
# 3. GENERIC / SUSPICIOUS SKILLS
# ============================================================

print("\n" + "=" * 70)
print("3. SUSPICIOUS GENERIC SKILLS")
print("=" * 70)

suspicious_skills = [
    "Manager",
    "Communication",
    "Sales",
    "Support",
    "ENGINEER",
    "Executive",
    "DESIGN",
    "Senior",
    "Lead",
    "Engineering",
    "Maintain",
    "Tools",
    "Performance",
    "DEVELOPER",
    "Office",
    "Hiring",
    "Operations",
    "Computer",
    "QUALITY",
    "professional",
    "expertise",
    "Analysis",
    "Associate",
    "Cross",
    "Selling",
    "Strategist",
    "Schedule",
    "adherence",
    "Problem",
    "Application",
    "Company",
    "Salary",
    "Career",
    "Environment",
    "Product",
    "Technical",
    "Technology",
    "Software",
    "Customer",
    "Client",
    "Delivery",
    "Build",
    "Building",
]


print(
    "\nChecking suspicious skills in extraction...\n"
)

for skill in suspicious_skills:

    matches = df[
        df["skill_name"]
        .astype(str)
        .str.lower()
        ==
        skill.lower()
    ]

    if len(matches) > 0:

        print(
            f"{skill:<20} "
            f"{len(matches):>6,}"
        )


# ============================================================
# 4. SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("4. SHORT SKILLS (<= 2 CHARACTERS)")
print("=" * 70)

short_skills = df[
    df["skill_name"]
    .astype(str)
    .str.len()
    <= 2
]

print(
    f"\nTotal short-skill records: "
    f"{len(short_skills):,}"
)

short_counts = (
    short_skills["skill_name"]
    .value_counts()
)

print("\nShort skill frequency:")

print(
    short_counts.to_string()
)


# ============================================================
# 5. CHECK BE DEGREE
# ============================================================

print("\n" + "=" * 70)
print("5. CHECK 'BE DEGREE'")
print("=" * 70)

be_degree = df[
    df["skill_name"]
    .astype(str)
    .str.lower()
    == "be degree"
]

print(
    f"\n'be degree' occurrences: "
    f"{len(be_degree):,}"
)


# ============================================================
# 6. PROBLEMATIC JOB
# ============================================================

print("\n" + "=" * 70)
print("6. PROBLEMATIC JOB CHECK")
print("=" * 70)

problematic_job_id = 240925000000

problematic_job = df[
    df["job_id"] == problematic_job_id
]

print(
    f"\nJob ID: {problematic_job_id}"
)

print(
    f"Extracted skills: "
    f"{len(problematic_job):,}"
)

if not problematic_job.empty:

    print("\nExtracted skills:")

    print(
        problematic_job[
            [
                "skill_id",
                "skill_name"
            ]
        ]
        .sort_values("skill_name")
        .to_string(index=False)
    )

else:

    print("No skills extracted.")


# ============================================================
# 7. ZERO-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("7. ZERO-SKILL JOBS")
print("=" * 70)

jobs_query = text("""
    SELECT
        job_id,
        title,
        job_description
    FROM jobs
    ORDER BY job_id
""")

with engine.connect() as connection:

    jobs_df = pd.read_sql(
        jobs_query,
        connection
    )

all_job_ids = set(
    jobs_df["job_id"].astype(int)
)

extracted_job_ids = set(
    df["job_id"].astype(int)
)

zero_skill_ids = (
    all_job_ids -
    extracted_job_ids
)

print(
    f"\nTotal zero-skill jobs: "
    f"{len(zero_skill_ids):,}"
)

if zero_skill_ids:

    zero_jobs = jobs_df[
        jobs_df["job_id"].isin(zero_skill_ids)
    ][
        [
            "job_id",
            "title",
            "job_description"
        ]
    ]

    for _, row in zero_jobs.iterrows():

        print("\n" + "-" * 70)

        print(
            f"Job ID: {row['job_id']}"
        )

        print(
            f"Title: {row['title']}"
        )

        description = str(
            row["job_description"]
        )

        print(
            "Description:"
        )

        print(
            description[:1000]
        )


# ============================================================
# 8. HIGHEST SKILL COUNT JOBS
# ============================================================

print("\n" + "=" * 70)
print("8. TOP 20 JOBS BY SKILL COUNT")
print("=" * 70)

highest_jobs = (
    skills_per_job
    .sort_values(
        ascending=False
    )
    .head(20)
)

print(
    highest_jobs.to_string()
)


# ============================================================
# 9. JOBS WITH MORE THAN 100 SKILLS
# ============================================================

print("\n" + "=" * 70)
print("9. JOBS WITH MORE THAN 100 SKILLS")
print("=" * 70)

high_skill_jobs = skills_per_job[
    skills_per_job > 100
]

print(
    f"\nJobs with >100 skills: "
    f"{len(high_skill_jobs):,}"
)

print(
    high_skill_jobs
    .sort_values(
        ascending=False
    )
    .head(30)
    .to_string()
)


# ============================================================
# 10. CHECK IMPORTANT TECHNICAL SKILLS
# ============================================================

print("\n" + "=" * 70)
print("10. IMPORTANT TECHNICAL SKILL CHECK")
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

print()

for skill in technical_skills:

    matches = df[
        df["skill_name"]
        .astype(str)
        .str.lower()
        ==
        skill.lower()
    ]

    print(
        f"{skill:<20} "
        f"{len(matches):>6,}"
    )


# ============================================================
# 11. SAVE VALIDATION REPORT
# ============================================================

REPORT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "nlp_v4_validation_summary.txt"
)

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "NLP V4 VALIDATION SUMMARY\n"
    )

    report.write(
        "=" * 60 + "\n\n"
    )

    report.write(
        f"Records: {len(df):,}\n"
    )

    report.write(
        f"Unique jobs: {df['job_id'].nunique():,}\n"
    )

    report.write(
        f"Unique skills: {df['skill_id'].nunique():,}\n"
    )

    report.write(
        f"Duplicate pairs: {duplicate_pairs:,}\n"
    )

    report.write(
        f"Minimum skills/job: {skills_per_job.min()}\n"
    )

    report.write(
        f"Maximum skills/job: {skills_per_job.max()}\n"
    )

    report.write(
        f"Average skills/job: "
        f"{skills_per_job.mean():.2f}\n"
    )

    report.write(
        f"Median skills/job: "
        f"{skills_per_job.median():.0f}\n"
    )

    report.write(
        f"Short skill records: "
        f"{len(short_skills):,}\n"
    )

    report.write(
        f"BE Degree occurrences: "
        f"{len(be_degree):,}\n"
    )

    report.write(
        f"Zero-skill jobs: "
        f"{len(zero_skill_ids):,}\n"
    )

    report.write(
        f"Jobs with >100 skills: "
        f"{len(high_skill_jobs):,}\n"
    )


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 70)
print("DETAILED V4 VALIDATION COMPLETED")
print("=" * 70)

print("\nValidation report saved to:")

print(REPORT_FILE)

print("\nNo PostgreSQL tables were modified.")