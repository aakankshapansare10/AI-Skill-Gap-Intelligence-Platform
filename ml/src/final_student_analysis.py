import json
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

STUDENT_SKILLS_PATH = OUTPUT_DIR / "student_extracted_skills.csv"
MATCHING_PATH = OUTPUT_DIR / "resume_job_matching_results.csv"
RECOMMENDATION_PATH = OUTPUT_DIR / "resume_top_job_recommendations.csv"
GAP_PATH = OUTPUT_DIR / "resume_skill_gap_analysis.csv"
TARGET_ROLE_PATH = OUTPUT_DIR / "resume_target_role_analysis.csv"

CSV_OUTPUT = OUTPUT_DIR / "final_student_analysis.csv"
JSON_OUTPUT = OUTPUT_DIR / "final_student_analysis.json"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_csv(path):
    """Load a CSV safely and report a useful error if missing."""
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Run the resume analysis pipeline first."
        )

    return pd.read_csv(path)


def safe_text(value, default=""):
    """Convert a value to clean text."""
    if pd.isna(value):
        return default

    return str(value).strip()


def safe_number(value, default=0):
    """Convert a value to a number safely."""
    try:
        if pd.isna(value):
            return default

        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    """Convert a value to an integer safely."""
    return int(safe_number(value, default))


def split_skills(value):
    """Convert pipe-separated or comma-separated skills into a list."""
    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null"}:
        return []

    if "|" in text:
        parts = text.split("|")
    else:
        parts = text.split(",")

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def unique_skills(skills):
    """Remove duplicate skills without changing their original order."""
    result = []
    seen = set()

    for skill in skills:
        cleaned = safe_text(skill)

        if not cleaned:
            continue

        key = cleaned.casefold()

        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result


# ============================================================
# START
# ============================================================

