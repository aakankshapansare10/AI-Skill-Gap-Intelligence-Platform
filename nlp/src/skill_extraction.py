import os
import re
import pandas as pd
from sqlalchemy import create_engine, text
import ahocorasick


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# V4 CLEAN SKILL DICTIONARY
SKILLS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills_dictionary_clean_v4.csv"
)

# NEW OUTPUT FILE
OUTPUT_FILE = os.path.join(
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
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text_value):
    """
    Normalize text so that matching is more consistent.
    """

    if pd.isna(text_value):
        return ""

    text_value = str(text_value)

    # Convert to lowercase
    text_value = text_value.lower()

    # Replace common separators with spaces
    text_value = re.sub(r"[/|;,]+", " ", text_value)

    # Keep letters, numbers, +, #, &, . and -
    text_value = re.sub(r"[^a-z0-9+#&.\- ]+", " ", text_value)

    # Collapse multiple spaces
    text_value = re.sub(r"\s+", " ", text_value)

    return text_value.strip()


# ============================================================
# LOAD CLEAN V4 SKILL DICTIONARY
# ============================================================

print("=" * 70)
print("NLP SKILL EXTRACTION - V4")
print("=" * 70)

print("\nLoading V4 clean skill dictionary...")

if not os.path.exists(SKILLS_FILE):
    raise FileNotFoundError(
        f"\nV4 skill dictionary not found:\n{SKILLS_FILE}"
    )

skills_df = pd.read_csv(SKILLS_FILE)

required_skill_columns = ["skill_id", "skill_name"]

for column in required_skill_columns:
    if column not in skills_df.columns:
        raise ValueError(
            f"Required column '{column}' is missing from skill dictionary."
        )

skills_df = skills_df.dropna(
    subset=["skill_id", "skill_name"]
).copy()

skills_df["skill_id"] = skills_df["skill_id"].astype(int)
skills_df["skill_name"] = skills_df["skill_name"].astype(str)

print(f"V4 clean skills loaded: {len(skills_df):,}")


# ============================================================
# PREPARE SKILL PATTERNS
# ============================================================

print("\nPreparing skill patterns...")

pattern_to_skill = {}

rejected_one_character = 0
duplicate_patterns = 0

for _, row in skills_df.iterrows():

    skill_id = int(row["skill_id"])
    skill_name = str(row["skill_name"]).strip()

    normalized_skill = normalize_text(skill_name)

    if not normalized_skill:
        continue

    # Reject one-character alphabetic skills
    if len(normalized_skill) == 1 and normalized_skill.isalpha():
        rejected_one_character += 1
        continue

    # Avoid duplicate normalized patterns
    if normalized_skill in pattern_to_skill:
        duplicate_patterns += 1
        continue

    pattern_to_skill[normalized_skill] = (
        skill_id,
        skill_name
    )


print(f"Usable skill patterns: {len(pattern_to_skill):,}")
print(f"Rejected one-character skills: {rejected_one_character:,}")
print(f"Duplicate normalized patterns ignored: {duplicate_patterns:,}")


# ============================================================
# BUILD AHO-CORASICK MATCHER
# ============================================================

print("\nBuilding Aho-Corasick matcher...")

automaton = ahocorasick.Automaton()

for pattern, skill_data in pattern_to_skill.items():

    # Add spaces around the pattern.
    #
    # This helps prevent matching a skill inside another word.
    padded_pattern = " " + pattern + " "

    automaton.add_word(
        padded_pattern,
        (pattern, skill_data[0], skill_data[1])
    )

automaton.make_automaton()

print("Aho-Corasick matcher ready.")


# ============================================================
# LOAD JOBS FROM POSTGRESQL
# ============================================================

print("\nLoading jobs from PostgreSQL...")

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

print(f"Jobs loaded: {len(jobs_df):,}")


# ============================================================
# EXTRACT SKILLS FROM JOBS
# ============================================================

print("\nStarting NLP skill extraction...")
print("This may take some time.\n")

results = []

processed_jobs = 0

for _, job in jobs_df.iterrows():

    job_id = int(job["job_id"])

    title = (
        ""
        if pd.isna(job["title"])
        else str(job["title"])
    )

    description = (
        ""
        if pd.isna(job["job_description"])
        else str(job["job_description"])
    )

    # Combine title + description
    combined_text = title + " " + description

    normalized_text = normalize_text(combined_text)

    if not normalized_text:
        processed_jobs += 1
        continue

    # Add spaces to make padded matching possible
    searchable_text = " " + normalized_text + " "

    found_skills = set()

    # Search all skill patterns
    for _, match_data in automaton.iter(
        searchable_text
    ):

        pattern, skill_id, skill_name = match_data

        pair = (
            skill_id,
            skill_name
        )

        found_skills.add(pair)

    # Save unique job-skill relationships
    for skill_id, skill_name in found_skills:

        results.append({
            "job_id": job_id,
            "skill_id": skill_id,
            "skill_name": skill_name
        })

    processed_jobs += 1

    # Progress message
    if processed_jobs % 1000 == 0:

        print(
            f"Processed {processed_jobs:,} / "
            f"{len(jobs_df):,} jobs..."
        )


