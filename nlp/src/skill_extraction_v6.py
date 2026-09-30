import os
import re
import pandas as pd
import psycopg2
import ahocorasick


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform"

DICTIONARY_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills_dictionary_clean_v6.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "job_skill_extraction_clean_v6.csv"
)


# ============================================================
# POSTGRESQL CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5100,
    "database": "ai_skill_gaps",
    "user": "postgres",
    "password": "Postgres@5100"
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = text.replace("’", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(skill):

    return normalize_text(skill)


# ============================================================
# LOAD V6 DICTIONARY
# ============================================================

print("=" * 70)
print("NLP SKILL EXTRACTION - V6")
print("=" * 70)

print("\nLoading V6 skill dictionary:")
print(DICTIONARY_FILE)

skills_df = pd.read_csv(DICTIONARY_FILE)

skills_df = skills_df[
    ["skill_id", "skill_name"]
].dropna(
    subset=["skill_id", "skill_name"]
)

print(
    f"\nClean V6 skills loaded: "
    f"{len(skills_df):,}"
)


# ============================================================
# PREPARE AHO-CORASICK AUTOMATON
# ============================================================

automaton = ahocorasick.Automaton()

normalized_seen = set()

rejected_one_character = 0
duplicate_normalized = 0

for _, row in skills_df.iterrows():

    skill_id = int(row["skill_id"])

    skill_name = str(
        row["skill_name"]
    ).strip()

    normalized = normalize_skill(
        skill_name
    )

    if not normalized:
        continue

    # --------------------------------------------------------
    # Reject one-character alphabetic skills
    # --------------------------------------------------------

    if (
        len(normalized) == 1
        and normalized.isalpha()
    ):
        rejected_one_character += 1
        continue

    # --------------------------------------------------------
    # Avoid duplicate normalized patterns
    # --------------------------------------------------------

    if normalized in normalized_seen:

        duplicate_normalized += 1

        continue

    normalized_seen.add(normalized)

    # --------------------------------------------------------
    # Store:
    #
    # skill_name
    # skill_id
    # normalized pattern
    # --------------------------------------------------------

    automaton.add_word(
        normalized,
        (
            skill_id,
            skill_name,
            normalized
        )
    )


# Build automaton

automaton.make_automaton()


print(
    f"Usable skill patterns: "
    f"{len(normalized_seen):,}"
)

print(
    f"Rejected one-character skills: "
    f"{rejected_one_character:,}"
)

print(
    f"Duplicate normalized patterns ignored: "
    f"{duplicate_normalized:,}"
)


# ============================================================
# SKILL EXTRACTION FUNCTION
# ============================================================

def extract_skills(text):

    text = normalize_text(text)

    if not text:
        return []

    found = {}

    text_length = len(text)

    # --------------------------------------------------------
    # Aho-Corasick searches all patterns efficiently
    # --------------------------------------------------------

    for end_index, data in automaton.iter(text):

        skill_id, skill_name, pattern = data

        start_index = (
            end_index
            - len(pattern)
            + 1
        )

        # ----------------------------------------------------
        # Boundary checking
        #
        # Prevent:
        # sql inside mysql
        #
        # Allow:
        # machine learning
        # c++
        # node.js
        # ----------------------------------------------------

        before_ok = True
        after_ok = True

        if start_index > 0:

            previous_char = text[
                start_index - 1
            ]

            current_char = pattern[0]

            if (
                previous_char.isalnum()
                and current_char.isalnum()
            ):

                before_ok = False

        if end_index < text_length - 1:

            next_char = text[
                end_index + 1
            ]

            last_char = pattern[-1]

            if (
                next_char.isalnum()
                and last_char.isalnum()
            ):

                after_ok = False

        if not (
            before_ok
            and after_ok
        ):

            continue

        found[skill_id] = skill_name

    return [
        (
            skill_id,
            skill_name
        )
        for skill_id, skill_name
        in found.items()
    ]


# ============================================================
# CONNECT TO POSTGRESQL
# ============================================================

print("\nConnecting to PostgreSQL...")

connection = psycopg2.connect(
    **DB_CONFIG
)


# ============================================================
# LOAD JOBS
# ============================================================

query = """
SELECT
    job_id,
    title,
    job_description
FROM jobs
ORDER BY job_id;
"""

jobs_df = pd.read_sql(
    query,
    connection
)

connection.close()

print(
    f"Jobs loaded: "
    f"{len(jobs_df):,}"
)


# ============================================================
# EXTRACT SKILLS
# ============================================================

records = []

total_jobs = len(jobs_df)

print("\nStarting extraction...\n")


for index, row in jobs_df.iterrows():

    job_id = int(
        row["job_id"]
    )

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

    # --------------------------------------------------------
    # Combine title + description
    # --------------------------------------------------------

    combined_text = (
        f"{title} {description}"
    )

    extracted = extract_skills(
        combined_text
    )

    for skill_id, skill_name in extracted:

        records.append(
            {
                "job_id": job_id,
                "skill_id": skill_id,
                "skill_name": skill_name
            }
        )

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if (
        (index + 1) % 1000 == 0
        or index + 1 == total_jobs
    ):

        print(
            f"Processed "
            f"{index + 1:,}/"
            f"{total_jobs:,} jobs..."
        )


# ============================================================
# CREATE RESULT DATAFRAME
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

before_duplicates = len(
    result_df
)

result_df = result_df.drop_duplicates(
    subset=[
        "job_id",
        "skill_id"
    ]
)

duplicate_pairs = (
    before_duplicates
    - len(result_df)
)


# ============================================================
# SAVE OUTPUT
# ============================================================

os.makedirs(
    os.path.dirname(
        OUTPUT_FILE
    ),
    exist_ok=True
)

result_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# VALIDATION STATISTICS
# ============================================================

total_records = len(
    result_df
)

unique_jobs = result_df[
    "job_id"
].nunique()

unique_skills = result_df[
    "skill_id"
].nunique()


if total_records > 0:

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )

    min_skills = (
        skills_per_job.min()
    )

    max_skills = (
        skills_per_job.max()
    )

    avg_skills = (
        skills_per_job.mean()
    )

    median_skills = (
        skills_per_job.median()
    )

