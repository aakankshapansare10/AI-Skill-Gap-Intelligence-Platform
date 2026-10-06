import pandas as pd
from collections import Counter


print("=" * 60)
print("LOADING JOB MATCHING RESULTS")
print("=" * 60)

input_path = "ml/outputs/job_matching_results.csv"

df = pd.read_csv(input_path)

print("Total jobs:", len(df))


# ------------------------------------------------------------
# EXTRACT MISSING SKILLS
# ------------------------------------------------------------

skill_counter = Counter()

for skills in df["missing_skills"].fillna(""):

    if skills.strip() == "":
        continue

    missing = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    skill_counter.update(missing)


# ------------------------------------------------------------
# CREATE SKILL GAP DATAFRAME
# ------------------------------------------------------------

skill_gap_data = []

for skill, count in skill_counter.items():

    skill_gap_data.append({
        "skill": skill,
        "jobs_requiring_skill": count
    })


skill_gap_df = pd.DataFrame(skill_gap_data)


# ------------------------------------------------------------
# CALCULATE DEMAND PERCENTAGE
# ------------------------------------------------------------

if len(df) > 0:

    skill_gap_df["demand_percentage"] = (
        skill_gap_df["jobs_requiring_skill"]
        / len(df)
        * 100
    )

else:

    skill_gap_df["demand_percentage"] = 0


# ------------------------------------------------------------
# PRIORITY
# ------------------------------------------------------------

def assign_priority(percentage):

    if percentage >= 30:
        return "High"

    elif percentage >= 15:
        return "Medium"

    else:
        return "Low"


skill_gap_df["priority"] = (
    skill_gap_df["demand_percentage"]
    .apply(assign_priority)
)


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
print("TOP SKILL GAPS")
print("=" * 60)

print(
    skill_gap_df.head(20).to_string(index=False)
)


# ------------------------------------------------------------
# SAVE OUTPUT
# ------------------------------------------------------------

output_path = "ml/outputs/skill_gap_analysis.csv"

skill_gap_df.to_csv(
    output_path,
    index=False
)


print()
print("=" * 60)
print("SKILL GAP ANALYSIS SAVED")
print("=" * 60)

print("File:", output_path)
print("Total unique missing skills:", len(skill_gap_df))