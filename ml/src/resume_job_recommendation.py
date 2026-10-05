import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

INPUT_PATH = (
    "ml/outputs/resume_job_matching_results.csv"
)

OUTPUT_PATH = (
    "ml/outputs/resume_top_job_recommendations.csv"
)


# ------------------------------------------------------------
# LOAD MATCHING RESULTS
# ------------------------------------------------------------

print("=" * 70)
print("RESUME TO TOP JOB RECOMMENDATIONS")
print("=" * 70)

print("\nLoading resume-job matching results...")

df = pd.read_csv(
    INPUT_PATH
)

print(
    "Jobs available:",
    len(df)
)


# ------------------------------------------------------------
# REMOVE EMPTY / INVALID JOBS
# ------------------------------------------------------------

df = df[
    df["total_job_skills"] > 0
].copy()


# ------------------------------------------------------------
# SORT JOBS
# ------------------------------------------------------------

df = df.sort_values(
    by=[
        "job_match_percentage",
        "matching_skill_count"
    ],
    ascending=False
)


# ------------------------------------------------------------
# TOP 20 JOBS
# ------------------------------------------------------------

top_jobs = df.head(20).copy()


# ------------------------------------------------------------
# ADD RANK
# ------------------------------------------------------------

top_jobs.insert(
    0,
    "recommendation_rank",
    range(
        1,
        len(top_jobs) + 1
    )
)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

top_jobs.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 20 RECOMMENDED JOBS")
print("=" * 70)

print(
    top_jobs[
        [
            "recommendation_rank",
            "job_title",
            "matching_skill_count",
            "job_match_percentage",
            "skill_gap_percentage"
        ]
    ].to_string(index=False)
)


print("\n" + "=" * 70)
print("RECOMMENDATION COMPLETE")
print("=" * 70)

print(
    "\nOutput file:",
    OUTPUT_PATH
)