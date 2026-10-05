import os
import re
import pandas as pd
import ahocorasick
from sqlalchemy import create_engine


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DICT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v11.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_skill_extraction_clean_v11.csv"
)


# ============================================================
# POSTGRESQL
# ============================================================

DB_URL = (
    "postgresql+psycopg2://"
    "postgres:Postgres%405100"
    "@localhost:5100/"
    "ai_skill_gaps"
)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("_", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# CHECK WHETHER MATCH IS A REAL WORD/PHRASE
# ============================================================

def valid_boundary(text, start, end, pattern):

    # Characters immediately before and after the match
    before = text[start - 1] if start > 0 else " "
    after = text[end + 1] if end + 1 < len(text) else " "

    # --------------------------------------------------------
    # For normal alphabetic words:
    # require word boundaries
    # --------------------------------------------------------

    if pattern[0].isalnum() and pattern[-1].isalnum():

        if before.isalnum():
            return False

        if after.isalnum():
            return False

    return True


# ============================================================
# LOAD DICTIONARY
# ============================================================

print("=" * 70)
print("Aho-Corasick NLP SKILL EXTRACTION - V11 FIXED")
print("=" * 70)

print("\nLoading V11 skill dictionary...")

skills_df = pd.read_csv(DICT_FILE)

required_columns = {
    "skill_id",
    "skill_name",
    "canonical_skill_name"
}

missing_columns = required_columns - set(skills_df.columns)

if missing_columns:

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


skills_df["skill_name_normalized"] = (
    skills_df["skill_name"]
    .fillna("")
    .astype(str)
    .map(normalize_text)
)

skills_df["canonical_skill_name"] = (
    skills_df["canonical_skill_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)


skills_df = skills_df[
    (skills_df["skill_name_normalized"] != "") &
    (skills_df["canonical_skill_name"] != "")
].copy()


print(
    f"V11 dictionary rows loaded: "
    f"{len(skills_df):,}"
)


# ============================================================
# BUILD CANONICAL REPRESENTATIVE MAP
# ============================================================

print("\nBuilding canonical skill mapping...")

canonical_map = {}

for _, row in skills_df.iterrows():

    canonical = row["canonical_skill_name"]

    if canonical not in canonical_map:

        canonical_map[canonical] = {
            "skill_id": int(row["skill_id"]),
            "skill_name": canonical
        }


print(
    f"Canonical skills: "
    f"{len(canonical_map):,}"
)


# ============================================================
# BUILD AHO-CORASICK AUTOMATON
# ============================================================

print("\nBuilding Aho-Corasick matcher...")

automaton = ahocorasick.Automaton()

pattern_to_canonical = {}

duplicate_patterns = 0
rejected_short = 0


for _, row in skills_df.iterrows():

    pattern = row["skill_name_normalized"]
    canonical = row["canonical_skill_name"]

    # Reject one-character alphabetic patterns
    if len(pattern) == 1 and pattern.isalpha():

        rejected_short += 1
        continue

    # Ignore duplicate normalized aliases
    if pattern in pattern_to_canonical:

        duplicate_patterns += 1
        continue

    pattern_to_canonical[pattern] = canonical

    automaton.add_word(
        pattern,
        (pattern, canonical)
    )


automaton.make_automaton()


print(
    f"Usable skill patterns: "
    f"{len(pattern_to_canonical):,}"
)

print(
    f"Rejected one-character patterns: "
    f"{rejected_short:,}"
)

print(
    f"Duplicate normalized patterns ignored: "
    f"{duplicate_patterns:,}"
)


# ============================================================
# LOAD JOBS
# ============================================================

print("\nConnecting to PostgreSQL...")

engine = create_engine(DB_URL)

print("Loading jobs from PostgreSQL...")

jobs_df = pd.read_sql(
    """
    SELECT
        job_id,
        job_description
    FROM jobs
    WHERE job_description IS NOT NULL
    ORDER BY job_id
    """,
    engine
)


print(
    f"Jobs loaded: "
    f"{len(jobs_df):,}"
)


# ============================================================
# EXTRACTION
# ============================================================

print("\n" + "=" * 70)
print("STARTING V11 FIXED AHO-CORASICK EXTRACTION")
print("=" * 70)


results = []

total_jobs = len(jobs_df)


for index, row in jobs_df.iterrows():

    job_id = int(row["job_id"])

    description = normalize_text(
        row["job_description"]
    )

    if not description:
        continue


    # One canonical skill only once per job
    matched_canonical = set()


    for end_index, value in automaton.iter(description):

        pattern, canonical = value

        start_index = (
            end_index -
            len(pattern) +
            1
        )


        # ----------------------------------------------------
        # IMPORTANT:
        # Reject substring matches.
        # ----------------------------------------------------

        if not valid_boundary(
            description,
            start_index,
            end_index,
            pattern
        ):
            continue


        matched_canonical.add(canonical)


    # --------------------------------------------------------
    # Save canonical skills
    # --------------------------------------------------------

    for canonical in matched_canonical:

        representative = canonical_map.get(
            canonical
        )

        if representative is None:
            continue


        results.append(
            {
                "job_id": job_id,
                "skill_id": representative["skill_id"],
                "skill_name": canonical,
                "canonical_skill_name": canonical
            }
        )


    if (index + 1) % 500 == 0:

        print(
            f"Processed "
            f"{index + 1:,} / "
            f"{total_jobs:,} jobs"
        )


# ============================================================
# RESULT DATAFRAME
# ============================================================

print("\nCreating result dataframe...")

result_df = pd.DataFrame(
    results,
    columns=[
        "job_id",
        "skill_id",
        "skill_name",
        "canonical_skill_name"
    ]
)


# Remove duplicate job-skill pairs
result_df = result_df.drop_duplicates(
    subset=[
        "job_id",
        "skill_id"
    ]
)


if not result_df.empty:

    result_df = result_df.sort_values(
        [
            "job_id",
            "canonical_skill_name"
        ]
    )


# ============================================================
# SAVE
# ============================================================

print("\nSaving extraction file...")

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# BASIC VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("V11 FIXED EXTRACTION COMPLETED")
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


duplicate_pairs = result_df.duplicated(
    subset=[
        "job_id",
        "skill_id"
    ]
).sum()


print(
    f"Duplicate job-skill pairs: "
    f"{duplicate_pairs:,}"
)


# ============================================================
# SKILLS PER JOB
# ============================================================

print("\n" + "=" * 70)
print("SKILLS PER JOB")
print("=" * 70)


if not result_df.empty:

    skills_per_job = (
        result_df
        .groupby("job_id")
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
# SHORT SKILL CHECK
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILL CHECK")
print("=" * 70)


if not result_df.empty:

    short_df = result_df[
        result_df[
            "canonical_skill_name"
        ]
        .astype(str)
        .str.len()
        <= 2
    ]


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


# ============================================================
# TECHNICAL SKILL CHECK
# ============================================================

print("\n" + "=" * 70)
print("TECHNICAL SKILL EXTRACTION CHECK")
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
    "Natural Language Processing",
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

        print(
            f"{skill}: "
            f"{skill_counts.get(skill, 0):,}"
        )


# ============================================================
# TOP 30
# ============================================================

print("\n" + "=" * 70)
print("TOP 30 EXTRACTED CANONICAL SKILLS")
print("=" * 70)


if not result_df.empty:

    print(
        result_df[
            "canonical_skill_name"
        ]
        .value_counts()
        .head(30)
        .to_string()
    )


# ============================================================
# ZERO SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)


all_job_ids = set(
    jobs_df[
        "job_id"
    ]
    .astype(int)
)


extracted_job_ids = set(
    result_df[
        "job_id"
    ]
    .astype(int)
) if not result_df.empty else set()


zero_skill_jobs = (
    all_job_ids -
    extracted_job_ids
)


print(
    f"Total jobs: "
    f"{len(all_job_ids):,}"
)

print(
    f"Jobs with at least one skill: "
    f"{len(extracted_job_ids):,}"
)

print(
    f"Jobs with zero extracted skills: "
    f"{len(zero_skill_jobs):,}"
)


# ============================================================
# HIGH SKILL JOBS
# ============================================================

print("\n" + "=" * 70)
print("HIGH-SKILL JOB CHECK")
print("=" * 70)


if not result_df.empty:

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )


    high_skill_jobs = (
        skills_per_job > 100
    ).sum()


    print(
        f"Jobs with more than 100 skills: "
        f"{high_skill_jobs:,}"
    )


# ============================================================
# PROBLEMATIC JOB
# ============================================================

print("\n" + "=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)


problem_job_id = 240925000000


problem_job = result_df[
    result_df[
        "job_id"
    ] == problem_job_id
]


print(
    f"Job ID: "
    f"{problem_job_id}"
)


print(
    f"Extracted skills: "
    f"{len(problem_job)}"
)


if not problem_job.empty:

    print(
        problem_job[
            [
                "skill_id",
                "skill_name",
                "canonical_skill_name"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT")
print("=" * 70)


print(
    f"File saved:\n"
    f"{OUTPUT_FILE}"
)


print(
    "\nPostgreSQL was NOT modified."
)


print("=" * 70)
print("DONE")
print("=" * 70)