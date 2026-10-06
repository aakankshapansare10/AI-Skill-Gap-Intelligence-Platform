import pandas as pd


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

STUDENT_SKILLS_PATH = (
    "ml/outputs/student_extracted_skills.csv"
)

JOB_DATA_PATH = (
    "ml/outputs/job_skill_dataset.csv"
)

OUTPUT_PATH = (
    "ml/outputs/resume_target_role_analysis.csv"
)


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
    "statistics": "statistics",
    "statistical analysis": "statistics",

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

    # Programming
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

    # Data Analysis
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

    # Business Intelligence / Reporting
    "business intelligence",
    "power bi",
    "tableau",
    "looker",
    "dashboards",
    "reporting",
    "excel",
    "advanced excel",

    # Databases
    "mysql",
    "postgresql",
    "oracle",
    "sql server",
    "mongodb",
    "database",
    "databases",

    # Python / Data Libraries
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scipy",

    # Machine Learning / AI
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "predictive modeling",

    # Data Engineering
    "etl",
    "data warehousing",
    "data warehouse",
    "apache spark",
    "spark",
    "hadoop",

    # Cloud
    "aws",
    "azure",
    "google cloud",
    "gcp",

    # Business / Analytical
    "business analysis",
    "risk management",
    "decision making",
    "problem solving",
    "research",
    "forecasting",

    # Professional Skills
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
# LOAD STUDENT SKILLS
# ------------------------------------------------------------

print("=" * 70)
print("RESUME TO TARGET ROLE ANALYSIS")
print("=" * 70)

print("\nLoading student skills...")

student_df = pd.read_csv(
    STUDENT_SKILLS_PATH
)


student_skills = set()


for skill in student_df["skill_name"].dropna():

    normalized = normalize_skill(skill)

    if is_valid_skill(normalized):

        student_skills.add(normalized)


print(
    "\nStudent meaningful skills found:",
    len(student_skills)
)

print(
    "Student skills:",
    ", ".join(sorted(student_skills))
)


# ------------------------------------------------------------
# ASK TARGET ROLE
# ------------------------------------------------------------

target_role = input(
    "\nEnter your target role: "
).strip()


if not target_role:

    raise ValueError(
        "Target role cannot be empty."
    )


target_role_normalized = normalize(
    target_role
)


print(
    "\nTarget role:",
    target_role
)


# ------------------------------------------------------------
# LOAD JOB DATA
# ------------------------------------------------------------

print("\nLoading job dataset...")

job_df = pd.read_csv(
    JOB_DATA_PATH
)


print(
    "Total jobs in dataset:",
    len(job_df)
)


# ------------------------------------------------------------
# FILTER TARGET ROLE
# ------------------------------------------------------------

job_df["job_title_clean"] = (
    job_df["job_title"]
    .fillna("")
    .astype(str)
    .map(normalize)
)


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


print(
    "Matching target-role jobs:",
    len(target_jobs)
)


# ------------------------------------------------------------
# CHECK JOBS
# ------------------------------------------------------------

if len(target_jobs) == 0:

    print(
        "\nNo jobs found for this target role."
    )

    raise SystemExit()


# ------------------------------------------------------------
# ANALYZE SKILLS
# ------------------------------------------------------------

skill_data = {}


for _, row in target_jobs.iterrows():

    required_skills_text = str(
        row["required_skills"]
    )

    job_skills = set()


    for skill in required_skills_text.split("|"):

        normalized = normalize_skill(skill)

        if is_valid_skill(normalized):

            job_skills.add(normalized)


    # Count each skill only once per job
    for skill in job_skills:

        if skill not in skill_data:

            skill_data[skill] = {
                "jobs_requiring_skill": 0,
                "matching_jobs": 0
            }


        skill_data[
            skill
        ][
            "jobs_requiring_skill"
        ] += 1


        if skill in student_skills:

            skill_data[
                skill
            ][
                "matching_jobs"
            ] += 1


# ------------------------------------------------------------
# CREATE RESULT
# ------------------------------------------------------------

results = []


for skill, values in skill_data.items():

    required_count = values[
        "jobs_requiring_skill"
    ]

    matching_count = values[
        "matching_jobs"
    ]

    missing_count = (
        required_count
        - matching_count
    )


    demand_percentage = (
        required_count
        / len(target_jobs)
    ) * 100


    results.append({

        "target_role":
            target_role,

        "skill_name":
            skill,

        "jobs_requiring_skill":
            required_count,

        "matching_jobs":
            matching_count,

        "missing_jobs":
            missing_count,

        "demand_percentage":
            round(
                demand_percentage,
                2
            ),

        "student_has_skill":
            "Yes"
            if skill in student_skills
            else "No"
    })


# ------------------------------------------------------------
# DATAFRAME
# ------------------------------------------------------------

result_df = pd.DataFrame(
    results
)


# ------------------------------------------------------------
# HANDLE EMPTY RESULT
# ------------------------------------------------------------

if result_df.empty:

    result_df = pd.DataFrame(
        columns=[
            "target_role",
            "skill_name",
            "jobs_requiring_skill",
            "matching_jobs",
            "missing_jobs",
            "demand_percentage",
            "student_has_skill",
            "priority"
        ]
    )


else:

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    result_df = result_df.sort_values(
        by=[
            "student_has_skill",
            "jobs_requiring_skill"
        ],
        ascending=[
            True,
            False
        ]
    )


    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    def priority(row):

        if row["student_has_skill"] == "No":

            if row["demand_percentage"] >= 30:

                return "HIGH"

            elif row["demand_percentage"] >= 10:

                return "MEDIUM"

            else:

                return "LOW"

        return "ALREADY HAVE"


    result_df["priority"] = (
        result_df.apply(
            priority,
            axis=1
        )
    )


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

result_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TARGET ROLE SKILL GAP")
print("=" * 70)


missing_df = result_df[
    result_df["student_has_skill"] == "No"
]


if not missing_df.empty:

    print(
        missing_df.head(20).to_string(
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
print("TARGET ROLE ANALYSIS COMPLETE")
print("=" * 70)

print(
    "\nTarget role:",
    target_role
)

print(
    "Jobs analyzed:",
    len(target_jobs)
)

print(
    "Meaningful missing skills:",
    len(missing_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)