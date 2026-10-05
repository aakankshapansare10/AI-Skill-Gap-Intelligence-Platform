import os
import re
import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

SKILL_DICTIONARY_PATH = (
    "data/processed/skills_dictionary_clean_v13.csv"
)


OUTPUT_PATH = (
    "ml/outputs/student_extracted_skills.csv"
)


# ------------------------------------------------------------
# SKILLS THAT ARE TOO GENERIC TO BE USEFUL ALONE
# ------------------------------------------------------------

GENERIC_SKILLS = {
    "machine",
    "learning",
    "data",
    "analysis",
    "analytics",
    "technology",
    "technologies",
    "development",
    "developer",
    "programming",
    "languages",
    "test",
    "testing",
    "management",
    "business",
    "digital",
    "predictive",
    "insights",
    "intelligence",
    "risk",
    "health",
    "voice",
    "frameworks",
    "methodologies",
    "datasets",
    "large datasets",
    "dashboards"
}


# ------------------------------------------------------------
# SKILL ALIASES / CLEANUP
# ------------------------------------------------------------

SKILL_ALIASES = {
    "bi": "Power BI",
    "power bi": "Power BI",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "python": "Python",
    "sql": "SQL",
    "excel": "Excel",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "statistics": "Statistics",
    "tableau": "Tableau",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analytics",
    "business intelligence": "Business Intelligence"
}


# ------------------------------------------------------------
# READ RESUME TEXT FILE
# ------------------------------------------------------------

def extract_resume_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


# ------------------------------------------------------------
# NORMALIZE TEXT
# ------------------------------------------------------------

def normalize_text(text):

    text = text.lower()

    # Convert slash-separated combinations into spaces.
    # Example: Python/SQL -> Python SQL
    text = re.sub(
        r"[/|]",
        " ",
        text
    )

    # Keep letters, numbers, #, +, dot, hyphen and spaces
    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ------------------------------------------------------------
# CLEAN SKILL NAME
# ------------------------------------------------------------

def clean_skill_name(skill):

    skill = str(skill).strip()

    if not skill:
        return None

    normalized = normalize_text(skill)

    if not normalized:
        return None

    # Remove obvious generic single-word entries
    if normalized in GENERIC_SKILLS:
        return None

    # Ignore slash-combination skills such as Python/SQL
    # because individual skills are extracted separately.
    if "/" in skill:
        return None

    # Ignore very short generic terms
    if len(normalized) <= 2 and normalized not in {
        "c",
        "r",
        "go",
        "ai",
        "ml",
        "bi",
        "ui",
        "ux",
        "sql"
    }:
        return None

    # Use canonical names where available
    if normalized in SKILL_ALIASES:
        return SKILL_ALIASES[normalized]

    return skill.strip()


# ------------------------------------------------------------
# LOAD SKILL DICTIONARY
# ------------------------------------------------------------

def load_skill_dictionary():

    df = pd.read_csv(
        SKILL_DICTIONARY_PATH
    )

    possible_columns = [
        "skill_name",
        "skill",
        "Skill",
        "Skill Name"
    ]

    skill_column = None

    for column in possible_columns:

        if column in df.columns:
            skill_column = column
            break

    if skill_column is None:

        raise ValueError(
            "Could not find skill column in dictionary."
        )

    skills = []

    for skill in (
        df[skill_column]
        .dropna()
        .astype(str)
        .str.strip()
    ):

        cleaned_skill = clean_skill_name(skill)

        if cleaned_skill is not None:
            skills.append(cleaned_skill)

    # Remove duplicates
    skills = list(set(skills))

    # Longest skills first.
    # This helps match "Machine Learning"
    # before smaller fragments.
    skills = sorted(
        skills,
        key=lambda x: len(normalize_text(x)),
        reverse=True
    )

    return skills


# ------------------------------------------------------------
# EXTRACT SKILLS
# ------------------------------------------------------------

def extract_skills_from_text(
    text,
    skill_dictionary
):

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in skill_dictionary:

        normalized_skill = normalize_text(
            skill
        )

        if not normalized_skill:
            continue

        # Do not extract generic standalone words
        if normalized_skill in GENERIC_SKILLS:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_skill)
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized_text
        ):

            found_skills.append(skill)

    # --------------------------------------------------------
    # CANONICALIZE SKILL NAMES
    # --------------------------------------------------------

    final_skills = []

    for skill in found_skills:

        normalized_skill = normalize_text(
            skill
        )

        canonical_skill = SKILL_ALIASES.get(
            normalized_skill,
            skill
        )

        final_skills.append(
            canonical_skill
        )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    final_skills = list(
        set(final_skills)
    )

    # --------------------------------------------------------
    # REMOVE SHORTER FRAGMENTS WHEN A LONGER SKILL EXISTS
    # --------------------------------------------------------

    final_set = set(final_skills)

    filtered_skills = []

    for skill in final_skills:

        normalized_skill = normalize_text(
            skill
        )

        remove_skill = False

        for other_skill in final_set:

            if skill == other_skill:
                continue

            normalized_other = normalize_text(
                other_skill
            )

            # Example:
            # Machine Learning exists
            # therefore remove Machine and Learning
            if (
                normalized_skill
                in normalized_other
                and len(normalized_other)
                > len(normalized_skill)
                and " " in normalized_other
            ):

                remove_skill = True
                break

        if not remove_skill:
            filtered_skills.append(skill)

    return sorted(
        set(filtered_skills),
        key=str.lower
    )


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("RESUME SKILL EXTRACTION")
    print("=" * 60)

    resume_path = input(
        "\nEnter TXT resume file path: "
    ).strip().strip('"')

    if not os.path.exists(resume_path):

        print()
        print("ERROR: Resume file not found.")

        exit()

    print()
    print("Reading resume...")

    resume_text = extract_resume_text(
        resume_path
    )

    print(
        "Resume characters:",
        len(resume_text)
    )

    print()
    print("Loading skill dictionary...")

    skill_dictionary = load_skill_dictionary()

    print(
        "Usable dictionary skills:",
        len(skill_dictionary)
    )

    print()
    print("Extracting skills...")

    student_skills = extract_skills_from_text(
        resume_text,
        skill_dictionary
    )

    print()
    print("=" * 60)
    print("CLEAN EXTRACTED STUDENT SKILLS")
    print("=" * 60)

    print(
        "Total skills found:",
        len(student_skills)
    )

    print()

    for i, skill in enumerate(
        student_skills,
        start=1
    ):

        print(
            str(i) + ".",
            skill
        )

    # --------------------------------------------------------
    # SAVE STUDENT SKILLS
    # --------------------------------------------------------

    skills_df = pd.DataFrame({
        "skill_name": student_skills
    })

    skills_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print()
    print("=" * 60)
    print("STUDENT SKILLS SAVED")
    print("=" * 60)

    print(
        "File:",
        OUTPUT_PATH
    )

    print()
    print("Extraction completed successfully.")