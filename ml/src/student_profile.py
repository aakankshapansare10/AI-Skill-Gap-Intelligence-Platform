import pandas as pd
from skill_matching import calculate_skill_match


print("=" * 60)
print("PERSONALIZED STUDENT SKILL GAP ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# LOAD JOB DATA
# ------------------------------------------------------------

input_path = "ml/outputs/job_skill_dataset.csv"

df = pd.read_csv(input_path)

print("Total jobs loaded:", len(df))


# ------------------------------------------------------------
# STUDENT INPUT
# ------------------------------------------------------------

student_skills_input = input(
    "\nEnter your skills separated by comma: "
).strip()

target_role = input(
    "Enter your target job role: "
).strip()


student_skills = [
    skill.strip()
    for skill in student_skills_input.split(",")
    if skill.strip()
]


print()
print("=" * 60)
print("STUDENT PROFILE")
print("=" * 60)

print("Target Role:", target_role)
print("Student Skills:", student_skills)


# ------------------------------------------------------------
# FIND TARGET ROLE JOBS
# ------------------------------------------------------------

role_words = target_role.lower().split()

role_mask = df["job_title"].fillna("").str.lower().apply(
    lambda title: all(word in title for word in role_words)
)

role_jobs = df[role_mask].copy()


print()
print("Matching target-role jobs:", len(role_jobs))


if len(role_jobs) == 0:

    print()
    print("No jobs found for this target role.")
    print("Try a broader role name.")

    exit()


# ------------------------------------------------------------
# CALCULATE MATCHING FOR TARGET ROLE JOBS
# ------------------------------------------------------------

results = []

for _, row in role_jobs.iterrows():

    required_skills = [
        skill.strip()
        for skill in str(row["required_skills"]).split("|")
        if skill.strip()
    ]

    result = calculate_skill_match(
        student_skills,
        required_skills
    )

    results.append({
        "job_id": row["job_id"],
        "job_title": row["job_title"],
        "matching_skills": result["matching_skills"],
        "missing_skills": result["missing_skills"],
        "skill_gap_percentage": result["skill_gap_percentage"],
        "job_match_score": result["job_match_score"]
    })


results_df = pd.DataFrame(results)


# ------------------------------------------------------------
# BEST JOB MATCH
# ------------------------------------------------------------

results_df = results_df.sort_values(
    by="job_match_score",
    ascending=False
)

best_job = results_df.iloc[0]


# ------------------------------------------------------------
# COLLECT ALL MISSING SKILLS
# ------------------------------------------------------------

from collections import Counter

missing_skill_counter = Counter()

for skills in results_df["missing_skills"]:

    for skill in skills:

        missing_skill_counter[skill] += 1


# ------------------------------------------------------------
# RECOMMENDED SKILLS
# ------------------------------------------------------------

recommended_skills = [
    skill
    for skill, count
    in missing_skill_counter.most_common(10)
]


# ------------------------------------------------------------
# FINAL STUDENT REPORT
# ------------------------------------------------------------

best_matching_skills = best_job["matching_skills"]
best_missing_skills = best_job["missing_skills"]


print()
print("=" * 60)
print("FINAL PERSONALIZED REPORT")
print("=" * 60)

print()
print("Target Role:")
print(target_role)

print()
print("Student Skills:")
print(", ".join(student_skills))

print()
print("Best Matching Job:")
print(best_job["job_title"])

print()
print("Matching Skills:")
print(", ".join(best_matching_skills))

print()
print("Missing Skills:")
print(", ".join(best_missing_skills))

print()
print("Skill Gap Percentage:")
print(str(best_job["skill_gap_percentage"]) + "%")

print()
print("Job Match Score:")
print(str(round(best_job["job_match_score"] * 100, 2)) + "%")

print()
print("Top Recommended Skills:")

for i, skill in enumerate(recommended_skills, start=1):

    print(str(i) + ".", skill)


# ------------------------------------------------------------
# SAVE FINAL REPORT
# ------------------------------------------------------------

report = pd.DataFrame([{
    "target_role": target_role,
    "student_skills": ", ".join(student_skills),
    "best_matching_job": best_job["job_title"],
    "matching_skills": ", ".join(best_matching_skills),
    "missing_skills": ", ".join(best_missing_skills),
    "skill_gap_percentage": best_job["skill_gap_percentage"],
    "job_match_score": round(
        best_job["job_match_score"] * 100,
        2
    ),
    "recommended_skills": ", ".join(
        recommended_skills
    )
}])


output_path = "ml/outputs/final_student_report.csv"

report.to_csv(
    output_path,
    index=False
)


print()
print("=" * 60)
print("FINAL REPORT SAVED")
print("=" * 60)

print("File:", output_path)