import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

STUDENT_SKILLS_PATH = "ml/outputs/student_extracted_skills.csv"

JOB_DATA_PATH = "ml/outputs/job_skill_dataset.csv"

OUTPUT_PATH = "ml/outputs/resume_job_matching_results.csv"


# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

def normalize(text):

    return (
        str(text)
        .strip()
        .lower()
    )


# ------------------------------------------------------------
# SKILL ALIASES
# ------------------------------------------------------------

SKILL_ALIASES = {

    # Data Analysis
    "data analyst": "data analysis",
    "data analytics": "data analysis",
    "data analysis": "data analysis",

    # Business Intelligence
    "business intelligence": "business intelligence",
    "bi": "business intelligence",

    # Power BI
    "powerbi": "power bi",
    "power bi": "power bi",

    # Machine Learning
    "machinelearning": "machine learning",
    "machine learning": "machine learning",

    # Programming
    "python programming": "python",
    "sql programming": "sql",

    # Statistics
    "statistical analysis": "statistics",
    "statistics": "statistics",

    # Visualization
    "data visualization": "visualization",
    "data visualisation": "visualization",
    "visualization": "visualization",

    # Excel
    "microsoft excel": "excel",
    "advanced microsoft excel": "advanced excel",

    # PostgreSQL
    "postgres": "postgresql",

    # AI / NLP
    "artificial intelligence": "artificial intelligence",
    "natural language processing": "natural language processing",
}


def normalize_skill(skill):

    skill = normalize(skill)

    return SKILL_ALIASES.get(
        skill,
        skill
    )


# ------------------------------------------------------------
# NOISY / NON-SKILL TERMS
# ------------------------------------------------------------

NOISY_SKILLS = {

    # Generic words
    "and",
    "or",
    "the",
    "with",
    "using",
    "subject",
    "access",
    "vision",
    "enterprise",
    "discipline",
    "functions",
    "learning",
    "usage",
    "flexible",
    "test",
    "clean",
    "driving",
    "culture",
    "zones",
    "physical",
    "trust",
    "partner",
    "document",
    "insights",
    "intelligence",
    "languages",
    "methodologies",
    "recommendations",
    "skilled",
    "evaluate",
    "reliability",
    "efficiency",
    "feedback",
    "unit",
    "measurement",
    "collect",
    "enhancements",
    "assurance",

    # Phrases that are not actual skills
    "quality standards",
    "strong analytical",
    "meet deadlines",
    "product managers",
    "customer experience",
    "collaborate with cross-functional teams",
    "cross-functional",
    "senior analyst",
    "business analyst",
    "senior data analyst",
    "and reporting",

    # Education / qualification terms
    "university",
    "btech",
    "b.tech",
    "degree",
    "bachelor",
    "master",
    "masters",
    "education",
    "qualification",
    "discipline",

    # Generic job-description terms
    "solid",
    "strong",
    "good",
    "excellent",
    "ability",
    "abilities",
    "experience",
    "years",
    "year",
    "knowledge",
    "skills",
    "technical skills",
    "responsibilities",
    "requirements",
    "qualifications",

    # Generic business words
    "strategy",
    "functions",
    "vision",
    "mission",
    "culture",
    "innovation",
    "usability",
    "workflows",
    "use cases",

    # Medical / irrelevant terms found in some postings
    "doctors",
    "medical",
    "health",
    "healthcare",

    # Company / organization-specific terms
    "amex",

    # Generic / weak skill-like terms
    "analytics",
    "programming",
    "programming languages",
    "consistency",
    "cleaning",
    "solid",
    "economics",
}


# ------------------------------------------------------------
# VALIDATE SKILL
# ------------------------------------------------------------

def is_valid_skill(skill):

    skill = normalize_skill(skill)

    if not skill:
        return False

    if skill == "nan":
        return False

    if skill in NOISY_SKILLS:
        return False

    # Remove very short generic terms
    if len(skill) <= 2 and skill not in {
        "ai",
        "ml",
        "bi",
        "qa",
        "aws",
        "hr",
        "etl",
        "r"
    }:
        return False

    return True


# ------------------------------------------------------------
# LOAD STUDENT SKILLS
# ------------------------------------------------------------

print("=" * 70)
print("RESUME TO JOB SKILL MATCHING")
print("=" * 70)

print("\nLoading extracted resume skills...")

student_df = pd.read_csv(
    STUDENT_SKILLS_PATH
)


student_skills = set()


for skill in student_df["skill_name"].dropna():

    normalized = normalize_skill(skill)

    if is_valid_skill(normalized):

        student_skills.add(normalized)


print(
    "Student skills found:",
    len(student_skills)
)


print(
    "Student skills:",
    ", ".join(
        sorted(student_skills)
    )
)


