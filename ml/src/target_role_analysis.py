import pandas as pd


print("=" * 60)
print("TARGET ROLE SKILL GAP ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# LOAD JOB MATCHING RESULTS
# ------------------------------------------------------------

input_path = "ml/outputs/job_matching_results.csv"

df = pd.read_csv(input_path)

print("Total jobs loaded:", len(df))


# ------------------------------------------------------------
# TARGET ROLE
# ------------------------------------------------------------

target_role = input(
    "\nEnter target job role: "
).strip()


print()
print("Target Role:", target_role)


# ------------------------------------------------------------
# FILTER JOBS
# ------------------------------------------------------------

role_words = target_role.lower().split()

role_mask = df["job_title"].fillna("").str.lower().apply(
    lambda title: all(word in title for word in role_words)
)

role_jobs = df[role_mask].copy()


print()
print("=" * 60)
print("TARGET ROLE JOBS")
print("=" * 60)

print("Matching jobs found:", len(role_jobs))


# ------------------------------------------------------------
# CHECK IF JOBS EXIST
# ------------------------------------------------------------

if len(role_jobs) == 0:

    print()
    print("No matching jobs found for this target role.")
    print("Try a broader role name such as:")
    print("Data Analyst")
    print("Software Engineer")
    print("Java Developer")
    print("Python Developer")

    exit()


# ------------------------------------------------------------
# DISPLAY SAMPLE JOBS
# ------------------------------------------------------------

print()
print("Sample matching jobs:")

print(
    role_jobs[
        [
            "job_id",
            "job_title",
            "job_match_score",
            "skill_gap_percentage"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# COLLECT MISSING SKILLS
# ------------------------------------------------------------

from collections import Counter

skill_counter = Counter()

for skills in role_jobs["missing_skills"].fillna(""):

    if skills.strip() == "":
        continue

    missing_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    skill_counter.update(missing_skills)


# ------------------------------------------------------------
# CREATE SKILL GAP DATA
# ------------------------------------------------------------

skill_gap_data = []

for skill, count in skill_counter.items():

    skill_gap_data.append({
        "target_role": target_role,
        "skill": skill,
        "jobs_requiring_skill": count,
        "total_target_role_jobs": len(role_jobs),
        "demand_percentage": round(
            (count / len(role_jobs)) * 100,
            2
        )
    })


skill_gap_df = pd.DataFrame(skill_gap_data)


# ------------------------------------------------------------
# SORT BY DEMAND
# ------------------------------------------------------------

skill_gap_df = skill_gap_df.sort_values(
    by="jobs_requiring_skill",
    ascending=False
)


# ------------------------------------------------------------
# DISPLAY TOP SKILL GAPS
# ------------------------------------------------------------

print()
print("=" * 60)
print("TOP SKILL GAPS FOR TARGET ROLE")
print("=" * 60)

if len(skill_gap_df) > 0:

    print(
        skill_gap_df.head(20).to_string(index=False)
    )

else:

    print("No missing skills found.")


# ------------------------------------------------------------
# SAVE RESULT
# ------------------------------------------------------------

output_path = "ml/outputs/target_role_skill_gap.csv"

skill_gap_df.to_csv(
    output_path,
    index=False
)


print()
print("=" * 60)
print("TARGET ROLE ANALYSIS COMPLETED")
print("=" * 60)

print("Target Role:", target_role)
print("Matching Jobs:", len(role_jobs))
print("Unique Skill Gaps:", len(skill_gap_df))
print("Output:", output_path)