from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

# Current file:
# AI Skill Gap Intelligence Platform/
# └── notebooks/
#     └── 09_skill_gap_analysis.py
#
# parents[0] = notebooks
# parents[1] = AI Skill Gap Intelligence Platform

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "skill_gap_predictions.csv"
)

OUTPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "skill_gap_analysis.csv"
)


# ============================================================
# 2. CHECK INPUT FILE
# ============================================================

print("========================================")
print("AI SKILL GAP ANALYSIS")
print("========================================")

print("\nProject Root:")
print(ROOT)

print("\nInput File:")
print(INPUT_FILE)

print("\nOutput File:")
print(OUTPUT_FILE)


if not INPUT_FILE.exists():
    print("\nERROR: skill_gap_predictions.csv was not found.")
    print("\nExpected location:")
    print(INPUT_FILE)

    print("\nPlease make sure the previous skill gap prediction")
    print("step has created:")
    print("data/processed/skill_gap_predictions.csv")

    raise FileNotFoundError(
        f"\nInput file not found:\n{INPUT_FILE}"
    )


# ============================================================
# 3. LOAD SKILL GAP PREDICTIONS
# ============================================================

print("\nLoading skill gap predictions...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully.")

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "job_title",
    "student_skills",
    "predicted_required_skills"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Required columns are missing.")

    print("\nMissing columns:")
    print(missing_columns)

    print("\nAvailable columns:")
    print(df.columns.tolist())

    raise ValueError(
        f"\nMissing required columns: {missing_columns}"
    )


# ============================================================
# 5. STUDENT SKILLS
# ============================================================

# These should match the skills you want to evaluate
# for the student.

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
# 6. FUNCTION TO CLEAN SKILLS
# ============================================================

def clean_skills(skill_text):

    if pd.isna(skill_text):
        return []

    skills = [
        skill.strip()
        for skill in str(skill_text).split(",")
        if skill.strip()
    ]

    # Remove non-skill job designation terms
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

        if skill_lower in non_skill_terms:
            continue

        if skill_lower not in seen:

            cleaned.append(skill_clean)

            seen.add(skill_lower)

    return cleaned


# ============================================================
# 7. FUNCTION TO ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(required_skills, student_skills):

    # Convert required skills into lowercase sets
    required_set = {
        skill.lower().strip()
        for skill in required_skills
        if skill.strip()
    }

    # Convert student skills into lowercase sets
    student_set = {
        skill.lower().strip()
        for skill in student_skills
        if skill.strip()
    }

    # Matching skills
    matching = required_set.intersection(student_set)

    # Missing skills
    missing = required_set - student_set

    # Counts
    total_required = len(required_set)

    total_matching = len(matching)

    total_missing = len(missing)

    # Skill gap percentage
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
# 8. PERFORM SKILL GAP ANALYSIS
# ============================================================

print("\n========================================")
print("PERFORMING SKILL GAP ANALYSIS")
print("========================================")

analysis_results = []


for _, row in df.iterrows():

    job_title = row["job_title"]

    # Get predicted required skills
    required_skills = clean_skills(
        row["predicted_required_skills"]
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


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

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
# 9. CREATE DATAFRAME
# ============================================================

analysis_df = pd.DataFrame(
    analysis_results
)


# ============================================================
# 10. SAVE OUTPUT
# ============================================================

# Make sure processed folder exists
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 11. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("SKILL GAP ANALYSIS RESULTS")
print("========================================")


if len(analysis_df) > 0:

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
            "\nTotal Required Skills:"
        )

        print(
            row["total_required_skills"]
        )

        print(
            "\nTotal Matching Skills:"
        )

        print(
            row["total_matching_skills"]
        )

        print(
            "\nTotal Missing Skills:"
        )

        print(
            row["total_missing_skills"]
        )

        print(
            "\nSkill Gap:"
        )

        print(
            f"{row['skill_gap_percentage']}%"
        )


else:

    print("\nNo skill gap results were generated.")


# ============================================================
# 12. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("SKILL GAP ANALYSIS COMPLETED")
print("========================================")

print("\nTotal records analyzed:")
print(len(analysis_df))

print("\nOutput file saved to:")
print(OUTPUT_FILE)