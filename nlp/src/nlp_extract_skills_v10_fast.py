import pandas as pd
import re
import ahocorasick
from sqlalchemy import create_engine


# ============================================================
# CONFIGURATION
# ============================================================

SKILLS_FILE = r"..\..\data\processed\skills_dictionary_clean_v10.csv"

OUTPUT_FILE = r"..\..\data\processed\job_skill_extraction_clean_v10.csv"

DB_URL = (
    "postgresql+psycopg2://"
    "postgres:Postgres%405100"
    "@localhost:5100/"
    "ai_skill_gaps"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text for matching.
    """

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# BOUNDARY CHECK
# ============================================================

def valid_boundary(text, start, end):
    """
    Prevent partial-word matches.

    Example:
        skill = 'java'

    It should match:
        Java
        Java developer

    It should NOT match:
        Javascript
        java123
    """

    # Character before the match
    if start > 0:

        previous_char = text[start - 1]

        if previous_char.isalnum():

            return False


    # Character after the match
    if end < len(text):

        next_char = text[end]

        if next_char.isalnum():

            return False


    return True


# ============================================================
# START
# ============================================================

print("=" * 70)
print("Aho-Corasick NLP SKILL EXTRACTION - V10")
print("=" * 70)


# ============================================================
# LOAD SKILLS
# ============================================================

print()
print("Loading V10 skill dictionary...")

skills_df = pd.read_csv(
    SKILLS_FILE
)

skills_df["skill_name"] = (
    skills_df["skill_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

print(
    f"Clean skills loaded: "
    f"{len(skills_df):,}"
)


# ============================================================
# BUILD AHO-CORASICK AUTOMATON
# ============================================================

print()
print("Building Aho-Corasick matcher...")

automaton = ahocorasick.Automaton()

seen_normalized = set()

duplicate_normalized = 0

rejected_one_character = 0

usable_skills = 0


for _, row in skills_df.iterrows():

    skill_id = int(
        row["skill_id"]
    )

    skill_name = row["skill_name"]

    if not skill_name:

        continue


    normalized_skill = normalize_text(
        skill_name
    )


    # --------------------------------------------------------
    # Reject one-character skills
    # --------------------------------------------------------

    if len(normalized_skill) == 1:

        rejected_one_character += 1

        continue


    # --------------------------------------------------------
    # Duplicate normalized skill
    # --------------------------------------------------------

    if normalized_skill in seen_normalized:

        duplicate_normalized += 1

        continue


    seen_normalized.add(
        normalized_skill
    )


    # --------------------------------------------------------
    # Add skill to automaton
    # --------------------------------------------------------

    automaton.add_word(
        normalized_skill,
        (
            skill_id,
            skill_name,
            normalized_skill
        )
    )

    usable_skills += 1


# Finalize automaton
automaton.make_automaton()


print(
    f"Usable skill patterns: "
    f"{usable_skills:,}"
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
# CONNECT TO POSTGRESQL
# ============================================================

print()
print("Connecting to PostgreSQL...")

engine = create_engine(
    DB_URL
)


# ============================================================
# LOAD JOBS
# ============================================================

print()
print("Loading jobs from PostgreSQL...")

jobs_df = pd.read_sql(
    """
    SELECT
        job_id,
        job_description
    FROM jobs
    ORDER BY job_id
    """,
    engine
)

print(
    f"Jobs loaded: "
    f"{len(jobs_df):,}"
)


# ============================================================
# CHECK DATABASE DATA
# ============================================================

if len(jobs_df) == 0:

    raise ValueError(
        "No jobs were loaded from PostgreSQL."
    )


if "job_id" not in jobs_df.columns:

    raise ValueError(
        "job_id column missing."
    )


if "job_description" not in jobs_df.columns:

    raise ValueError(
        "job_description column missing."
    )


# ============================================================
# EXTRACTION
# ============================================================

print()
print("=" * 70)
print("STARTING AHO-CORASICK EXTRACTION")
print("=" * 70)

records = []

seen_pairs = set()

total_jobs = len(jobs_df)


for index, row in jobs_df.iterrows():

    job_id = int(
        row["job_id"]
    )

    description = row[
        "job_description"
    ]


    # --------------------------------------------------------
    # Skip missing descriptions
    # --------------------------------------------------------

    if pd.isna(description):

        continue


    description = normalize_text(
        description
    )


    if not description:

        continue


    # --------------------------------------------------------
    # Search all skills in ONE PASS
    # --------------------------------------------------------

    for end_index, match_data in automaton.iter(
        description
    ):

        skill_id, skill_name, normalized_skill = match_data


        # ----------------------------------------------------
        # Calculate match start position
        # ----------------------------------------------------

        start_index = (
            end_index -
            len(normalized_skill) +
            1
        )

        end_index_exclusive = (
            end_index + 1
        )


        # ----------------------------------------------------
        # Check word boundaries
        # ----------------------------------------------------

        if not valid_boundary(
            description,
            start_index,
            end_index_exclusive
        ):

            continue


        # ----------------------------------------------------
        # Prevent duplicate job-skill pairs
        # ----------------------------------------------------

        pair = (
            job_id,
            skill_id
        )


        if pair in seen_pairs:

            continue


        seen_pairs.add(
            pair
        )


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

    if (index + 1) % 500 == 0:

        print(
            f"Processed "
            f"{index + 1:,} / "
            f"{total_jobs:,} jobs"
        )


# ============================================================
# CREATE RESULT
# ============================================================

print()
print("Creating result dataframe...")

result_df = pd.DataFrame(
    records,
    columns=[
        "job_id",
        "skill_id",
        "skill_name"
    ]
)


# ============================================================
# SAVE
# ============================================================

print()
print("Saving extraction file...")

result_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# BASIC VALIDATION
# ============================================================

print()
print("=" * 70)
print("EXTRACTION COMPLETED")
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
    f"Unique skills extracted: "
    f"{result_df['skill_id'].nunique():,}"
)


# ============================================================
# DUPLICATE CHECK
# ============================================================

if len(result_df) > 0:

    duplicate_pairs = (
        result_df
        .duplicated(
            subset=[
                "job_id",
                "skill_id"
            ]
        )
        .sum()
    )

else:

    duplicate_pairs = 0


print(
    f"Duplicate job-skill pairs: "
    f"{duplicate_pairs:,}"
)


# ============================================================
# SKILLS PER JOB
# ============================================================

if len(result_df) > 0:

    skills_per_job = (
        result_df
        .groupby("job_id")
        .size()
    )


    print()
    print("=" * 70)
    print("SKILLS PER JOB")
    print("=" * 70)

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

print()
print("=" * 70)
print("SHORT SKILL CHECK")
print("=" * 70)

if len(result_df) > 0:

    short_df = result_df[
        result_df["skill_name"]
        .str.len()
        <= 2
    ]

    print(
        f"Skills <= 2 characters: "
        f"{len(short_df):,}"
    )

    if len(short_df) > 0:

        print()

        print(
            short_df[
                "skill_name"
            ]
            .value_counts()
            .head(30)
            .to_string()
        )


# ============================================================
# TECHNICAL SKILL CHECK
# ============================================================

print()
print("=" * 70)
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


for skill in technical_skills:

    if len(result_df) == 0:

        count = 0

    else:

        count = (
            result_df[
                "skill_name"
            ]
            .str.lower()
            .eq(
                skill.lower()
            )
            .sum()
        )

    print(
        f"{skill}: {count:,}"
    )


# ============================================================
# TOP 30 SKILLS
# ============================================================

print()
print("=" * 70)
print("TOP 30 EXTRACTED SKILLS")
print("=" * 70)

if len(result_df) > 0:

    top_skills = (
        result_df[
            "skill_name"
        ]
        .value_counts()
        .head(30)
    )

    for skill, count in top_skills.items():

        print(
            f"{skill}: {count:,}"
        )


# ============================================================
# ZERO-SKILL JOBS
# ============================================================

print()
print("=" * 70)
print("ZERO-SKILL JOB CHECK")
print("=" * 70)

all_job_ids = set(
    jobs_df[
        "job_id"
    ]
    .astype(int)
)

jobs_with_skills = set(
    result_df[
        "job_id"
    ]
    .astype(int)
)

zero_skill_jobs = (
    all_job_ids -
    jobs_with_skills
)

print(
    f"Total jobs: "
    f"{len(all_job_ids):,}"
)

print(
    f"Jobs with at least one skill: "
    f"{len(jobs_with_skills):,}"
)

print(
    f"Jobs with zero extracted skills: "
    f"{len(zero_skill_jobs):,}"
)


# ============================================================
# HIGH-SKILL JOB CHECK
# ============================================================

print()
print("=" * 70)
print("HIGH-SKILL JOB CHECK")
print("=" * 70)

if len(result_df) > 0:

    jobs_over_100 = (
        skills_per_job[
            skills_per_job > 100
        ]
    )

    print(
        f"Jobs with more than 100 skills: "
        f"{len(jobs_over_100):,}"
    )


# ============================================================
# PROBLEMATIC JOB CHECK
# ============================================================

print()
print("=" * 70)
print("PROBLEMATIC JOB CHECK")
print("=" * 70)

problem_job_id = 240925000000

problem_job = result_df[
    result_df["job_id"]
    == problem_job_id
]

print(
    f"Job ID: {problem_job_id}"
)

print(
    f"Extracted skills: "
    f"{len(problem_job):,}"
)

if len(problem_job) > 0:

    print()

    print(
        problem_job[
            [
                "skill_id",
                "skill_name"
            ]
        ]
        .to_string(
            index=False
        )
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("OUTPUT")
print("=" * 70)

print(
    "File saved:"
)

print(
    OUTPUT_FILE
)

print()
print(
    "PostgreSQL was NOT modified."
)

print("=" * 70)
print("DONE")
print("=" * 70)