# ============================================================
# CREATE OUTPUT DATAFRAME
# ============================================================

print("\nExtraction finished.")

result_df = pd.DataFrame(
    results,
    columns=[
        "job_id",
        "skill_id",
        "skill_name"
    ]
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

if not result_df.empty:

    result_df = result_df.drop_duplicates(
        subset=[
            "job_id",
            "skill_id"
        ]
    )

    result_df = result_df.sort_values(
        by=[
            "job_id",
            "skill_id"
        ]
    ).reset_index(drop=True)


# ============================================================
# SAVE V4 OUTPUT
# ============================================================

result_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\n" + "=" * 70)
print("V4 EXTRACTION COMPLETED")
print("=" * 70)

print(f"\nOutput file:")
print(OUTPUT_FILE)

print(f"\nTotal extraction records: {len(result_df):,}")

if not result_df.empty:

    print(
        f"Unique jobs with skills: "
        f"{result_df['job_id'].nunique():,}"
    )

    print(
        f"Unique skills extracted: "
        f"{result_df['skill_id'].nunique():,}"
    )


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)


if result_df.empty:

    print("\nWARNING: No skills were extracted.")

else:

    # --------------------------------------------------------
    # DUPLICATE CHECK
    # --------------------------------------------------------

    duplicate_count = result_df.duplicated(
        subset=[
            "job_id",
            "skill_id"
        ]
    ).sum()

    print(
        f"\nDuplicate job-skill pairs: "
        f"{duplicate_count:,}"
    )


    # --------------------------------------------------------
    # SKILLS PER JOB
    # --------------------------------------------------------

    skills_per_job = (
        result_df
        .groupby("job_id")
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


    # --------------------------------------------------------
    # SHORT SKILL CHECK
    # --------------------------------------------------------

    short_skills = result_df[
        result_df["skill_name"]
        .astype(str)
        .str.len()
        <= 2
    ]

    print(
        f"\nSkills <= 2 characters: "
        f"{len(short_skills):,}"
    )

    if not short_skills.empty:

        print("\nShort skills found:")

        print(
            short_skills[
                "skill_name"
            ]
            .value_counts()
            .head(30)
            .to_string()
        )


    # --------------------------------------------------------
    # TOP SKILLS
    # --------------------------------------------------------

    print("\nTop 30 extracted skills:")

    top_skills = (
        result_df["skill_name"]
        .value_counts()
        .head(30)
    )

    print(top_skills.to_string())


    # --------------------------------------------------------
    # PROBLEMATIC JOB TEST
    # --------------------------------------------------------

    test_job_id = 240925000000

    problematic_job = result_df[
        result_df["job_id"] == test_job_id
    ]

    print(
        f"\nProblematic job "
        f"{test_job_id}: "
        f"{len(problematic_job)} skills"
    )

    if not problematic_job.empty:

        print(
            problematic_job[
                [
                    "skill_id",
                    "skill_name"
                ]
            ]
            .to_string(index=False)
        )

    else:

        print("No skills extracted for this job.")


    # --------------------------------------------------------
    # HIGH SKILL COUNT JOBS
    # --------------------------------------------------------

    print("\nJobs with highest extracted skill counts:")

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


    # --------------------------------------------------------
    # ZERO-SKILL JOBS
    # --------------------------------------------------------

    all_job_ids = set(
        jobs_df["job_id"].astype(int)
    )

    extracted_job_ids = set(
        result_df["job_id"].astype(int)
    )

    zero_skill_job_ids = (
        all_job_ids - extracted_job_ids
    )

    print(
        f"\nJobs with zero extracted skills: "
        f"{len(zero_skill_job_ids):,}"
    )

    if zero_skill_job_ids:

        zero_skill_jobs = jobs_df[
            jobs_df["job_id"].isin(
                zero_skill_job_ids
            )
        ][
            [
                "job_id",
                "title"
            ]
        ]

        print("\nZero-skill job titles:")

        print(
            zero_skill_jobs
            .head(30)
            .to_string(index=False)
        )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("NLP V4 PIPELINE FINISHED")
print("=" * 70)

print("\nIMPORTANT:")
print("The old extraction files were NOT modified.")

print(
    "\nNew file created:"
)

print(OUTPUT_FILE)

print(
    "\nDo NOT integrate this into PostgreSQL yet."
)

print(
    "First validate the V4 extraction results."
)