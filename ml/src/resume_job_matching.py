import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STUDENT_SKILLS_PATH = (
    PROJECT_ROOT / "ml" / "outputs" / "student_extracted_skills.csv"
)

JOB_DATA_PATH = (
    PROJECT_ROOT / "ml" / "outputs" / "job_skill_dataset.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "ml" / "outputs" / "resume_job_matching_results.csv"
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    if pd.isna(text):
        return ""

    return " ".join(str(text).strip().lower().split())


SKILL_ALIASES = {
    "data analyst": "data analysis",
    "data analytics": "data analysis",
    "data analysis": "data analysis",
    "business intelligence": "business intelligence",
    "bi": "business intelligence",
    "powerbi": "power bi",
    "power bi": "power bi",
    "machinelearning": "machine learning",
    "machine learning": "machine learning",
    "python programming": "python",
    "sql programming": "sql",
    "statistical analysis": "statistics",
    "statistics": "statistics",
    "data visualization": "visualization",
    "data visualisation": "visualization",
    "visualization": "visualization",
    "microsoft excel": "excel",
    "postgres": "postgresql",
    "natural language processing": "natural language processing",
    "nlp": "natural language processing",
    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",
    "ml": "machine learning",
}


def normalize_skill(skill):
    skill = normalize(skill)
    return SKILL_ALIASES.get(skill, skill)


# ============================================================
# GENERIC TERMS TO EXCLUDE
# ============================================================

NOISY_SKILLS = {
    "and", "or", "the", "with", "using", "subject",
    "access", "vision", "enterprise", "discipline",
    "functions", "usage", "flexible", "test", "clean",
    "driving", "culture", "zones", "physical", "trust",
    "partner", "document", "insights", "intelligence",
    "languages", "methodologies", "recommendations",
    "skilled", "evaluate", "reliability", "efficiency",
    "feedback", "unit", "measurement", "collect",
    "enhancements", "assurance", "quality standards",
    "strong analytical", "meet deadlines", "product managers",
    "customer experience", "cross-functional",
    "senior analyst", "business analyst", "senior data analyst",
    "and reporting", "university", "btech", "b.tech",
    "degree", "bachelor", "master", "masters", "education",
    "qualification", "solid", "strong", "good", "excellent",
    "ability", "abilities", "experience", "years", "year",
    "knowledge", "skills", "technical skills", "responsibilities",
    "requirements", "qualifications", "strategy", "vision",
    "mission", "innovation", "usability", "workflows",
    "use cases", "doctors", "medical", "health", "healthcare",
    "amex", "analytics", "programming", "programming languages",
    "consistency", "cleaning", "economics",
}


def is_valid_skill(skill):
    skill = normalize_skill(skill)

    if not skill or skill == "nan":
        return False

    if skill in NOISY_SKILLS:
        return False

    if len(skill) <= 2 and skill not in {
        "ai", "ml", "bi", "qa", "hr", "r"
    }:
        return False

    return True


# ============================================================
# LOAD STUDENT SKILLS
# ============================================================

def load_student_skills():
    if not STUDENT_SKILLS_PATH.exists():
        raise FileNotFoundError(
            f"Student skills file not found: {STUDENT_SKILLS_PATH}"
        )

    student_df = pd.read_csv(STUDENT_SKILLS_PATH)

    if "skill_name" not in student_df.columns:
        raise ValueError(
            "student_extracted_skills.csv must contain 'skill_name'."
        )

    skills = set()

    for skill in student_df["skill_name"].dropna():
        normalized = normalize_skill(skill)

        if is_valid_skill(normalized):
            skills.add(normalized)

    return skills


# ============================================================
# LOAD JOB DATA
# ============================================================

def load_job_data():
    if not JOB_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Job dataset not found: {JOB_DATA_PATH}"
        )

    job_df = pd.read_csv(JOB_DATA_PATH)

    required_columns = [
        "job_id",
        "job_title",
        "required_skills",
    ]

    for column in required_columns:
        if column not in job_df.columns:
            raise ValueError(
                f"Missing required column in job dataset: {column}"
            )

    return job_df


# ============================================================
# ROLE FILTERING
# ============================================================

