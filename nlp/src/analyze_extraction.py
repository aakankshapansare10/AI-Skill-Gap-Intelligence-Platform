import pandas as pd


FILE_PATH = "../../data/processed/job_skill_extraction.csv"


print("=" * 70)
print("NLP EXTRACTION QUALITY ANALYSIS")
print("=" * 70)


# --------------------------------------------------
# 1. Load extracted data
# --------------------------------------------------

df = pd.read_csv(FILE_PATH)

print("\nFile loaded successfully.")


# --------------------------------------------------
# 2. Basic statistics
# --------------------------------------------------

print("\n--- BASIC STATISTICS ---")

print(
    "Total job-skill matches:",
    len(df)
)

print(
    "Unique jobs:",
    df["job_id"].nunique()
)

print(
    "Unique skills extracted:",
    df["skill_id"].nunique()
)


# --------------------------------------------------
# 3. Skills per job
# --------------------------------------------------

skills_per_job = (
    df.groupby("job_id")
    .size()
)

print("\n--- SKILLS PER JOB ---")

print(
    "Average skills per job:",
    round(skills_per_job.mean(), 2)
)

print(
    "Minimum skills in a job:",
    skills_per_job.min()
)

print(
    "Maximum skills in a job:",
    skills_per_job.max()
)


# --------------------------------------------------
# 4. Jobs with most extracted skills
# --------------------------------------------------

print("\n--- JOBS WITH MOST EXTRACTED SKILLS ---")

top_jobs = (
    skills_per_job
    .sort_values(ascending=False)
    .head(10)
)

print(
    top_jobs.to_string()
)


# --------------------------------------------------
# 5. Most frequently extracted skills
# --------------------------------------------------

print("\n--- TOP 30 EXTRACTED SKILLS ---")

top_skills = (
    df["skill_name"]
    .value_counts()
    .head(30)
)

print(
    top_skills.to_string()
)


# --------------------------------------------------
# 6. Skills appearing only once
# --------------------------------------------------

skill_frequency = (
    df["skill_name"]
    .value_counts()
)

rare_skills = skill_frequency[
    skill_frequency == 1
]

print("\n--- RARE SKILLS ---")

print(
    "Skills appearing only once:",
    len(rare_skills)
)


# --------------------------------------------------
# 7. Check duplicate job-skill pairs
# --------------------------------------------------

duplicates = df.duplicated(
    subset=["job_id", "skill_id"]
).sum()

print("\n--- DUPLICATES ---")

print(
    "Duplicate job-skill pairs:",
    duplicates
)


# --------------------------------------------------
# 8. Missing values
# --------------------------------------------------

print("\n--- MISSING VALUES ---")

print(
    df.isnull().sum()
)


# --------------------------------------------------
# 9. Extraction distribution
# --------------------------------------------------

print("\n--- SKILL COUNT DISTRIBUTION ---")

distribution = (
    skills_per_job
    .value_counts()
    .sort_index()
    .head(20)
)

print(
    distribution.to_string()
)


# --------------------------------------------------
# 10. Final summary
# --------------------------------------------------

print("\n" + "=" * 70)

print("ANALYSIS COMPLETED")

print("=" * 70)