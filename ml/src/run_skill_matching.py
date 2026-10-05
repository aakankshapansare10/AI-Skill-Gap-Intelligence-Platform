import pandas as pd
from skill_matching import calculate_skill_match


print("=" * 60)
print("LOADING JOB DATASET")
print("=" * 60)

input_path = "ml/outputs/job_skill_dataset.csv"

df = pd.read_csv(input_path)

print("Total jobs loaded:", len(df))


# ------------------------------------------------------------
# STUDENT SKILLS
# ------------------------------------------------------------

student_skills = [
    "Python",
    "SQL",
    "Excel",
    "Machine Learning"
]

print()
print("=" * 60)
print("STUDENT SKILLS")
print("=" * 60)

print(student_skills)


# ------------------------------------------------------------
# CONVERT REQUIRED SKILLS
# ------------------------------------------------------------

df["required_skills"] = df["required_skills"].fillna("")

df["required_skills"] = df["required_skills"].apply(
    lambda x: [
        skill.strip()
        for skill in x.split("|")
        if skill.strip()
    ]
)


# ------------------------------------------------------------
# CALCULATE MATCHING FOR EVERY JOB
# ------------------------------------------------------------

results = []

print()
print("=" * 60)
print("CALCULATING SKILL MATCHING")
print("=" * 60)

for _, row in df.iterrows():

    result = calculate_skill_match(
        student_skills,
        row["required_skills"]
    )

    results.append({
        "job_id": row["job_id"],
        "job_title": row["job_title"],
        "student_skills": ", ".join(student_skills),
        "required_skills": ", ".join(row["required_skills"]),
        "matching_skills": ", ".join(result["matching_skills"]),
        "missing_skills": ", ".join(result["missing_skills"]),
        "skill_gap_percentage": result["skill_gap_percentage"],
        "job_match_score": result["job_match_score"]
    })


# ------------------------------------------------------------
# CREATE RESULT DATAFRAME
# ------------------------------------------------------------

result_df = pd.DataFrame(results)


print()
print("=" * 60)
print("MATCHING COMPLETED")
print("=" * 60)

print("Total jobs processed:", len(result_df))


# ------------------------------------------------------------
# SORT BY BEST JOB MATCH
# ------------------------------------------------------------

result_df = result_df.sort_values(
    by="job_match_score",
    ascending=False
)


# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

output_path = "ml/outputs/job_matching_results.csv"

result_df.to_csv(
    output_path,
    index=False
)


print()
print("=" * 60)
print("TOP 10 MATCHING JOBS")
print("=" * 60)

print(
    result_df[
        [
            "job_id",
            "job_title",
            "matching_skills",
            "missing_skills",
            "skill_gap_percentage",
            "job_match_score"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print()
print("=" * 60)
print("RESULT SAVED")
print("=" * 60)

print("File:", output_path)
print("Rows:", len(result_df))
print("Columns:", list(result_df.columns))