import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

EXTRACTION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v5.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("NLP VALIDATION - V5")
print("=" * 70)

print("\nLoading:")
print(EXTRACTION_FILE)

df = pd.read_csv(EXTRACTION_FILE)

print(f"\nTotal records: {len(df):,}")
print(f"Unique jobs: {df['job_id'].nunique():,}")
print(f"Unique skills: {df['skill_id'].nunique():,}")


# ============================================================
# DUPLICATES
# ============================================================

duplicates = df.duplicated(
    subset=["job_id", "skill_id"]
).sum()

print(f"\nDuplicate job-skill pairs: {duplicates:,}")


# ============================================================
# SKILLS PER JOB
# ============================================================

skill_counts = df.groupby("job_id").size()

print("\n" + "=" * 70)
print("SKILLS PER JOB")
print("=" * 70)

print(f"Minimum : {skill_counts.min():,}")
print(f"Maximum : {skill_counts.max():,}")
print(f"Average : {skill_counts.mean():.2f}")
print(f"Median  : {skill_counts.median():.0f}")


# ============================================================
# ZERO-SKILL JOBS
# ============================================================

jobs_with_skills = set(df["job_id"].unique())

# We know the complete dataset has 21,031 jobs
total_jobs = 21031

zero_skill_jobs = total_jobs - len(jobs_with_skills)

print(f"\nJobs with zero extracted skills: {zero_skill_jobs:,}")


# ============================================================
# TOP 100 SKILLS
# ============================================================

print("\n" + "=" * 70)
print("TOP 100 EXTRACTED SKILLS")
print("=" * 70)

top_skills = (
    df["skill_name"]
    .value_counts()
    .head(100)
)

print(top_skills.to_string())


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILLS")
print("=" * 70)

short_df = df[
    df["skill_name"].astype(str).str.len() <= 3
]

print(
    f"Records with <= 3 characters: "
    f"{len(short_df):,}"
)

if not short_df.empty:
    print("\nShort skill frequencies:")
    print(
        short_df["skill_name"]
        .value_counts()
        .to_string()
    )


# ============================================================
# GENERIC / SUSPICIOUS TERMS
# ============================================================

SUSPICIOUS_TERMS = [
    "skills",
    "Team",
    "Management",
    "Data",
    "DESIGN",
    "manage",
    "Teams",
    "Systems",
    "Time",
    "Science",
    "PROJECT",
    "Shift",
    "Compliance",
    "Computer Science",
    "Marketing",
    "CLOUD",
    "Financial",
    "clients",
    "FRESHERS",
    "System",
    "Good Communication",
    "TESTING",
    "ENGLISH",
    "TRAINING",
    "standards",
    "Certification",
    "Excellent Communication",
    "Automation",
    "Process",
    "Business",
    "Customer",
    "Technical",
    "Technology",
    "Software",
    "Application",
    "Development",
    "Develop",
    "Requirements",
    "Planning",
    "Documentation",
    "Leadership",
    "Relationship",
    "Service",
    "Industry",
    "Field",
    "Experience",
    "Education",
    "Qualification"
]


print("\n" + "=" * 70)
print("SUSPICIOUS TERM CHECK")
print("=" * 70)

skill_counts_all = df["skill_name"].value_counts()

for term in SUSPICIOUS_TERMS:

    count = skill_counts_all.get(term, 0)

    if count > 0:
        print(f"PRESENT: {term:<30} {count:,}")
    else:
        print(f"ABSENT : {term}")


# ============================================================
# TECHNICAL SKILLS
# ============================================================

TECHNICAL_SKILLS = [
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
print("IMPORTANT TECHNICAL SKILLS")
print("=" * 70)

for skill in TECHNICAL_SKILLS:

    count = skill_counts_all.get(skill, 0)

    if count > 0:
        print(f"PRESENT: {skill:<20} {count:,}")
    else:
        print(f"ABSENT : {skill}")


# ============================================================
# HIGH-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("JOBS WITH MORE THAN 100 EXTRACTED SKILLS")
print("=" * 70)

high_skill_jobs = skill_counts[
    skill_counts > 100
]

print(
    f"Jobs with >100 skills: "
    f"{len(high_skill_jobs):,}"
)

if not high_skill_jobs.empty:
    print(
        high_skill_jobs
        .sort_values(ascending=False)
        .head(30)
        .to_string()
    )


# ============================================================
# SAVE REPORT
# ============================================================

REPORT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "nlp_v5_validation_summary.txt"
)

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("NLP V5 VALIDATION REPORT\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Total records: {len(df):,}\n")
    f.write(
        f"Unique jobs: {df['job_id'].nunique():,}\n"
    )
    f.write(
        f"Unique skills: {df['skill_id'].nunique():,}\n"
    )
    f.write(
        f"Duplicate pairs: {duplicates:,}\n"
    )
    f.write(
        f"Min skills/job: {skill_counts.min():,}\n"
    )
    f.write(
        f"Max skills/job: {skill_counts.max():,}\n"
    )
    f.write(
        f"Average skills/job: {skill_counts.mean():.2f}\n"
    )
    f.write(
        f"Median skills/job: {skill_counts.median():.0f}\n"
    )
    f.write(
        f"Zero-skill jobs: {zero_skill_jobs:,}\n"
    )

    f.write("\nTOP 100 SKILLS\n")
    f.write("-" * 70 + "\n")
    f.write(top_skills.to_string())

    f.write("\n\nSHORT SKILLS\n")
    f.write("-" * 70 + "\n")
    f.write(
        short_df["skill_name"]
        .value_counts()
        .to_string()
    )

    f.write("\n\nSUSPICIOUS TERMS\n")
    f.write("-" * 70 + "\n")

    for term in SUSPICIOUS_TERMS:
        count = skill_counts_all.get(term, 0)

        if count > 0:
            f.write(
                f"PRESENT: {term} = {count:,}\n"
            )
        else:
            f.write(
                f"ABSENT: {term}\n"
            )

print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

print("\nReport saved to:")
print(REPORT_FILE)

print("\nNo PostgreSQL changes were made.")