# ------------------------------------------------------------
# LOAD TARGET ROLE
# ------------------------------------------------------------

target_role = input(
    "\nEnter target role: "
).strip()


if not target_role:

    raise ValueError(
        "Target role cannot be empty."
    )


target_role_normalized = normalize(
    target_role
)


print(
    "Target role:",
    target_role
)


# ------------------------------------------------------------
# LOAD JOB DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("Loading NLP job-skill dataset...")
print("=" * 70)


job_df = pd.read_csv(
    JOB_DATA_PATH
)


print(
    "Total jobs:",
    len(job_df)
)


# ------------------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = [
    "job_id",
    "job_title",
    "required_skills",
    "number_of_skills"
]


for column in required_columns:

    if column not in job_df.columns:

        raise ValueError(
            f"Missing column: {column}"
        )


# ------------------------------------------------------------
# NORMALIZE JOB TITLES
# ------------------------------------------------------------

job_df["job_title_clean"] = (
    job_df["job_title"]
    .fillna("")
    .astype(str)
    .map(normalize)
)


# ------------------------------------------------------------
# FILTER TARGET ROLE
# ------------------------------------------------------------

role_words = [
    word
    for word in target_role_normalized.split()
    if word
]


def role_matches(title):

    return all(
        word in title
        for word in role_words
    )


target_jobs = job_df[
    job_df["job_title_clean"].apply(
        role_matches
    )
].copy()


if len(target_jobs) > 0:

    print(
        "\nTarget-role jobs found:",
        len(target_jobs)
    )

    matching_job_df = target_jobs

else:

    print(
        "\nNo exact target-role jobs found."
    )

    print(
        "Using all jobs as fallback."
    )

    matching_job_df = job_df


# ------------------------------------------------------------
# JOB MATCHING
# ------------------------------------------------------------

results = []


print(
    "\nMatching resume skills with jobs..."
)


for _, row in matching_job_df.iterrows():

    job_id = row["job_id"]

    job_title = str(
        row["job_title"]
    ).strip()


    required_skills_text = str(
        row["required_skills"]
    )


    # --------------------------------------------------------
    # JOB SKILLS
    # --------------------------------------------------------

    job_skills = set()


    for skill in required_skills_text.split("|"):

        normalized = normalize_skill(skill)

        if is_valid_skill(normalized):

            job_skills.add(normalized)


    # --------------------------------------------------------
    # MATCHING
    # --------------------------------------------------------

    matching_skills = (
        student_skills
        .intersection(job_skills)
    )


    # --------------------------------------------------------
    # MISSING
    # --------------------------------------------------------

    missing_skills = (
        job_skills
        .difference(student_skills)
    )


    total_job_skills = len(
        job_skills
    )


    matching_count = len(
        matching_skills
    )


    missing_count = len(
        missing_skills
    )


    # --------------------------------------------------------
    # PERCENTAGE
    # --------------------------------------------------------

    if total_job_skills > 0:

        job_match_percentage = (
            matching_count
            / total_job_skills
        ) * 100

        skill_gap_percentage = (
            missing_count
            / total_job_skills
        ) * 100

    else:

        job_match_percentage = 0

        skill_gap_percentage = 0


    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    results.append({

        "job_id":
            job_id,

        "job_title":
            job_title,

        "total_job_skills":
            total_job_skills,

        "matching_skills":
            " | ".join(
                sorted(matching_skills)
            ),

        "missing_skills":
            " | ".join(
                sorted(missing_skills)
            ),

        "matching_skill_count":
            matching_count,

        "missing_skill_count":
            missing_count,

        "job_match_percentage":
            round(
                job_match_percentage,
                2
            ),

        "skill_gap_percentage":
            round(
                skill_gap_percentage,
                2
            )
    })


# ------------------------------------------------------------
# DATAFRAME
# ------------------------------------------------------------

results_df = pd.DataFrame(
    results
)


# ------------------------------------------------------------
# REMOVE EMPTY JOBS
# ------------------------------------------------------------

if not results_df.empty:

    results_df = results_df[
        results_df["total_job_skills"] > 0
    ].copy()


# ------------------------------------------------------------
# SORT
# ------------------------------------------------------------

if not results_df.empty:

    results_df = results_df.sort_values(

        by=[
            "job_match_percentage",
            "matching_skill_count"
        ],

        ascending=False
    )


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY TOP 10
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 JOB MATCHES")
print("=" * 70)


if not results_df.empty:

    print(

        results_df[
            [
                "job_id",
                "job_title",
                "matching_skill_count",
                "job_match_percentage",
                "skill_gap_percentage"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

else:

    print(
        "No matching jobs found."
    )


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUME JOB MATCHING COMPLETE")
print("=" * 70)


print(
    "\nTarget role:",
    target_role
)


print(
    "Jobs analyzed:",
    len(results_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)