else:

    min_skills = 0
    max_skills = 0
    avg_skills = 0
    median_skills = 0


# ============================================================
# SHORT SKILL CHECK
# ============================================================

if total_records > 0:

    short_df = result_df[
        result_df[
            "skill_name"
        ]
        .astype(str)
        .str.len()
        <= 2
    ]

else:

    short_df = pd.DataFrame()


# ============================================================
# RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("V6 EXTRACTION COMPLETED")
print("=" * 70)

print(
    f"\nClean V6 skills loaded: "
    f"{len(skills_df):,}"
)

print(
    f"Usable skill patterns: "
    f"{len(normalized_seen):,}"
)

print(
    f"Rejected one-character skills: "
    f"{rejected_one_character:,}"
)

print(
    f"Duplicate normalized patterns ignored: "
    f"{duplicate_normalized:,}"
)

print(
    f"\nJobs loaded: "
    f"{len(jobs_df):,}"
)

print(
    f"Total extraction records: "
    f"{total_records:,}"
)

print(
    f"Unique jobs with skills: "
    f"{unique_jobs:,}"
)

print(
    f"Unique skills extracted: "
    f"{unique_skills:,}"
)

print(
    f"Duplicate job-skill pairs: "
    f"{duplicate_pairs:,}"
)

print("\nSkills/job:")

print(
    f"  Min    : "
    f"{min_skills}"
)

print(
    f"  Max    : "
    f"{max_skills}"
)

print(
    f"  Average: "
    f"{avg_skills:.2f}"
)

print(
    f"  Median : "
    f"{median_skills:.0f}"
)

print(
    f"\nSkills <= 2 characters: "
    f"{len(short_df):,}"
)


# ============================================================
# SHORT SKILL FREQUENCIES
# ============================================================

if len(short_df) > 0:

    print("\nShort skills:")

    short_counts = (
        short_df[
            "skill_name"
        ]
        .value_counts()
        .head(20)
    )

    for skill, count in (
        short_counts.items()
    ):

        print(
            f"  {skill}: {count}"
        )


# ============================================================
# TOP 30 SKILLS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 30 EXTRACTED SKILLS")
print("=" * 70)

if total_records > 0:

    top_skills = (
        result_df[
            "skill_name"
        ]
        .value_counts()
        .head(30)
    )

    for skill, count in (
        top_skills.items()
    ):

        print(
            f"{skill}: {count}"
        )


# ============================================================
# PROBLEMATIC JOB CHECK
# ============================================================

problem_job_id = 240925000000

problem_job = result_df[
    result_df[
        "job_id"
    ]
    == problem_job_id
]

print("\n")
print("=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)

print(
    f"Job ID: "
    f"{problem_job_id}"
)

print(
    f"Extracted skills: "
    f"{len(problem_job)}"
)

if len(problem_job) > 0:

    print("\nSkills:")

    for _, row in (
        problem_job.iterrows()
    ):

        print(
            f"  {row['skill_id']} "
            f"{row['skill_name']}"
        )


# ============================================================
# ZERO-SKILL JOBS
# ============================================================

jobs_with_skills = set(
    result_df[
        "job_id"
    ].unique()
)

all_jobs = set(
    jobs_df[
        "job_id"
    ].unique()
)

zero_skill_jobs = sorted(
    all_jobs
    - jobs_with_skills
)

print("\n")
print("=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)

print(
    f"Jobs with zero extracted skills: "
    f"{len(zero_skill_jobs):,}"
)

if zero_skill_jobs:

    zero_df = jobs_df[
        jobs_df[
            "job_id"
        ].isin(zero_skill_jobs)
    ][
        [
            "job_id",
            "title"
        ]
    ]

    print(
        "\nZero-skill job titles:"
    )

    for _, row in (
        zero_df.head(20).iterrows()
    ):

        print(
            f"  {row['job_id']} - "
            f"{row['title']}"
        )


# ============================================================
# OUTPUT
# ============================================================

print("\n")
print("=" * 70)
print("OUTPUT FILE")
print("=" * 70)

print(
    OUTPUT_FILE
)

print(
    "\nPostgreSQL was NOT modified."
)

print(
    "V1-V5 extraction files were NOT modified."
)

print("=" * 70)