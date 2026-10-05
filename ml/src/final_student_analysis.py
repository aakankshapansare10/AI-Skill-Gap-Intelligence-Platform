import pandas as pd
import json
import os


# ============================================================
# PATHS
# ============================================================

STUDENT_SKILLS_PATH = (
    "ml/outputs/student_extracted_skills.csv"
)

MATCHING_PATH = (
    "ml/outputs/resume_job_matching_results.csv"
)

RECOMMENDATION_PATH = (
    "ml/outputs/resume_top_job_recommendations.csv"
)

GAP_PATH = (
    "ml/outputs/resume_skill_gap_analysis.csv"
)

TARGET_ROLE_PATH = (
    "ml/outputs/resume_target_role_analysis.csv"
)

CSV_OUTPUT = (
    "ml/outputs/final_student_analysis.csv"
)

JSON_OUTPUT = (
    "ml/outputs/final_student_analysis.json"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("FINAL STUDENT ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD STUDENT SKILLS
# ============================================================

student_df = pd.read_csv(
    STUDENT_SKILLS_PATH
)

student_skills = (
    student_df["skill_name"]
    .dropna()
    .astype(str)
    .tolist()
)

print(
    "\nStudent skills:",
    len(student_skills)
)


# ============================================================
# LOAD JOB MATCHING
# ============================================================

matching_df = pd.read_csv(
    MATCHING_PATH
)

print(
    "Jobs analyzed:",
    len(matching_df)
)


# ============================================================
# OVERALL MATCH SCORE
# ============================================================

if len(matching_df) > 0:

    best_match_score = (
        matching_df[
            "job_match_percentage"
        ].max()
    )

    average_match_score = (
        matching_df[
            "job_match_percentage"
        ].mean()
    )

    average_skill_gap = (
        matching_df[
            "skill_gap_percentage"
        ].mean()
    )

else:

    best_match_score = 0
    average_match_score = 0
    average_skill_gap = 0


# ============================================================
# TOP JOB RECOMMENDATIONS
# ============================================================

recommendation_df = pd.read_csv(
    RECOMMENDATION_PATH
)

top_jobs = []


for _, row in recommendation_df.head(10).iterrows():

    top_jobs.append({

        "rank":
            int(row["recommendation_rank"]),

        "job_id":
            str(row["job_id"]),

        "job_title":
            str(row["job_title"]),

        "matching_skill_count":
            int(row["matching_skill_count"]),

        "job_match_percentage":
            float(
                row["job_match_percentage"]
            ),

        "skill_gap_percentage":
            float(
                row["skill_gap_percentage"]
            ),

        "matching_skills":
            str(
                row["matching_skills"]
            ),

        "missing_skills":
            str(
                row["missing_skills"]
            )
    })


# ============================================================
# TOP MISSING SKILLS
# ============================================================

gap_df = pd.read_csv(
    GAP_PATH
)

top_missing_skills = []


for _, row in gap_df.head(20).iterrows():

    top_missing_skills.append({

        "skill_name":
            str(row["skill_name"]),

        "jobs_requiring_skill":
            int(
                row["jobs_requiring_skill"]
            ),

        "demand_percentage":
            float(
                row["demand_percentage"]
            )
    })


# ============================================================
# TARGET ROLE
# ============================================================

target_df = pd.read_csv(
    TARGET_ROLE_PATH
)

if len(target_df) > 0:

    target_role = str(
        target_df[
            "target_role"
        ].iloc[0]
    )

else:

    target_role = ""


# ============================================================
# TARGET ROLE MISSING SKILLS
# ============================================================

target_missing_df = target_df[
    target_df[
        "student_has_skill"
    ].astype(str).str.lower() == "no"
].copy()

target_missing_skills = []


for _, row in target_missing_df.head(20).iterrows():

    target_missing_skills.append({

        "skill_name":
            str(row["skill_name"]),

        "jobs_requiring_skill":
            int(
                row["jobs_requiring_skill"]
            ),

        "demand_percentage":
            float(
                row["demand_percentage"]
            ),

        "priority":
            str(row["priority"])
    })


# ============================================================
# FINAL REPORT
# ============================================================

final_report = {

    "student_profile": {

        "total_skills":
            len(student_skills),

        "skills":
            student_skills
    },


    "overall_analysis": {

        "jobs_analyzed":
            int(len(matching_df)),

        "best_job_match_percentage":
            round(
                float(best_match_score),
                2
            ),

        "average_job_match_percentage":
            round(
                float(average_match_score),
                2
            ),

        "average_skill_gap_percentage":
            round(
                float(average_skill_gap),
                2
            )
    },


    "top_job_recommendations":
        top_jobs,


    "top_missing_skills":
        top_missing_skills,


    "target_role_analysis": {

        "target_role":
            target_role,

        "missing_skills":
            target_missing_skills
    }
}


# ============================================================
# SAVE JSON
# ============================================================

with open(
    JSON_OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        final_report,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# CREATE SUMMARY CSV
# ============================================================

summary_rows = []


for job in top_jobs:

    summary_rows.append({

        "type":
            "job_recommendation",

        "rank":
            job["rank"],

        "name":
            job["job_title"],

        "match_percentage":
            job[
                "job_match_percentage"
            ],

        "skill_gap_percentage":
            job[
                "skill_gap_percentage"
            ],

        "details":
            job["missing_skills"]
    })


for skill in top_missing_skills:

    summary_rows.append({

        "type":
            "missing_skill",

        "rank":
            "",

        "name":
            skill["skill_name"],

        "match_percentage":
            "",

        "skill_gap_percentage":
            "",

        "details":
            skill[
                "jobs_requiring_skill"
            ]
    })


final_csv_df = pd.DataFrame(
    summary_rows
)

final_csv_df.to_csv(
    CSV_OUTPUT,
    index=False
)


# ============================================================
# DISPLAY FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL STUDENT REPORT")
print("=" * 70)

print(
    "\nTarget Role:",
    target_role
)

print(
    "Student Skills:",
    len(student_skills)
)

print(
    "Jobs Analyzed:",
    len(matching_df)
)

print(
    "Best Job Match:",
    round(
        float(best_match_score),
        2
    ),
    "%"
)

print(
    "Average Job Match:",
    round(
        float(average_match_score),
        2
    ),
    "%"
)

print(
    "Average Skill Gap:",
    round(
        float(average_skill_gap),
        2
    ),
    "%"
)


print("\nTop Recommended Jobs:")

for job in top_jobs[:5]:

    print(
        f"{job['rank']}. "
        f"{job['job_title']} "
        f"TO {job['job_match_percentage']}%"
    )


print("\nTop Missing Skills:")

for skill in top_missing_skills[:10]:

    print(
        f"- {skill['skill_name']} "
        f"TO {skill['demand_percentage']}% job demand"
    )


print("\n" + "=" * 70)
print("FINAL PIPELINE COMPLETE")
print("=" * 70)

print(
    "\nCSV:",
    CSV_OUTPUT
)

print(
    "JSON:",
    JSON_OUTPUT
)