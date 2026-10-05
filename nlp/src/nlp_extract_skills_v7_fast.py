import pandas as pd
import re
from sqlalchemy import create_engine

# ============================================================
# PATHS
# ============================================================

SKILLS_FILE = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform\data\processed\skills_dictionary_clean_v7.csv"

OUTPUT_FILE = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform\data\processed\job_skill_extraction_clean_v7.csv"

DB_URL = "postgresql+psycopg2://postgres:Postgres%405100@localhost:5100/ai_skill_gaps"


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# AHO-CORASICK
# ============================================================

try:
    import ahocorasick
except ImportError:
    print("pyahocorasick is not installed.")
    print("Run:")
    print("pip install pyahocorasick")
    raise


# ============================================================
# LOAD DICTIONARY
# ============================================================

print("=" * 70)
print("NLP SKILL EXTRACTION - V7 FAST")
print("=" * 70)

skills_df = pd.read_csv(SKILLS_FILE)

print(f"\nClean V7 skills loaded: {len(skills_df):,}")


# ============================================================
# BUILD AHO-CORASICK AUTOMATON
# ============================================================

automaton = ahocorasick.Automaton()

pattern_count = 0
duplicate_count = 0

seen_normalized = set()

for _, row in skills_df.iterrows():

    skill_id = int(row["skill_id"])
    skill_name = str(row["skill_name"]).strip()

    normalized = normalize_text(skill_name)

    if not normalized:
        continue

    if normalized in seen_normalized:
        duplicate_count += 1
        continue

    seen_normalized.add(normalized)

    automaton.add_word(
        normalized,
        (skill_id, skill_name, normalized)
    )

    pattern_count += 1


automaton.make_automaton()

print(f"Usable skill patterns: {pattern_count:,}")
print(f"Duplicate normalized patterns ignored: {duplicate_count:,}")


# ============================================================
# LOAD JOBS
# ============================================================

print("\nLoading jobs from PostgreSQL...")

engine = create_engine(DB_URL)

jobs_df = pd.read_sql(
    """
    SELECT
        job_id,
        title,
        job_description
    FROM jobs
    ORDER BY job_id
    """,
    engine
)

print(f"Jobs loaded: {len(jobs_df):,}")


# ============================================================
# BOUNDARY CHECK
# ============================================================

def valid_boundary(text, start, end):

    # Character before match
    if start > 0:

        before = text[start - 1]

        if before.isalnum():
            return False

    # Character after match
    if end < len(text):

        after = text[end]

        if after.isalnum():
            return False

    return True


# ============================================================
# EXTRACT
# ============================================================

records = []

seen_pairs = set()

print("\nStarting fast extraction...\n")

for index, row in jobs_df.iterrows():

    job_id = int(row["job_id"])

    title = "" if pd.isna(row["title"]) else str(row["title"])

    description = (
        ""
        if pd.isna(row["job_description"])
        else str(row["job_description"])
    )

    text = normalize_text(
        title + " " + description
    )

    if not text:
        continue

    job_pairs = set()

    for end_index, data in automaton.iter(text):

        skill_id, skill_name, normalized_skill = data

        start_index = end_index - len(normalized_skill) + 1

        if not valid_boundary(
            text,
            start_index,
            end_index + 1
        ):
            continue

        pair = (job_id, skill_id)

        if pair not in job_pairs:

            job_pairs.add(pair)

            if pair not in seen_pairs:

                seen_pairs.add(pair)

                records.append(
                    {
                        "job_id": job_id,
                        "skill_id": skill_id,
                        "skill_name": skill_name
                    }
                )

    if (index + 1) % 500 == 0:

        print(
            f"Processed {index + 1:,}/{len(jobs_df):,} jobs | "
            f"records: {len(records):,}"
        )


# ============================================================
# SAVE
# ============================================================

result_df = pd.DataFrame(
    records,
    columns=[
        "job_id",
        "skill_id",
        "skill_name"
    ]
)

result_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("V7 FAST EXTRACTION COMPLETED")
print("=" * 70)

print(f"\nTotal extraction records : {len(result_df):,}")

if len(result_df) > 0:

    unique_jobs = result_df["job_id"].nunique()

    unique_skills = result_df["skill_id"].nunique()

    duplicate_pairs = result_df.duplicated(
        subset=["job_id", "skill_id"]
    ).sum()

    print(f"Unique jobs with skills  : {unique_jobs:,}")
    print(f"Unique skills extracted  : {unique_skills:,}")
    print(f"Duplicate job-skill pairs: {duplicate_pairs:,}")

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )

    print("\nSkills per job:")

    print(f"Minimum : {skills_per_job.min():,}")
    print(f"Maximum : {skills_per_job.max():,}")
    print(f"Average : {skills_per_job.mean():.2f}")
    print(f"Median  : {skills_per_job.median():.0f}")


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILLS <= 2 CHARACTERS")
print("=" * 70)

short_df = result_df[
    result_df["skill_name"]
    .astype(str)
    .str.len() <= 2
]

print(f"Records with <=2 character skills: {len(short_df):,}")

if len(short_df) > 0:

    short_counts = (
        short_df["skill_name"]
        .value_counts()
        .head(30)
    )

    for skill, count in short_counts.items():

        print(
            f"{skill:<10} {count:,}"
        )


# ============================================================
# PROBLEMATIC JOB
# ============================================================

problem_job = 240925000000

print("\n" + "=" * 70)
print("PROBLEMATIC JOB")
print("=" * 70)

problem_result = result_df[
    result_df["job_id"] == problem_job
]

print(f"Job ID: {problem_job}")
print(f"Extracted skills: {len(problem_result)}")

for skill in problem_result["skill_name"]:

    print(f"  {skill}")


# ============================================================
# TOP 30
# ============================================================

print("\n" + "=" * 70)
print("TOP 30 EXTRACTED SKILLS")
print("=" * 70)

top_skills = (
    result_df["skill_name"]
    .value_counts()
    .head(30)
)

for i, (skill, count) in enumerate(
    top_skills.items(),
    1
):

    print(
        f"{i:2}. {skill:<35} {count:,}"
    )


# ============================================================
# ZERO-SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("ZERO-SKILL JOB ANALYSIS")
print("=" * 70)

jobs_with_skills = set(
    result_df["job_id"].unique()
)

zero_skill_jobs = jobs_df[
    ~jobs_df["job_id"].isin(jobs_with_skills)
]

print(
    f"Total jobs in PostgreSQL : {len(jobs_df):,}"
)

print(
    f"Jobs with extracted skills: "
    f"{len(jobs_with_skills):,}"
)

print(
    f"Jobs with zero skills     : "
    f"{len(zero_skill_jobs):,}"
)

if len(zero_skill_jobs) > 0:

    for _, row in zero_skill_jobs.head(30).iterrows():

        print(
            f"  {row['job_id']} - {row['title']}"
        )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)

print("Output saved to:")
print(OUTPUT_FILE)

print("\nPostgreSQL data was NOT modified.")

print("=" * 70)