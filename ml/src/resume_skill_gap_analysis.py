import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

MATCHING_RESULTS_PATH = (
    "ml/outputs/resume_job_matching_results.csv"
)

OUTPUT_PATH = (
    "ml/outputs/resume_skill_gap_analysis.csv"
)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("=" * 70)
print("RESUME SKILL GAP ANALYSIS")
print("=" * 70)

print("\nLoading resume-job matching results...")

df = pd.read_csv(
    MATCHING_RESULTS_PATH
)

print(
    "Jobs loaded:",
    len(df)
)


# ------------------------------------------------------------
# EXTRACT MISSING SKILLS
# ------------------------------------------------------------

skill_counts = {}


for _, row in df.iterrows():

    missing_skills = str(
        row["missing_skills"]
    )

    if (
        missing_skills == ""
        or missing_skills.lower() == "nan"
    ):
        continue

    skills = missing_skills.split("|")

    for skill in skills:

        skill = skill.strip()

        if skill == "":
            continue

        skill_counts[skill] = (
            skill_counts.get(skill, 0) + 1
        )


# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

gap_df = pd.DataFrame(
    [
        {
            "skill_name": skill,
            "jobs_requiring_skill": count
        }

        for skill, count
        in skill_counts.items()
    ]
)


# ------------------------------------------------------------
# CALCULATE PERCENTAGE
# ------------------------------------------------------------

total_jobs = len(df)

if total_jobs > 0:

    gap_df["demand_percentage"] = (
        gap_df["jobs_requiring_skill"]
        / total_jobs
    ) * 100

else:

    gap_df["demand_percentage"] = 0


# ------------------------------------------------------------
# SORT
# ------------------------------------------------------------

gap_df = gap_df.sort_values(
    by=[
        "jobs_requiring_skill",
        "demand_percentage"
    ],
    ascending=False
)


# ------------------------------------------------------------
# ADD RANK
# ------------------------------------------------------------

gap_df.insert(
    0,
    "rank",
    range(
        1,
        len(gap_df) + 1
    )
)


# ------------------------------------------------------------
# ROUND
# ------------------------------------------------------------

gap_df["demand_percentage"] = (
    gap_df["demand_percentage"]
    .round(2)
)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

gap_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY TOP 20
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP MISSING SKILLS")
print("=" * 70)

print(
    gap_df.head(20).to_string(
        index=False
    )
)


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SKILL GAP ANALYSIS COMPLETE")
print("=" * 70)

print(
    "\nUnique missing skills:",
    len(gap_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)