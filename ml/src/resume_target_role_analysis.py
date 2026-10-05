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
# NORMALIZE
# ------------------------------------------------------------

def normalize(text):

    return (
        str(text)
        .strip()
        .lower()
    )


# ------------------------------------------------------------
# LOAD STUDENT SKILLS
# ------------------------------------------------------------

print("=" * 70)
print("RESUME TO TARGET ROLE ANALYSIS")
print("=" * 70)

student_df = pd.read_csv(
    STUDENT_SKILLS_PATH
)

student_skills = set(
    student_df["skill_name"]
    .dropna()
    .astype(str)
    .map(normalize)
)

student_skills.discard("")


# ------------------------------------------------------------
# ASK TARGET ROLE
# ------------------------------------------------------------

target_role = input(
    "\nEnter your target role: "
).strip()

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

job_df = pd.read_csv(
    JOB_DATA_PATH
)

print(
    "\nTotal jobs in dataset:",
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
# CHECK IF JOBS FOUND
# ------------------------------------------------------------

if len(target_jobs) == 0:

    print("\nNo jobs found for this target role.")

    print(
        "\nTry a broader role name."
    )

    exit()


# ------------------------------------------------------------
# ANALYZE SKILLS
# ------------------------------------------------------------

skill_data = {}


for _, row in target_jobs.iterrows():

    required_skills_text = str(
        row["required_skills"]
    )

    job_skills = set(
        normalize(skill)
        for skill
        in required_skills_text.split("|")
    )

    job_skills.discard("")


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

    if required_count > 0:

        demand_percentage = (
            required_count
            / len(target_jobs)
        ) * 100

    else:

        demand_percentage = 0


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
# SORT
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# ADD PRIORITY
# ------------------------------------------------------------

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

print(
    missing_df.head(20).to_string(
        index=False
    )
)


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
    "Missing skills:",
    len(missing_df)
)

print(
    "\nOutput file:",
    OUTPUT_PATH
)