print("=" * 70)
print("FINAL STUDENT ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD STUDENT SKILLS
# ============================================================

student_df = load_csv(STUDENT_SKILLS_PATH)

if "skill_name" not in student_df.columns:
    raise ValueError(
        "student_extracted_skills.csv must contain 'skill_name'."
    )

student_skills = unique_skills(
    student_df["skill_name"].dropna().astype(str).tolist()
)

student_skill_set = {
    skill.casefold()
    for skill in student_skills
}

print("\nStudent skills:", len(student_skills))


# ============================================================
# LOAD JOB MATCHING RESULTS
# ============================================================

matching_df = load_csv(MATCHING_PATH)

print("Jobs analyzed:", len(matching_df))


# ============================================================
# OVERALL JOB MATCH STATISTICS
# ============================================================

if not matching_df.empty:
    match_values = pd.to_numeric(
        matching_df.get(
            "job_match_percentage",
            pd.Series(dtype=float)
        ),
        errors="coerce"
    ).dropna()

    gap_values = pd.to_numeric(
        matching_df.get(
            "skill_gap_percentage",
            pd.Series(dtype=float)
        ),
        errors="coerce"
    ).dropna()

    best_match_score = (
        float(match_values.max())
        if not match_values.empty
        else 0.0
    )

    average_match_score = (
        float(match_values.mean())
        if not match_values.empty
        else 0.0
    )

    average_skill_gap = (
        float(gap_values.mean())
        if not gap_values.empty
        else 0.0
    )

else:
    best_match_score = 0.0
    average_match_score = 0.0
    average_skill_gap = 0.0


# ============================================================
# TOP JOB RECOMMENDATIONS
# ============================================================

recommendation_df = load_csv(RECOMMENDATION_PATH)

top_jobs = []

for rank, (_, row) in enumerate(
    recommendation_df.head(10).iterrows(),
    start=1
):
    top_jobs.append({
        "rank": safe_int(
            row.get("recommendation_rank", rank),
            rank
        ),
        "job_id": safe_text(row.get("job_id")),
        "job_title": safe_text(row.get("job_title")),
        "matching_skill_count": safe_int(
            row.get("matching_skill_count", 0)
        ),
        "job_match_percentage": round(
            safe_number(row.get("job_match_percentage", 0)),
            2
        ),
        "skill_gap_percentage": round(
            safe_number(row.get("skill_gap_percentage", 0)),
            2
        ),
        "matching_skills": split_skills(
            row.get("matching_skills", "")
        ),
        "missing_skills": split_skills(
            row.get("missing_skills", "")
        )
    })


# ============================================================
# OVERALL MISSING SKILLS
# ============================================================

gap_df = load_csv(GAP_PATH)

top_missing_skills = []

for _, row in gap_df.head(20).iterrows():
    top_missing_skills.append({
        "skill_name": safe_text(row.get("skill_name")),
        "jobs_requiring_skill": safe_int(
            row.get("jobs_requiring_skill", 0)
        ),
        "demand_percentage": round(
            safe_number(row.get("demand_percentage", 0)),
            2
        )
    })


# ============================================================
# TARGET ROLE ANALYSIS
# ============================================================

target_df = load_csv(TARGET_ROLE_PATH)

required_columns = {
    "target_role",
    "skill_name",
    "student_has_skill"
}

missing_columns = required_columns - set(target_df.columns)

if missing_columns:
    raise ValueError(
        "resume_target_role_analysis.csv is missing columns: "
        + ", ".join(sorted(missing_columns))
    )


# Use the role actually stored in the target-role analysis CSV.
if not target_df.empty:
    target_role = safe_text(
        target_df["target_role"].dropna().iloc[0]
        if target_df["target_role"].notna().any()
        else ""
    )
else:
    target_role = ""


# Remove invalid skill rows and duplicate required skills.
target_df = target_df.copy()

target_df["skill_name"] = (
    target_df["skill_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

target_df = target_df[
    target_df["skill_name"] != ""
].copy()

target_df["_skill_key"] = (
    target_df["skill_name"].str.casefold()
)

target_df = target_df.drop_duplicates(
    subset=["_skill_key"],
    keep="first"
)


# ============================================================
# MATCHED AND MISSING REQUIRED SKILLS
# ============================================================

matched_skill_rows = []
target_missing_skills = []

for _, row in target_df.iterrows():

    skill_name = safe_text(row.get("skill_name"))

    # Use the explicit student_has_skill field from the CSV.
    has_skill_value = safe_text(
        row.get("student_has_skill")
    ).casefold()

    # Also verify against the extracted resume skills.
    # A skill is considered matched only when both sources agree.
    skill_found_in_resume = (
        skill_name.casefold() in student_skill_set
    )

    is_matched = (
        has_skill_value in {"yes", "true", "1"}
        and skill_found_in_resume
    )

    skill_details = {
        "skill_name": skill_name,
        "jobs_requiring_skill": safe_int(
            row.get("jobs_requiring_skill", 0)
        ),
        "demand_percentage": round(
            safe_number(row.get("demand_percentage", 0)),
            2
        ),
        "priority": safe_text(
            row.get("priority", "LOW")
        ).upper()
    }

    if is_matched:
        matched_skill_rows.append(skill_details)

    else:
        target_missing_skills.append(skill_details)


# Highest-demand missing skills first.
target_missing_skills.sort(
    key=lambda item: (
        item["demand_percentage"],
        item["jobs_requiring_skill"]
    ),
    reverse=True
)

matched_skill_count = len(matched_skill_rows)
missing_skill_count = len(target_missing_skills)
total_required_skills = len(target_df)

if total_required_skills > 0:
    target_role_match_percentage = round(
        (matched_skill_count / total_required_skills) * 100,
        2
    )
else:
    target_role_match_percentage = 0.0


print("\nTarget role:", target_role)
print("Required skills:", total_required_skills)
print("Matched required skills:", matched_skill_count)
print("Missing required skills:", missing_skill_count)
print("Target role match:", target_role_match_percentage, "%")


# ============================================================
# FINAL REPORT
# ============================================================

final_report = {
    "student_profile": {
        "total_skills": len(student_skills),
        "skills": student_skills
    },

    "overall_analysis": {
        "jobs_analyzed": int(len(matching_df)),
        "best_job_match_percentage": round(
            best_match_score,
            2
        ),
        "average_job_match_percentage": round(
            average_match_score,
            2
        ),
        "average_skill_gap_percentage": round(
            average_skill_gap,
            2
        )
    },

    "top_job_recommendations": top_jobs,

    "top_missing_skills": top_missing_skills,

    "target_role_analysis": {
        "target_role": target_role,

        "total_required_skills": total_required_skills,

        "matched_skill_count": matched_skill_count,

        "matched_skills": matched_skill_rows,

        "missing_skill_count": missing_skill_count,

        "missing_skills": target_missing_skills,

        "match_percentage": target_role_match_percentage
    }
}


# ============================================================
# SAVE JSON
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

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
        "type": "job_recommendation",
        "rank": job["rank"],
        "name": job["job_title"],
        "match_percentage": job["job_match_percentage"],
        "skill_gap_percentage": job["skill_gap_percentage"],
        "details": " | ".join(job["missing_skills"])
    })

for skill in top_missing_skills:
    summary_rows.append({
        "type": "missing_skill",
        "rank": "",
        "name": skill["skill_name"],
        "match_percentage": "",
        "skill_gap_percentage": "",
        "details": skill["jobs_requiring_skill"]
    })

for skill in matched_skill_rows:
    summary_rows.append({
        "type": "target_role_matched_skill",
        "rank": "",
        "name": skill["skill_name"],
        "match_percentage": target_role_match_percentage,
        "skill_gap_percentage": "",
        "details": skill["priority"]
    })

for skill in target_missing_skills:
    summary_rows.append({
        "type": "target_role_missing_skill",
        "rank": "",
        "name": skill["skill_name"],
        "match_percentage": target_role_match_percentage,
        "skill_gap_percentage": "",
        "details": skill["priority"]
    })

final_csv_df = pd.DataFrame(summary_rows)

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

print("\nTarget Role:", target_role)
print("Student Skills:", len(student_skills))
print("Jobs Analyzed:", len(matching_df))

print(
    "Best Job Match:",
    round(best_match_score, 2),
    "%"
)

print(
    "Average Job Match:",
    round(average_match_score, 2),
    "%"
)

print(
    "Average Skill Gap:",
    round(average_skill_gap, 2),
    "%"
)

print(
    "Target Role Match:",
    target_role_match_percentage,
    "%"
)

print("\nMatched Skills:")
for skill in matched_skill_rows:
    print("-", skill["skill_name"])

print("\nMissing Skills:")
for skill in target_missing_skills[:10]:
    print(
        f"- {skill['skill_name']} "
        f"({skill['priority']}, "
        f"{skill['demand_percentage']}% demand)"
    )

print("\nTop Recommended Jobs:")
for job in top_jobs[:5]:
    print(
        f"{job['rank']}. {job['job_title']} "
        f"-> {job['job_match_percentage']}%"
    )

print("\n" + "=" * 70)
print("FINAL PIPELINE COMPLETE")
print("=" * 70)

print("\nCSV:", CSV_OUTPUT)
print("JSON:", JSON_OUTPUT)