import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

MATCHING_RESULTS_PATH = (
    "ml/outputs/resume_job_matching_results.csv"
)

OUTPUT_PATH = (
    "ml/outputs/resume_skill_gap_analysis.csv"
)


# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

def normalize_skill(skill):
    return str(skill).strip().lower()


# ------------------------------------------------------------
# SKILL ALIASES
# ------------------------------------------------------------

SKILL_ALIASES = {
    # Data Analysis
    "data analyst": "data analysis",
    "data analytics": "data analysis",
    "data analysis": "data analysis",

    # Business Intelligence
    "bi": "business intelligence",
    "business intelligence": "business intelligence",

    # Power BI
    "powerbi": "power bi",
    "power bi": "power bi",

    # Visualization
    "data visualisation": "visualization",
    "data visualization": "visualization",
    "visualization": "visualization",

    # Statistics
    "statistical analysis": "statistics",
    "statistics": "statistics",

    # Programming
    "python programming": "python",
    "sql programming": "sql",

    # Excel
    "microsoft excel": "excel",
    "advanced microsoft excel": "advanced excel",

    # PostgreSQL
    "postgres": "postgresql",

    # Machine Learning
    "machinelearning": "machine learning",

    # AI / NLP
    "artificial intelligence": "artificial intelligence",
    "natural language processing": "natural language processing",
}


# ------------------------------------------------------------
# NOISY SKILLS
# ------------------------------------------------------------

NOISY_SKILLS = {
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
}


# ------------------------------------------------------------
# RECOGNIZED SKILLS
# ------------------------------------------------------------

VALID_SKILLS = {
    # --------------------------------------------------------
    # PROGRAMMING
    # --------------------------------------------------------

    "python",
    "r",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "sql",
    "vba",

    # --------------------------------------------------------
    # DATA ANALYSIS
    # --------------------------------------------------------

    "data analysis",
    "data analytics",
    "data science",
    "data mining",
    "data modeling",
    "data management",
    "data cleaning",
    "data preprocessing",
    "data quality",
    "data visualization",
    "visualization",
    "statistics",
    "mathematics",
    "quantitative analysis",

    # --------------------------------------------------------
    # BUSINESS INTELLIGENCE / REPORTING
    # --------------------------------------------------------

    "business intelligence",
    "power bi",
    "tableau",
    "looker",
    "dashboards",
    "reporting",
    "excel",
    "advanced excel",

    # --------------------------------------------------------
    # DATABASES
    # --------------------------------------------------------

    "mysql",
    "postgresql",
    "oracle",
    "sql server",
    "mongodb",
    "database",
    "databases",

    # --------------------------------------------------------
    # PYTHON / DATA LIBRARIES
    # --------------------------------------------------------

    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scipy",

    # --------------------------------------------------------
    # MACHINE LEARNING / AI
    # --------------------------------------------------------

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "predictive modeling",

    # --------------------------------------------------------
    # DATA ENGINEERING
    # --------------------------------------------------------

    "etl",
    "data warehousing",
    "data warehouse",
    "apache spark",
    "spark",
    "hadoop",

    # --------------------------------------------------------
    # CLOUD
    # --------------------------------------------------------

    "aws",
    "azure",
    "google cloud",
    "gcp",

    # --------------------------------------------------------
    # BUSINESS / ANALYTICAL
    # --------------------------------------------------------

    "business analysis",
    "risk management",
    "decision making",
    "problem solving",
    "research",
    "forecasting",

    # --------------------------------------------------------
    # PROFESSIONAL SKILLS
    # --------------------------------------------------------

    "project management",
    "communication",
    "presentation",
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

    if skill in VALID_SKILLS:
        return True

    return False


# ------------------------------------------------------------
# CANONICAL SKILL
# ------------------------------------------------------------

def canonical_skill(skill):

    skill = normalize_skill(skill)

    return SKILL_ALIASES.get(
        skill,
        skill
    )


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("=" * 70)
print("RESUME SKILL GAP ANALYSIS")
print("=" * 70)

print("\nLoading resume-job matching results...")

try:

    df = pd.read_csv(
        MATCHING_RESULTS_PATH
    )

except FileNotFoundError:

    print(
        "\nERROR: Matching results file not found:"
    )

    print(
        MATCHING_RESULTS_PATH
    )

    raise


print(
    "Jobs loaded:",
    len(df)
)


# ------------------------------------------------------------
# CHECK REQUIRED COLUMN
# ------------------------------------------------------------

if "missing_skills" not in df.columns:

    raise ValueError(
        "Column 'missing_skills' not found in matching results."
    )


# ------------------------------------------------------------
# EXTRACT MISSING SKILLS
# ------------------------------------------------------------

skill_counts = {}


for _, row in df.iterrows():

    missing_skills = str(
        row["missing_skills"]
    )

    if (
        missing_skills == ""
        or missing_skills.lower() == "nan"
    ):
        continue

    skills = missing_skills.split("|")

    # Avoid counting the same skill twice
    # for the same job
    job_skills = set()

    for skill in skills:

        skill = canonical_skill(skill)

        if not is_valid_skill(skill):
            continue

        job_skills.add(skill)

    for skill in job_skills:

        skill_counts[skill] = (
            skill_counts.get(skill, 0) + 1
        )


# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

gap_df = pd.DataFrame(
    [
        {
            "skill_name": skill,
            "jobs_requiring_skill": count
        }

        for skill, count
        in skill_counts.items()
    ]
)


# ------------------------------------------------------------
# HANDLE EMPTY RESULT
# ------------------------------------------------------------

if gap_df.empty:

    gap_df = pd.DataFrame(
        columns=[
            "rank",
            "skill_name",
            "jobs_requiring_skill",
            "demand_percentage"
        ]
    )

else:

    # --------------------------------------------------------
    # CALCULATE PERCENTAGE
    # --------------------------------------------------------

    total_jobs = len(df)

    if total_jobs > 0:

        gap_df["demand_percentage"] = (
            gap_df["jobs_requiring_skill"]
            / total_jobs
        ) * 100

    else:

        gap_df["demand_percentage"] = 0


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    gap_df = gap_df.sort_values(
        by=[
            "jobs_requiring_skill",
            "demand_percentage"
        ],
        ascending=False
    )


    # --------------------------------------------------------
    # ROUND
    # --------------------------------------------------------

    gap_df["demand_percentage"] = (
        gap_df["demand_percentage"]
        .round(2)
    )


    # --------------------------------------------------------
    # ADD RANK
    # --------------------------------------------------------

    gap_df.insert(
        0,
        "rank",
        range(
            1,
            len(gap_df) + 1
        )
    )


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

gap_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY TOP 20
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP MISSING SKILLS")
print("=" * 70)

if not gap_df.empty:

    print(
        gap_df.head(20).to_string(
            index=False
        )
    )

else:

    print(
        "No meaningful missing skills found."
    )


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SKILL GAP ANALYSIS COMPLETE")
print("=" * 70)

print(
    "\nUnique meaningful missing skills:",
    len(gap_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)