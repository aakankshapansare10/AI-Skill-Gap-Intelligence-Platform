from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_predictions.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_analysis.csv"
)


# ============================================================
# 2. LOAD SKILL GAP PREDICTIONS
# ============================================================

print("Loading skill gap predictions...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. STUDENT SKILLS
# ============================================================

student_skills = [
    "Python",
    "SQL",
    "Excel",
    "Communication"
]

print("\n========================================")
print("STUDENT SKILLS")
print("========================================")
print(student_skills)


# ============================================================
# 4. FUNCTION TO CLEAN SKILLS
# ============================================================

def clean_skills(skill_text):

    if pd.isna(skill_text):
        return []

    skills = [
        skill.strip()
        for skill in str(skill_text).split(",")
        if skill.strip()
    ]

    non_skill_terms = {
        "senior",
        "junior",
        "lead",
        "executive",
        "manager",
        "assistant",
        "associate",
        "intern",
        "trainee"
    }

    cleaned = []
    seen = set()

    for skill in skills:

        skill_clean = skill.strip()
        skill_lower = skill_clean.lower()

        # Remove job designation terms
        if skill_lower in non_skill_terms:
            continue

        # Remove duplicate skills ignoring capitalization
        if skill_lower not in seen:
            cleaned.append(skill_clean)
            seen.add(skill_lower)

    return cleaned


# ============================================================
# 5. FUNCTION TO ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(required_skills, student_skills):

    required_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    student_set = {
        skill.lower().strip()
        for skill in student_skills
    }

    matching = required_set.intersection(student_set)

    missing = required_set - student_set

    total_required = len(required_set)
    total_matching = len(matching)
    total_missing = len(missing)

    if total_required > 0:
        gap_percentage = (
            total_missing / total_required
        ) * 100
    else:
        gap_percentage = 0

    return (
        matching,
        missing,
        total_required,
        total_matching,
        total_missing,
        round(gap_percentage, 2)
    )


# ============================================================
# 6. PERFORM SKILL GAP ANALYSIS
# ============================================================

print("\nPerforming skill gap analysis...")

analysis_results = []

for _, row in df.iterrows():

    job_title = row["job_title"]

    required_skills = clean_skills(
        row["required_skills"]
    )

    (
        matching,
        missing,
        total_required,
        total_matching,
        total_missing,
        gap_percentage
    ) = analyze_skill_gap(
        required_skills,
        student_skills
    )

    analysis_results.append(
        {
            "job_title": job_title,

            "student_skills":
                ", ".join(student_skills),

            "required_skills":
                ", ".join(
                    sorted(required_skills)
                ),

            "matching_skills":
                ", ".join(
                    sorted(matching)
                ),

            "missing_skills":
                ", ".join(
                    sorted(missing)
                ),

            "total_required_skills":
                total_required,

            "total_matching_skills":
                total_matching,

            "total_missing_skills":
                total_missing,

            "skill_gap_percentage":
                gap_percentage
        }
    )


# ============================================================
# 7. CREATE DATAFRAME
# ============================================================

analysis_df = pd.DataFrame(
    analysis_results
)


# ============================================================
# 8. SAVE OUTPUT
# ============================================================

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("SKILL GAP ANALYSIS RESULTS")
print("========================================")

for i in range(
    min(5, len(analysis_df))
):

    row = analysis_df.iloc[i]

    print("\n----------------------------------------")

    print(
        "Target Job:",
        row["job_title"]
    )

    print(
        "\nStudent Skills:"
    )

    print(
        row["student_skills"]
    )

    print(
        "\nRequired Skills:"
    )

    print(
        row["required_skills"]
    )

    print(
        "\nMatching Skills:"
    )

    print(
        row["matching_skills"]
    )

    print(
        "\nMissing Skills:"
    )

    print(
        row["missing_skills"]
    )

    print(
        "\nSkill Gap:"
    )

    print(
        f"{row['skill_gap_percentage']}%"
    )


# ============================================================
# 10. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("SKILL GAP ANALYSIS COMPLETED")
print("========================================")

print("\nOutput file:")

print(OUTPUT_FILE)