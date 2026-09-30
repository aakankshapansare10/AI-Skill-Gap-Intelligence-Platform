from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_recommendations.csv"
)

OUTPUT_CSV = (
    ROOT / "data" / "processed"
    / "student_skill_gap_report.csv"
)

OUTPUT_TXT = (
    ROOT / "data" / "processed"
    / "student_skill_gap_report.txt"
)


# ============================================================
# 2. LOAD RECOMMENDATION DATA
# ============================================================

print("Loading recommendation data...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. NON-SKILL TERMS
# ============================================================

NON_SKILL_TERMS = {
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


# ============================================================
# 4. CLEAN SKILL LIST
# ============================================================

def clean_skill_list(skill_text):

    if pd.isna(skill_text):
        return []

    skill_text = str(skill_text).strip()

    if not skill_text:
        return []

    skills = [
        skill.strip()
        for skill in skill_text.split(",")
        if skill.strip()
    ]

    cleaned = []

    for skill in skills:

        if skill.lower() not in NON_SKILL_TERMS:
            cleaned.append(skill)

    return cleaned


# ============================================================
# 5. CREATE FINAL REPORT
# ============================================================

print("\nGenerating student skill gap report...")

report_rows = []


for _, row in df.iterrows():

    # --------------------------------------------------------
    # Job title
    # --------------------------------------------------------

    job_title = row["job_title"]


    # --------------------------------------------------------
    # Student skills
    # --------------------------------------------------------

    student_skills = clean_skill_list(
        row["student_skills"]
    )


    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing_skills = clean_skill_list(
        row["missing_skills"]
    )


    # --------------------------------------------------------
    # Required skills
    #
    # Step 7 does not contain required_skills.
    # Therefore we reconstruct the required skills from:
    #
    # student skills + missing skills
    # --------------------------------------------------------

    required_skills = []

    for skill in student_skills:

        if skill.lower() not in [
            x.lower()
            for x in required_skills
        ]:

            required_skills.append(skill)


    for skill in missing_skills:

        if skill.lower() not in [
            x.lower()
            for x in required_skills
        ]:

            required_skills.append(skill)


    # --------------------------------------------------------
    # Matching skills
    # --------------------------------------------------------

    student_lower = {
        skill.lower()
        for skill in student_skills
    }

    matching_skills = []

    for skill in required_skills:

        if skill.lower() in student_lower:

            matching_skills.append(skill)


    # --------------------------------------------------------
    # Calculate skill gap
    # --------------------------------------------------------

    total_required = len(
        required_skills
    )

    total_missing = len(
        missing_skills
    )

    if total_required > 0:

        skill_gap = (
            total_missing
            / total_required
        ) * 100

    else:

        skill_gap = 0


    # --------------------------------------------------------
    # Get recommendations from Step 7
    # --------------------------------------------------------

    recommendations = row[
        "recommendations"
    ]

    if pd.isna(recommendations):

        recommendations = ""

    else:

        recommendations = str(
            recommendations
        )


    # --------------------------------------------------------
    # Store report row
    # --------------------------------------------------------

    report_rows.append(
        {
            "job_title":
                job_title,

            "student_skills":
                ", ".join(
                    student_skills
                ),

            "required_skills":
                ", ".join(
                    required_skills
                ),

            "matching_skills":
                ", ".join(
                    matching_skills
                ),

            "missing_skills":
                ", ".join(
                    missing_skills
                ),

            "total_required_skills":
                total_required,

            "total_matching_skills":
                len(
                    matching_skills
                ),

            "total_missing_skills":
                total_missing,

            "skill_gap_percentage":
                round(
                    skill_gap,
                    2
                ),

            "learning_recommendations":
                recommendations
        }
    )


# ============================================================
# 6. CREATE DATAFRAME
# ============================================================

report_df = pd.DataFrame(
    report_rows
)


# ============================================================
# 7. SAVE CSV
# ============================================================

report_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# 8. CREATE READABLE TEXT REPORT
# ============================================================

print("\nCreating readable report...")

with open(
    OUTPUT_TXT,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STUDENT SKILL GAP REPORT\n"
    )

    file.write(
        "=" * 70
    )

    file.write("\n\n")


    # Student skills

    if len(report_df) > 0:

        file.write(
            "Student Skills:\n"
        )

        file.write(
            report_df.iloc[0][
                "student_skills"
            ]
        )

        file.write("\n\n")


    # First 20 jobs

    for i in range(
        min(20, len(report_df))
    ):

        row = report_df.iloc[i]


        file.write(
            "-" * 70
        )

        file.write("\n")


        file.write(
            f"Target Job: "
            f"{row['job_title']}\n\n"
        )


        file.write(
            "Required Skills:\n"
        )

        file.write(
            f"{row['required_skills']}\n\n"
        )


        file.write(
            "Matching Skills:\n"
        )

        file.write(
            f"{row['matching_skills']}\n\n"
        )


        file.write(
            "Missing Skills:\n"
        )

        file.write(
            f"{row['missing_skills']}\n\n"
        )


        file.write(
            "Skill Gap:\n"
        )

        file.write(
            f"{row['skill_gap_percentage']}%\n\n"
        )


        file.write(
            "Learning Recommendations:\n"
        )

        if row[
            "learning_recommendations"
        ]:

            file.write(
                row[
                    "learning_recommendations"
                ]
            )

        else:

            file.write(
                "No additional skills identified."
            )

        file.write("\n\n")


# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("STUDENT SKILL GAP REPORT")
print("========================================")


for i in range(
    min(5, len(report_df))
):

    row = report_df.iloc[i]


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


    print(
        "\nLearning Recommendations:"
    )

    print(
        row[
            "learning_recommendations"
        ]
    )


# ============================================================
# 10. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("STUDENT SKILL GAP REPORT COMPLETED")
print("========================================")

print("\nCSV report:")
print(OUTPUT_CSV)

print("\nReadable text report:")
print(OUTPUT_TXT)