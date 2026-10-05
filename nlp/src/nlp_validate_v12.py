import os
import pandas as pd


# ============================================================
# V12 NLP EXTRACTION VALIDATION
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

EXTRACTION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v12.csv"
)

TOTAL_JOBS = 21031


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("V12 NLP EXTRACTION VALIDATION")
print("=" * 70)

print("\nLoading V12 extraction...")

if not os.path.exists(EXTRACTION_FILE):
    raise FileNotFoundError(
        f"\nV12 extraction file not found:\n{EXTRACTION_FILE}"
    )

df = pd.read_csv(EXTRACTION_FILE)

print(f"Records loaded: {len(df):,}")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = {
    "job_id",
    "skill_id",
    "skill_name",
    "canonical_skill_name"
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("BASIC VALIDATION")
print("=" * 70)

print(f"Rows: {len(df):,}")

print(
    f"Unique jobs: "
    f"{df['job_id'].nunique():,}"
)

print(
    f"Unique skills: "
    f"{df['canonical_skill_name'].nunique():,}"
)

duplicate_pairs = df.duplicated(
    subset=["job_id", "canonical_skill_name"]
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

print(
    f"Minimum: "
    f"{skills_per_job.min()}"
)

print(
    f"Maximum: "
    f"{skills_per_job.max()}"
)

print(
    f"Average: "
    f"{skills_per_job.mean():.2f}"
)

print(
    f"Median: "
    f"{skills_per_job.median():.0f}"
)

print(
    f"25th percentile: "
    f"{skills_per_job.quantile(0.25):.0f}"
)

print(
    f"75th percentile: "
    f"{skills_per_job.quantile(0.75):.0f}"
)


# ============================================================
# SKILL BUCKETS
# ============================================================

print("\n" + "=" * 70)
print("SKILLS PER JOB BUCKETS")
print("=" * 70)

buckets = {
    "1-5": (
        (skills_per_job >= 1) &
        (skills_per_job <= 5)
    ).sum(),

    "6-10": (
        (skills_per_job >= 6) &
        (skills_per_job <= 10)
    ).sum(),

    "11-20": (
        (skills_per_job >= 11) &
        (skills_per_job <= 20)
    ).sum(),

    "21-30": (
        (skills_per_job >= 21) &
        (skills_per_job <= 30)
    ).sum(),

    "31-50": (
        (skills_per_job >= 31) &
        (skills_per_job <= 50)
    ).sum(),

    "51-100": (
        (skills_per_job >= 51) &
        (skills_per_job <= 100)
    ).sum(),

    "101+": (
        skills_per_job >= 101
    ).sum(),
}

for bucket, count in buckets.items():
    print(f"{bucket:<10}{count}")


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILL VALIDATION")
print("=" * 70)

short_mask = (
    df["canonical_skill_name"]
    .astype(str)
    .str.len()
    <= 2
)

short_df = df[short_mask]

print(
    f"Records with skills <= 2 characters: "
    f"{len(short_df):,}"
)

if not short_df.empty:

    print("\nShort skill frequencies:")

    print(
        short_df[
            "canonical_skill_name"
        ]
        .value_counts()
        .to_string()
    )


# ============================================================
# TOP 50 SKILLS
# ============================================================

print("\n" + "=" * 70)
print("TOP 50 EXTRACTED SKILLS")
print("=" * 70)

top_50 = (
    df["canonical_skill_name"]
    .value_counts()
    .head(50)
)

print(top_50.to_string())


# ============================================================
# TECHNICAL SKILL COUNTS
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
    "Git",
]

skill_counts = (
    df["canonical_skill_name"]
    .value_counts()
)

for skill in technical_skills:

    count = skill_counts.get(
        skill,
        0
    )

    print(
        f"{skill}: {count:,}"
    )


# ============================================================
# SUSPICIOUS / GENERIC TERM CHECK
# ============================================================

print("\n" + "=" * 70)
print("SUSPICIOUS / GENERIC TERM CHECK")
print("=" * 70)

suspicious_terms = [
    # V11 problematic terms
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
    "code",

    # V11 other frequent generic terms
    "Providing",
    "Public",
    "Clarity",
    "similar",
    "Strong",
    "High",
    "Good",
    "Basic",
    "Excellent",
    "Professional",
    "Expertise",
    "Experience",
    "Knowledge",
    "Skills",
    "Skill",
    "Ability",
    "Responsibility",
    "Responsibilities",
    "Requirement",
    "Requirements",
    "Candidate",
    "Candidates",
    "Job",
    "Jobs",
    "Role",
    "Roles",
    "Work",
    "Working",
    "Team",
    "Teams",
    "Member",
    "Members",
    "Manager",
    "Management",
    "Lead",
    "Leader",
    "Leadership",
    "Senior",
    "Junior",
    "Executive",
    "Associate",
    "Support",
    "Service",
    "Services",
    "Business",
    "Customer",
    "Customers",
    "Client",
    "Clients",
    "Company",
    "Organization",
    "Industry",
    "Field",
    "Office",
    "Operations",
    "Operation",
    "Process",
    "Processes",
    "Planning",
    "Delivery",
    "Development",
    "Develop",
    "Documentation",
    "Communication",
    "Written",
    "Verbal",
    "Interpersonal",
    "Public",
    "Prepare",
    "Preparing",
    "Maintain",
    "Maintaining",
    "Maintenance",
    "Monitoring",
    "Problem",
    "Problems",
    "Global",
    "International",
    "Complex",
    "Time",
    "Year",
    "Years",
    "Shift",
    "Schedule",
    "Quality",
    "Performance",
    "Production",
    "Administration",
    "Administrative",
    "Environment",
    "Projects",
    "Project",
    "Tools",
    "Systems",
    "System",
    "Computer",
    "Computer Science",
    "Science",
    "Marketing",
    "Financial",
    "Sales",
    "Selling",
    "Upselling",
    "Cross",
    "Cross Selling",
    "Strategist",
    "Adherence",
    "Best Practices",

    # V12 newly suspicious terms
    "VOICE",
    "Digital",
    "Execution",
    "Assistant",
    "Test",
    "Learning",
    "platform",
    "Naukri",
    "Frameworks",
    "Travel",
    "Part",
    "Health",
    "Programming",
    "Dynamic",
    "Review",
    "Resolve",
    "BANK",
    "ACCOUNTING",
    "ACCOUNTS",
]


found_suspicious = []

for term in suspicious_terms:

    matches = df[
        df["canonical_skill_name"]
        .astype(str)
        .str.lower()
        == term.lower()
    ]

    if not matches.empty:

        count = len(matches)

        found_suspicious.append(
            (term, count)
        )

        print(
            f"{term}: {count:,}"
        )


if not found_suspicious:
    print(
        "No suspicious terms from the validation list were extracted."
    )


# ============================================================
# HIGH-SKILL JOB VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("HIGH-SKILL JOB VALIDATION")
print("=" * 70)

print(
    f"Jobs with more than 50 skills: "
    f"{(skills_per_job > 50).sum():,}"
)

print(
    f"Jobs with more than 75 skills: "
    f"{(skills_per_job > 75).sum():,}"
)

print(
    f"Jobs with more than 100 skills: "
    f"{(skills_per_job > 100).sum():,}"
)

print(
    f"Jobs with more than 150 skills: "
    f"{(skills_per_job > 150).sum():,}"
)


# ============================================================
# TOP 20 HIGH-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("TOP 20 JOBS BY EXTRACTED SKILL COUNT")
print("=" * 70)

print(
    skills_per_job
    .sort_values(ascending=False)
    .head(20)
    .to_string()
)


# ============================================================
# PROBLEMATIC JOB
# ============================================================

print("\n" + "=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)

problematic_job_id = 240925000000

problematic = df[
    df["job_id"] == problematic_job_id
]

print(
    f"Job ID: {problematic_job_id}"
)

print(
    f"Extracted skills: {len(problematic)}"
)

if not problematic.empty:

    print(
        problematic[
            "canonical_skill_name"
        ]
        .to_string(index=False)
    )


# ============================================================
# ZERO-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)

unique_jobs = set(
    df["job_id"]
    .astype(int)
    .unique()
)

zero_skill_jobs = (
    TOTAL_JOBS - len(unique_jobs)
)

print(
    f"Total jobs: {TOTAL_JOBS:,}"
)

print(
    f"Jobs with skills: {len(unique_jobs):,}"
)

print(
    f"Jobs with zero skills: {zero_skill_jobs:,}"
)


# ============================================================
# DATA QUALITY CHECKS
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECKS")
print("=" * 70)

print(
    f"Missing job_id: "
    f"{df['job_id'].isna().sum()}"
)

print(
    f"Missing skill_id: "
    f"{df['skill_id'].isna().sum()}"
)

print(
    f"Missing skill name: "
    f"{df['skill_name'].isna().sum()}"
)

print(
    f"Missing canonical skill: "
    f"{df['canonical_skill_name'].isna().sum()}"
)

print(
    f"Empty canonical skill: "
    f"{(
        df['canonical_skill_name']
        .astype(str)
        .str.strip()
        .eq("")
    ).sum()}"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V12 VALIDATION COMPLETED")
print("=" * 70)

print(
    "\nPostgreSQL was NOT modified."
)

print("=" * 70)