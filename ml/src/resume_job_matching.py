import pandas as pd
import os


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

STUDENT_SKILLS_PATH = (
    "ml/outputs/student_extracted_skills.csv"
)

JOB_DATA_PATH = (
    "ml/outputs/job_skill_dataset.csv"
)

OUTPUT_PATH = (
    "ml/outputs/resume_job_matching_results.csv"
)


# ------------------------------------------------------------
# SKILL NORMALIZATION
# ------------------------------------------------------------

def normalize_skill(skill):

    return (
        str(skill)
        .strip()
        .lower()
    )


# ------------------------------------------------------------
# LOAD STUDENT SKILLS
# ------------------------------------------------------------

print("=" * 70)
print("RESUME TO JOB SKILL MATCHING")
print("=" * 70)

print("\nLoading extracted resume skills...")

student_df = pd.read_csv(
    STUDENT_SKILLS_PATH
)

student_skills = set(
    student_df["skill_name"]
    .dropna()
    .astype(str)
    .map(normalize_skill)
)

student_skills.discard("")

print(
    "Student skills found:",
    len(student_skills)
)

print("\nStudent skills:")

for skill in sorted(student_skills):

    print("-", skill)


# ------------------------------------------------------------
# LOAD JOB DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("Loading NLP job-skill dataset...")
print("=" * 70)

job_df = pd.read_csv(
    JOB_DATA_PATH
)

print(
    "Total jobs:",
    len(job_df)
)


# ------------------------------------------------------------
# CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = [
    "job_id",
    "job_title",
    "required_skills",
    "number_of_skills"
]

for column in required_columns:

    if column not in job_df.columns:

        raise ValueError(
            f"Missing column: {column}"
        )


# ------------------------------------------------------------
# JOB MATCHING
# ------------------------------------------------------------

results = []

print("\nMatching resume skills with jobs...")

for _, row in job_df.iterrows():

    job_id = row["job_id"]

    job_title = row["job_title"]

    required_skills_text = (
        str(row["required_skills"])
    )

    # Split skills using |
    job_skills = set(
        normalize_skill(skill)
        for skill in
        required_skills_text.split("|")
    )

    job_skills.discard("")

    # --------------------------------------------------------
    # MATCHING SKILLS
    # --------------------------------------------------------

    matching_skills = (
        student_skills
        .intersection(job_skills)
    )

    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    missing_skills = (
        job_skills
        .difference(student_skills)
    )

    total_job_skills = len(
        job_skills
    )

    matching_count = len(
        matching_skills
    )

    missing_count = len(
        missing_skills
    )

    # --------------------------------------------------------
    # MATCH PERCENTAGE
    # --------------------------------------------------------

    if total_job_skills > 0:

        job_match_percentage = (
            matching_count
            / total_job_skills
        ) * 100

        skill_gap_percentage = (
            missing_count
            / total_job_skills
        ) * 100

    else:

        job_match_percentage = 0

        skill_gap_percentage = 0


    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    results.append({

        "job_id": job_id,

        "job_title": job_title,

        "total_job_skills":
            total_job_skills,

        "matching_skills":
            " | ".join(
                sorted(matching_skills)
            ),

        "missing_skills":
            " | ".join(
                sorted(missing_skills)
            ),

        "matching_skill_count":
            matching_count,

        "missing_skill_count":
            missing_count,

        "job_match_percentage":
            round(
                job_match_percentage,
                2
            ),

        "skill_gap_percentage":
            round(
                skill_gap_percentage,
                2
            )
    })


# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

results_df = pd.DataFrame(
    results
)


# ------------------------------------------------------------
# SORT BEST MATCHES FIRST
# ------------------------------------------------------------

results_df = results_df.sort_values(
    by=[
        "job_match_percentage",
        "matching_skill_count"
    ],
    ascending=False
)


# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY TOP 10
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 JOB MATCHES")
print("=" * 70)

print(
    results_df[
        [
            "job_id",
            "job_title",
            "matching_skill_count",
            "job_match_percentage",
            "skill_gap_percentage"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUME JOB MATCHING COMPLETE")
print("=" * 70)

print(
    "\nTotal jobs processed:",
    len(results_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)