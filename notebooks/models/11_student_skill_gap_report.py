from pathlib import Path
import pandas as pd


# ==========================================
# 1. PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "processed" / "recommendations.csv"

OUTPUT_CSV = ROOT / "data" / "processed" / "student_skill_gap_report.csv"
OUTPUT_TXT = ROOT / "data" / "processed" / "student_skill_gap_report.txt"


# ==========================================
# 2. LOAD RECOMMENDATIONS
# ==========================================

print("Loading recommendations...")

df = pd.read_csv(INPUT)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 3. GENERATE STUDENT SKILL GAP REPORT
# ==========================================

print("\nGenerating student skill gap report...")


report_rows = []


for _, row in df.iterrows():

    job_title = row["job_title"]
    student_skills = row["student_skills"]
    missing_skills = row["missing_skills"]
    gap_percentage = row["skill_gap_percentage"]
    recommendations = row["recommendations"]

    # Convert missing skills into list
    if pd.isna(missing_skills) or str(missing_skills).strip() == "":
        missing_list = []
    else:
        missing_list = [
            skill.strip()
            for skill in str(missing_skills).split(",")
            if skill.strip()
        ]

    # Count skills
    total_missing = len(missing_list)

    # Create report
    report_rows.append({
        "job_title": job_title,
        "student_skills": student_skills,
        "missing_skills": missing_skills,
        "total_missing_skills": total_missing,
        "skill_gap_percentage": gap_percentage,
        "recommendations": recommendations
    })


# ==========================================
# 4. CREATE DATAFRAME
# ==========================================

report_df = pd.DataFrame(report_rows)


# ==========================================
# 5. SAVE CSV REPORT
# ==========================================

report_df.to_csv(OUTPUT_CSV, index=False)


# ==========================================
# 6. CREATE TEXT REPORT
# ==========================================

with open(OUTPUT_TXT, "w", encoding="utf-8") as file:

    file.write("=" * 70 + "\n")
    file.write("        AI SKILL GAP INTELLIGENCE REPORT\n")
    file.write("=" * 70 + "\n\n")

    if len(report_df) > 0:

        # Student information
        file.write("STUDENT SKILLS\n")
        file.write("-" * 70 + "\n")
        file.write(str(report_df.iloc[0]["student_skills"]) + "\n\n")

        # Job reports
        for index, row in report_df.iterrows():

            file.write("=" * 70 + "\n")
            file.write(f"TARGET JOB: {row['job_title']}\n")
            file.write("=" * 70 + "\n\n")

            file.write("Student Skills:\n")
            file.write(str(row["student_skills"]) + "\n\n")

            file.write("Missing Skills:\n")
            file.write(str(row["missing_skills"]) + "\n\n")

            file.write("Total Missing Skills:\n")
            file.write(str(row["total_missing_skills"]) + "\n\n")

            file.write("Skill Gap Percentage:\n")
            file.write(str(row["skill_gap_percentage"]) + "%\n\n")

            file.write("Learning Recommendations:\n")
            file.write(str(row["recommendations"]) + "\n\n")


# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("STUDENT SKILL GAP REPORT")
print("========================================")

print("\nFirst 5 reports:\n")

print(
    report_df[
        [
            "job_title",
            "total_missing_skills",
            "skill_gap_percentage"
        ]
    ].head()
)


print("\n========================================")
print("STUDENT SKILL GAP REPORT COMPLETED")
print("========================================")

print(f"\nCSV Report saved to:")
print(OUTPUT_CSV)

print(f"\nText Report saved to:")
print(OUTPUT_TXT)