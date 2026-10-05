import os
import re
import pandas as pd
import ahocorasick
from sqlalchemy import create_engine, text


# ============================================================
# V12 NLP SKILL EXTRACTION
# Boundary-aware Aho-Corasick
# ============================================================


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DICTIONARY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v12.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v12.csv"
)


# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

DB_URL = (
    "postgresql+psycopg2://"
    "postgres:Postgres%405100"
    "@localhost:5100/"
    "ai_skill_gaps"
)

engine = create_engine(DB_URL)


# ------------------------------------------------------------
# BOUNDARY CHECK
# ------------------------------------------------------------

def valid_boundary(text, start, end):
    """
    Prevent substring false positives.

    Example:
        UI should not match inside:
        "build"
        "fruit"
        "security"

    But:
        "UI design"
        "experience with UI"
    should match.
    """

    before = text[start - 1] if start > 0 else ""
    after = text[end] if end < len(text) else ""

    # If the matched skill starts/ends with an alphanumeric
    # character, require a non-alphanumeric boundary.

    if before and before.isalnum():
        return False

    if after and after.isalnum():
        return False

    return True


# ------------------------------------------------------------
# LOAD V12 DICTIONARY
# ------------------------------------------------------------

print("=" * 70)
print("Aho-Corasick NLP SKILL EXTRACTION - V12")
print("=" * 70)

print("\nLoading V12 dictionary...")

if not os.path.exists(DICTIONARY_FILE):
    raise FileNotFoundError(
        f"\nV12 dictionary not found:\n{DICTIONARY_FILE}"
    )

dictionary_df = pd.read_csv(DICTIONARY_FILE)

print(
    f"V12 dictionary rows loaded: "
    f"{len(dictionary_df):,}"
)


# ------------------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = {
    "skill_id",
    "skill_name",
    "canonical_skill_name"
}

missing_columns = required_columns - set(dictionary_df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ------------------------------------------------------------
# PREPROCESS TEXT
# ------------------------------------------------------------

def preprocess_text(text_value):
    if pd.isna(text_value):
        return ""

    text_value = str(text_value).lower()

    # Normalize common separators
    text_value = text_value.replace("–", "-")
    text_value = text_value.replace("—", "-")

    # Normalize whitespace
    text_value = re.sub(r"\s+", " ", text_value)

    return text_value.strip()


# ------------------------------------------------------------
# BUILD AHO-CORASICK AUTOMATON
# ------------------------------------------------------------

automaton = ahocorasick.Automaton()

pattern_count = 0
duplicate_patterns = 0
rejected_one_char = 0

seen_patterns = set()

for _, row in dictionary_df.iterrows():

    skill_id = int(row["skill_id"])

    skill_name = str(row["skill_name"]).strip()

    canonical_skill = str(
        row["canonical_skill_name"]
    ).strip()

    pattern = preprocess_text(skill_name)

    if not pattern:
        continue

    # Reject single alphabetic characters
    if len(pattern) == 1 and pattern.isalpha():
        rejected_one_char += 1
        continue

    if pattern in seen_patterns:
        duplicate_patterns += 1
        continue

    seen_patterns.add(pattern)

    automaton.add_word(
        pattern,
        (
            skill_id,
            skill_name,
            canonical_skill
        )
    )

    pattern_count += 1


automaton.make_automaton()


print(
    f"Canonical skills: "
    f"{dictionary_df['canonical_skill_name'].nunique():,}"
)

print(
    f"Usable skill patterns: "
    f"{pattern_count:,}"
)

print(
    f"Rejected one-character patterns: "
    f"{rejected_one_char:,}"
)

print(
    f"Duplicate normalized patterns ignored: "
    f"{duplicate_patterns:,}"
)


# ------------------------------------------------------------
# LOAD JOBS
# ------------------------------------------------------------

print("\nLoading jobs from PostgreSQL...")

query = text("""
    SELECT
        job_id,
        title,
        job_description
    FROM jobs
    ORDER BY job_id
""")

jobs_df = pd.read_sql(query, engine)

print(
    f"Jobs loaded: {len(jobs_df):,}"
)


# ------------------------------------------------------------
# EXTRACT SKILLS
# ------------------------------------------------------------

records = []

for row in jobs_df.itertuples(index=False):

    job_id = int(row.job_id)

    title = (
        "" if pd.isna(row.title)
        else str(row.title)
    )

    description = (
        "" if pd.isna(row.job_description)
        else str(row.job_description)
    )

    # Search title + description
    full_text = (
        title + " " + description
    )

    processed_text = preprocess_text(full_text)

    if not processed_text:
        continue

    found_for_job = set()

    for end_index, match_data in automaton.iter(
        processed_text
    ):

        skill_id, skill_name, canonical_skill = match_data

        start_index = (
            end_index - len(
                preprocess_text(skill_name)
            ) + 1
        )

        end_position = end_index + 1

        # ----------------------------------------------------
        # Boundary validation
        # ----------------------------------------------------

        if not valid_boundary(
            processed_text,
            start_index,
            end_position
        ):
            continue

        # ----------------------------------------------------
        # Deduplicate within job
        # ----------------------------------------------------

        canonical_key = (
            str(canonical_skill).strip().lower()
        )

        if canonical_key in found_for_job:
            continue

        found_for_job.add(canonical_key)

        records.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "skill_name": skill_name,
            "canonical_skill_name": canonical_skill
        })


