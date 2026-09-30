import os
import re
import pandas as pd
import ahocorasick
from collections import defaultdict
from sqlalchemy import create_engine, text

# ============================================================
# V13 FAST AHO-CORASICK NLP SKILL EXTRACTION
# ============================================================

print("=" * 70)
print("V13 FAST AHO-CORASICK NLP SKILL EXTRACTION")
print("=" * 70)

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

DICTIONARY_FILE = os.path.join(
    DATA_DIR,
    "skills_dictionary_clean_v13.csv"
)

OUTPUT_FILE = os.path.join(
    DATA_DIR,
    "job_skill_extraction_clean_v13.csv"
)

# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

DB_URL = (
    "postgresql+psycopg2://postgres:"
    "Postgres%405100@localhost:5100/ai_skill_gaps"
)

# ------------------------------------------------------------
# TECHNICAL SKILLS
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

def normalize_text(value):

    if pd.isna(value):
        return ""

    text = str(value).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(value):
    return normalize_text(value)


# ------------------------------------------------------------
# LOAD DICTIONARY
# ------------------------------------------------------------

print("\nLoading V13 dictionary...")

skills_df = pd.read_csv(
    DICTIONARY_FILE,
    dtype=str
)

print(
    f"Dictionary rows loaded: "
    f"{len(skills_df):,}"
)

# ------------------------------------------------------------
# BUILD SKILL LOOKUP
# ------------------------------------------------------------

skill_lookup = {}

duplicate_count = 0

for _, row in skills_df.iterrows():

    skill_id = int(row["skill_id"])

    skill_name = str(
        row["skill_name"]
    ).strip()

    canonical_name = str(
        row["canonical_skill_name"]
    ).strip()

    normalized = normalize_skill(
        skill_name
    )

    if not normalized:
        continue

    if normalized in skill_lookup:

        duplicate_count += 1
        continue

    skill_lookup[normalized] = {
        "skill_id": skill_id,
        "skill_name": skill_name,
        "canonical_skill_name": canonical_name
    }

print(
    f"Usable skill patterns: "
    f"{len(skill_lookup):,}"
)

print(
    f"Duplicate normalized patterns ignored: "
    f"{duplicate_count:,}"
)

# ------------------------------------------------------------
# BUILD AHO-CORASICK AUTOMATON
# ------------------------------------------------------------

print("\nBuilding Aho-Corasick matcher...")

automaton = ahocorasick.Automaton()

for pattern, info in skill_lookup.items():

    automaton.add_word(
        pattern,
        (pattern, info)
    )

automaton.make_automaton()

print("Aho-Corasick matcher ready.")

# ------------------------------------------------------------
# BOUNDARY CHECK
# ------------------------------------------------------------

def valid_boundary(text, start, end):

    """
    Prevent substring false positives.

    Example:
        SQL should match "SQL"
        but not "MySQL"
        or "NoSQL"

    """

    if start > 0:

        left = text[start - 1]

        if left.isalnum() or left == "_":
            return False

    if end < len(text):

        right = text[end]

        if right.isalnum() or right == "_":
            return False

    return True


# ------------------------------------------------------------
# LOAD JOBS
# ------------------------------------------------------------

print("\nConnecting to PostgreSQL...")

engine = create_engine(DB_URL)

query = text("""
    SELECT
        job_id,
        title,
        job_description
    FROM jobs
    ORDER BY job_id
""")

jobs_df = pd.read_sql(
    query,
    engine
)

print(
    f"Jobs loaded: "
    f"{len(jobs_df):,}"
)

# ------------------------------------------------------------
# EXTRACTION
# ------------------------------------------------------------

print("\nStarting V13 Aho-Corasick extraction...")
print()

records = []

skill_frequency = defaultdict(int)

for index, row in jobs_df.iterrows():

    job_id = int(row["job_id"])

    title = (
        ""
        if pd.isna(row["title"])
        else str(row["title"])
    )

    description = (
        ""
        if pd.isna(row["job_description"])
        else str(row["job_description"])
    )

    text_to_search = normalize_text(
        title + " " + description
    )

    if not text_to_search:
        continue

    job_seen = set()

    for end_index, value in automaton.iter(
        text_to_search
    ):

        pattern, info = value

        start_index = (
            end_index
            - len(pattern)
            + 1
        )

        end_exclusive = (
            end_index + 1
        )

        # ----------------------------------------
        # Boundary validation
        # ----------------------------------------

        if not valid_boundary(
            text_to_search,
            start_index,
            end_exclusive
        ):
            continue

        skill_id = info["skill_id"]

        if skill_id in job_seen:
            continue

        job_seen.add(skill_id)

        records.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "skill_name": info["skill_name"],
            "canonical_skill_name":
                info["canonical_skill_name"]
        })

        skill_frequency[
            info["canonical_skill_name"]
        ] += 1

    # --------------------------------------------
    # Progress
    # --------------------------------------------

    if (index + 1) % 1000 == 0:

        print(
            f"Processed "
            f"{index + 1:,} / "
            f"{len(jobs_df):,} jobs"
        )

# ------------------------------------------------------------
# RESULT
# ------------------------------------------------------------

result_df = pd.DataFrame(records)

if result_df.empty:

    print("\nERROR: No skills extracted.")

    raise SystemExit(1)

