import os
import re
import pandas as pd
import psycopg2
import ahocorasick


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5100,
    "database": "ai_skill_gaps",
    "user": "postgres",
    "password": "Postgres@5100"
}

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DICT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v5.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v5.csv"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Normalize common separators
    text = text.replace("&", " and ")

    # Keep letters, numbers, spaces and common skill symbols
    text = re.sub(r"[^a-z0-9+#./\- ]+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# PADDED MATCHING
# ============================================================

def prepare_pattern(skill):
    skill = normalize_text(skill)

    if not skill:
        return None

    return f" {skill} "


def prepare_text(text):
    text = normalize_text(text)

    if not text:
        return ""

    return f" {text} "


# ============================================================
# LOAD CLEAN V5 DICTIONARY
# ============================================================

print("=" * 70)
print("SKILL EXTRACTION - V5")
print("=" * 70)

print("\nLoading V5 clean dictionary...")
print(DICT_FILE)

skills_df = pd.read_csv(DICT_FILE)

print(f"Clean V5 skills loaded: {len(skills_df):,}")


# ============================================================
# BUILD AHO-CORASICK AUTOMATON
# ============================================================

automaton = ahocorasick.Automaton()

normalized_to_skill = {}

rejected_one_char = 0
duplicate_normalized = 0

for _, row in skills_df.iterrows():

    skill_id = int(row["skill_id"])
    skill_name = str(row["skill_name"]).strip()

    normalized = normalize_text(skill_name)

    if not normalized:
        continue

    # Reject one-character alphabetic skills
    if len(normalized) == 1 and normalized.isalpha():
        rejected_one_char += 1
        continue

    if normalized in normalized_to_skill:
        duplicate_normalized += 1
        continue

    normalized_to_skill[normalized] = (
        skill_id,
        skill_name
    )

    pattern = prepare_pattern(skill_name)

    if pattern:
        automaton.add_word(
            pattern,
            (skill_id, skill_name)
        )


automaton.make_automaton()

print(f"Usable skill patterns: {len(normalized_to_skill):,}")
print(f"Rejected one-character skills: {rejected_one_char:,}")
print(f"Duplicate normalized patterns ignored: {duplicate_normalized:,}")


# ============================================================
# CONNECT TO POSTGRESQL
# ============================================================

print("\nConnecting to PostgreSQL...")

conn = psycopg2.connect(**DB_CONFIG)

query = """
SELECT
    job_id,
    title,
    job_description
FROM jobs
ORDER BY job_id
"""

jobs_df = pd.read_sql(query, conn)

conn.close()

print(f"Jobs loaded: {len(jobs_df):,}")


# ============================================================
# EXTRACT SKILLS
# ============================================================

records = []

print("\nExtracting skills...")

for index, row in jobs_df.iterrows():

    job_id = int(row["job_id"])

    title = "" if pd.isna(row["title"]) else str(row["title"])
    description = (
        ""
        if pd.isna(row["job_description"])
        else str(row["job_description"])
    )

    # Search both title and description
    combined_text = f"{title} {description}"

    text = prepare_text(combined_text)

    if not text:
        continue

    found_pairs = set()

    for _, (_, skill_data) in enumerate(automaton.iter(text)):

        skill_id, skill_name = skill_data

        pair = (job_id, skill_id)

        if pair in found_pairs:
            continue

        found_pairs.add(pair)

        records.append(
            {
                "job_id": job_id,
                "skill_id": skill_id,
                "skill_name": skill_name
            }
        )

    if (index + 1) % 1000 == 0:
        print(
            f"Processed {index + 1:,}/{len(jobs_df):,} jobs..."
        )


# ============================================================
# CREATE DATAFRAME
# ============================================================

result_df = pd.DataFrame(
    records,
    columns=[
        "job_id",
        "skill_id",
        "skill_name"
    ]
)


# ============================================================
# REMOVE DUPLICATE JOB-SKILL PAIRS
# ============================================================

if not result_df.empty:

    result_df = result_df.drop_duplicates(
        subset=["job_id", "skill_id"]
    )

    result_df = result_df.sort_values(
        ["job_id", "skill_id"]
    )


# ============================================================
# SAVE
# ============================================================

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V5 EXTRACTION COMPLETED")
print("=" * 70)

print(f"Output file:")
print(OUTPUT_FILE)

print(f"\nTotal extraction records: {len(result_df):,}")

if not result_df.empty:

    unique_jobs = result_df["job_id"].nunique()
    unique_skills = result_df["skill_id"].nunique()

    counts = result_df.groupby("job_id").size()

    print(f"Unique jobs with skills: {unique_jobs:,}")
    print(f"Unique skills extracted: {unique_skills:,}")

    print("\nSkills/job:")
    print(f"  Min    : {counts.min():,}")
    print(f"  Max    : {counts.max():,}")
    print(f"  Average: {counts.mean():.2f}")
    print(f"  Median : {counts.median():.0f}")

    duplicate_pairs = result_df.duplicated(
        subset=["job_id", "skill_id"]
    ).sum()

    print(f"\nDuplicate job-skill pairs: {duplicate_pairs:,}")

    short_df = result_df[
        result_df["skill_name"].str.len() <= 2
    ]

    print(
        f"\nSkills <= 2 characters: {len(short_df):,}"
    )

    if not short_df.empty:
        print("\nShort skills:")
        print(
            short_df["skill_name"]
            .value_counts()
            .head(20)
            .to_string()
        )

    print("\nTop 30 extracted skills:")

    print(
        result_df["skill_name"]
        .value_counts()
        .head(30)
        .to_string()
    )

print("\nPostgreSQL was NOT modified.")
print("Previous V1-V4 extraction files were NOT modified.")