# ------------------------------------------------------------
# CREATE OUTPUT DATAFRAME
# ------------------------------------------------------------

result_df = pd.DataFrame(records)


if result_df.empty:

    print("\nWARNING: No skills were extracted.")

    result_df = pd.DataFrame(
        columns=[
            "job_id",
            "skill_id",
            "skill_name",
            "canonical_skill_name"
        ]
    )


# ------------------------------------------------------------
# REMOVE DUPLICATE JOB-SKILL PAIRS
# ------------------------------------------------------------

before_dedup = len(result_df)

result_df = result_df.drop_duplicates(
    subset=[
        "job_id",
        "canonical_skill_name"
    ]
)

duplicate_pairs = (
    before_dedup - len(result_df)
)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

result_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ------------------------------------------------------------
# BASIC STATISTICS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("V12 EXTRACTION COMPLETED")
print("=" * 70)

print(
    f"Total extraction records: "
    f"{len(result_df):,}"
)

print(
    f"Unique jobs with skills: "
    f"{result_df['job_id'].nunique():,}"
)

print(
    f"Unique canonical skills extracted: "
    f"{result_df['canonical_skill_name'].nunique():,}"
)

print(
    f"Duplicate job-skill pairs removed: "
    f"{duplicate_pairs:,}"
)


# ------------------------------------------------------------
# SKILLS PER JOB
# ------------------------------------------------------------

if not result_df.empty:

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )

    print("\nSKILLS PER JOB")

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


# ------------------------------------------------------------
# SHORT SKILL CHECK
# ------------------------------------------------------------

if not result_df.empty:

    short_df = result_df[
        result_df["canonical_skill_name"]
        .astype(str)
        .str.len()
        <= 2
    ]

    print("\nSHORT SKILL CHECK")

    print(
        f"Skills <= 2 characters: "
        f"{len(short_df):,}"
    )

    if not short_df.empty:

        print(
            short_df[
                "canonical_skill_name"
            ]
            .value_counts()
            .head(30)
            .to_string()
        )


# ------------------------------------------------------------
# TOP 30 SKILLS
# ------------------------------------------------------------

print("\nTOP 30 EXTRACTED SKILLS")

if not result_df.empty:

    print(
        result_df[
            "canonical_skill_name"
        ]
        .value_counts()
        .head(30)
        .to_string()
    )


# ------------------------------------------------------------
# TECHNICAL SKILLS
# ------------------------------------------------------------

print("\nTECHNICAL SKILLS")

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

if not result_df.empty:

    skill_counts = (
        result_df[
            "canonical_skill_name"
        ]
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


# ------------------------------------------------------------
# ZERO-SKILL JOBS
# ------------------------------------------------------------

all_job_ids = set(
    jobs_df["job_id"].astype(int)
)

jobs_with_skills = set(
    result_df["job_id"].astype(int)
)

zero_skill_jobs = (
    all_job_ids - jobs_with_skills
)

print("\nZERO-SKILL JOBS")

print(
    f"Total jobs: "
    f"{len(all_job_ids):,}"
)

print(
    f"Jobs with skills: "
    f"{len(jobs_with_skills):,}"
)

print(
    f"Jobs with zero skills: "
    f"{len(zero_skill_jobs):,}"
)


# ------------------------------------------------------------
# HIGH-SKILL JOBS
# ------------------------------------------------------------

if not result_df.empty:

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )

    print("\nHIGH-SKILL JOBS")

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
# PROBLEMATIC JOB
# ------------------------------------------------------------

problematic_job_id = 240925000000

problematic = result_df[
    result_df["job_id"]
    == problematic_job_id
]

print("\nPROBLEMATIC JOB")

print(
    f"Job ID: "
    f"{problematic_job_id}"
)

print(
    f"Extracted skills: "
    f"{len(problematic)}"
)

if not problematic.empty:

    print(
        problematic[
            "canonical_skill_name"
        ]
        .to_string(index=False)
    )


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 70)

print("Output:")
print(OUTPUT_FILE)

print("\nPostgreSQL was NOT modified.")

print("=" * 70)