# ------------------------------------------------------------
# REMOVE DUPLICATES
# ------------------------------------------------------------

before = len(result_df)

result_df = result_df.drop_duplicates(
    subset=[
        "job_id",
        "skill_id"
    ]
)

duplicates_removed = (
    before - len(result_df)
)

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ------------------------------------------------------------
# STATISTICS
# ------------------------------------------------------------

total_jobs = len(jobs_df)

total_records = len(result_df)

unique_jobs = result_df[
    "job_id"
].nunique()

unique_skills = result_df[
    "canonical_skill_name"
].nunique()

skills_per_job = (
    result_df
    .groupby("job_id")
    .size()
)

zero_skill_jobs = (
    total_jobs - unique_jobs
)

duplicate_pairs = result_df.duplicated(
    subset=[
        "job_id",
        "skill_id"
    ]
).sum()

# ------------------------------------------------------------
# TECHNICAL COUNTS
# ------------------------------------------------------------

technical_counts = {}

canonical_lower = (
    result_df[
        "canonical_skill_name"
    ]
    .astype(str)
    .str.lower()
)

for skill in TECHNICAL_SKILLS:

    count = result_df[
        canonical_lower
        == skill.lower()
    ]["job_id"].nunique()

    technical_counts[
        skill
    ] = count

# ------------------------------------------------------------
# SHORT SKILLS
# ------------------------------------------------------------

short_mask = (
    result_df[
        "canonical_skill_name"
    ]
    .astype(str)
    .str.len()
    <= 2
)

short_df = result_df[
    short_mask
]

short_counts = (
    short_df[
        "canonical_skill_name"
    ]
    .value_counts()
    .head(20)
)

# ------------------------------------------------------------
# TOP SKILLS
# ------------------------------------------------------------

top_skills = (
    result_df[
        "canonical_skill_name"
    ]
    .value_counts()
    .head(30)
)

# ------------------------------------------------------------
# HIGH-SKILL JOBS
# ------------------------------------------------------------

over_50 = (
    skills_per_job > 50
).sum()

over_75 = (
    skills_per_job > 75
).sum()

over_100 = (
    skills_per_job > 100
).sum()

over_150 = (
    skills_per_job > 150
).sum()

# ------------------------------------------------------------
# PROBLEMATIC JOB
# ------------------------------------------------------------

problematic_id = 240925000000

problematic = result_df[
    result_df["job_id"]
    == problematic_id
]

# ------------------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("V13 EXTRACTION COMPLETED")
print("=" * 70)

print(
    f"Total extraction records: "
    f"{total_records:,}"
)

print(
    f"Unique jobs with skills: "
    f"{unique_jobs:,}"
)

print(
    f"Unique canonical skills: "
    f"{unique_skills:,}"
)

print(
    f"Duplicate job-skill pairs removed: "
    f"{duplicates_removed:,}"
)

print("\nSKILLS PER JOB")

print(
    f"Minimum: "
    f"{skills_per_job.min():,}"
)

print(
    f"Maximum: "
    f"{skills_per_job.max():,}"
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

# ------------------------------------------------------------
# SHORT SKILLS
# ------------------------------------------------------------

print("\nSHORT SKILL CHECK")

print(
    f"Skills <= 2 characters: "
    f"{len(short_df):,}"
)

for skill, count in short_counts.items():

    print(
        f"{skill}: {count}"
    )

# ------------------------------------------------------------
# TOP SKILLS
# ------------------------------------------------------------

print("\nTOP 30 SKILLS")

for skill, count in top_skills.items():

    print(
        f"{skill}: {count}"
    )

# ------------------------------------------------------------
# TECHNICAL
# ------------------------------------------------------------

print("\nTECHNICAL SKILL COUNTS")

for skill in TECHNICAL_SKILLS:

    print(
        f"{skill}: "
        f"{technical_counts[skill]}"
    )

# ------------------------------------------------------------
# ZERO SKILLS
# ------------------------------------------------------------

print("\nZERO-SKILL JOBS")

print(
    f"Total jobs: "
    f"{total_jobs:,}"
)

print(
    f"Jobs with skills: "
    f"{unique_jobs:,}"
)

print(
    f"Jobs with zero skills: "
    f"{zero_skill_jobs:,}"
)

# ------------------------------------------------------------
# HIGH SKILL
# ------------------------------------------------------------

print("\nHIGH-SKILL JOBS")

print(
    f"Jobs >50 skills: "
    f"{over_50:,}"
)

print(
    f"Jobs >75 skills: "
    f"{over_75:,}"
)

print(
    f"Jobs >100 skills: "
    f"{over_100:,}"
)

print(
    f"Jobs >150 skills: "
    f"{over_150:,}"
)

# ------------------------------------------------------------
# PROBLEMATIC JOB
# ------------------------------------------------------------

print("\nPROBLEMATIC JOB")

print(
    f"Job ID: "
    f"{problematic_id}"
)

if problematic.empty:

    print("Extracted skills: 0")

else:

    problem_skills = (
        problematic[
            "canonical_skill_name"
        ]
        .drop_duplicates()
        .tolist()
    )

    print(
        f"Extracted skills: "
        f"{len(problem_skills)}"
    )

    print(problem_skills)

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print("\nOutput:")
print(OUTPUT_FILE)

print("\nPostgreSQL was NOT modified.")

print("=" * 70)