def filter_target_role(job_df, target_role):
    target_role_normalized = normalize(target_role)

    # First try matching the complete phrase in the title.
    exact_phrase_matches = job_df[
        job_df["job_title"]
        .fillna("")
        .astype(str)
        .map(normalize)
        .str.contains(target_role_normalized, regex=False)
    ].copy()

    if not exact_phrase_matches.empty:
        return exact_phrase_matches

    # If the complete phrase is absent, try all role words.
    role_words = target_role_normalized.split()

    if not role_words:
        return job_df.copy()

    def matches_all_words(title):
        title = normalize(title)
        return all(word in title for word in role_words)

    word_matches = job_df[
        job_df["job_title"]
        .fillna("")
        .astype(str)
        .map(matches_all_words)
    ].copy()

    if not word_matches.empty:
        return word_matches

    print(
        "\nWARNING: No matching job titles found for the target role."
    )
    print("Using the complete job dataset as a fallback.")

    return job_df.copy()


# ============================================================
# MATCHING ENGINE
# ============================================================

def calculate_job_match(student_skills, required_skills_text):
    job_skills = set()

    if pd.notna(required_skills_text):
        for skill in str(required_skills_text).split("|"):
            normalized = normalize_skill(skill)

            if is_valid_skill(normalized):
                job_skills.add(normalized)

    matching_skills = student_skills.intersection(job_skills)
    missing_skills = job_skills.difference(student_skills)

    total_required = len(job_skills)
    matching_count = len(matching_skills)
    missing_count = len(missing_skills)

    if total_required == 0:
        return None

    # Both percentages use the same denominator.
    match_percentage = matching_count / total_required * 100
    gap_percentage = missing_count / total_required * 100

    return {
        "total_job_skills": total_required,
        "matching_skills": " | ".join(sorted(matching_skills)),
        "missing_skills": " | ".join(sorted(missing_skills)),
        "matching_skill_count": matching_count,
        "missing_skill_count": missing_count,
        "job_match_percentage": round(match_percentage, 2),
        "skill_gap_percentage": round(gap_percentage, 2),
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("RESUME TO JOB SKILL MATCHING")
    print("=" * 70)

    student_skills = load_student_skills()

    print(f"\nUnique valid resume skills: {len(student_skills)}")
    print("Resume skills:", ", ".join(sorted(student_skills)))

    target_role = input("\nEnter target role: ").strip()

    if not target_role:
        raise ValueError("Target role cannot be empty.")

    job_df = load_job_data()

    print(f"\nTotal jobs in dataset: {len(job_df)}")

    matching_job_df = filter_target_role(job_df, target_role)

    print(f"Jobs selected for analysis: {len(matching_job_df)}")

    results = []

    for _, row in matching_job_df.iterrows():
        calculated = calculate_job_match(
            student_skills,
            row["required_skills"],
        )

        # Skip jobs with no valid required skills.
        if calculated is None:
            continue

        results.append({
            "job_id": row["job_id"],
            "job_title": str(row["job_title"]).strip(),
            **calculated,
        })

    results_df = pd.DataFrame(results)

    if results_df.empty:
        print("\nNo jobs with valid required skills were found.")
        results_df.to_csv(OUTPUT_PATH, index=False)
        return

    # Sort by score, then by the number of matching skills.
    results_df = results_df.sort_values(
        by=[
            "job_match_percentage",
            "matching_skill_count",
            "total_job_skills",
        ],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_PATH, index=False)

    print("\n" + "=" * 70)
    print("TOP 10 JOB MATCHES")
    print("=" * 70)

    display_columns = [
        "job_title",
        "total_job_skills",
        "matching_skill_count",
        "missing_skill_count",
        "job_match_percentage",
        "skill_gap_percentage",
    ]

    print(
        results_df[display_columns]
        .head(10)
        .to_string(index=False)
    )

    # Validate that match and gap percentages add up.
    percentage_sum = (
        results_df["job_match_percentage"]
        + results_df["skill_gap_percentage"]
    )

    invalid_rows = results_df[
        (percentage_sum - 100).abs() > 0.02
    ]

    if not invalid_rows.empty:
        print(
            "\nWARNING: Some rows have inconsistent percentages."
        )
    else:
        print(
            "\nValidation passed: match % + skill gap % = 100%."
        )

    print(f"\nJobs analyzed: {len(results_df)}")
    print(f"Output saved to: {OUTPUT_PATH}")
    print("\nResume job matching completed successfully.")


if __name__ == "__main__":
    main()