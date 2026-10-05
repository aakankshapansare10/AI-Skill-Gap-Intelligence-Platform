import pandas as pd


print("=" * 60)
print("LOADING JOB MATCHING RESULTS")
print("=" * 60)

input_path = "ml/outputs/job_matching_results.csv"

df = pd.read_csv(input_path)

print("Total jobs loaded:", len(df))


# ------------------------------------------------------------
# CALCULATE RECOMMENDATION SCORE
# ------------------------------------------------------------

df["recommendation_score"] = (
    df["job_match_score"] * 100
)


# ------------------------------------------------------------
# REMOVE JOBS WITH ZERO MATCH
# ------------------------------------------------------------

recommended_jobs = df[
    df["job_match_score"] > 0
].copy()


# ------------------------------------------------------------
# SORT BEST JOBS FIRST
# ------------------------------------------------------------

recommended_jobs = recommended_jobs.sort_values(
    by=[
        "recommendation_score",
        "skill_gap_percentage"
    ],
    ascending=[
        False,
        True
    ]
)


# ------------------------------------------------------------
# TOP 20 JOBS
# ------------------------------------------------------------

top_jobs = recommended_jobs.head(20)


print()
print("=" * 60)
print("TOP 20 JOB RECOMMENDATIONS")
print("=" * 60)

print(
    top_jobs[
        [
            "job_id",
            "job_title",
            "matching_skills",
            "missing_skills",
            "skill_gap_percentage",
            "job_match_score",
            "recommendation_score"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# SAVE RECOMMENDATIONS
# ------------------------------------------------------------

output_path = "ml/outputs/top_job_recommendations.csv"

top_jobs.to_csv(
    output_path,
    index=False
)


print()
print("=" * 60)
print("RECOMMENDATIONS SAVED")
print("=" * 60)

print("File:", output_path)
print("Number of recommendations:", len(top_jobs))