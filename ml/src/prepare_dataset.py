import pandas as pd
from database_connection import load_ml_job_skills


print("=" * 60)
print("LOADING NLP DATA")
print("=" * 60)

df = load_ml_job_skills()

print("Total rows:", len(df))
print("Total jobs:", df["job_id"].nunique())
print("Total skills:", df["skill_id"].nunique())

print()
print("=" * 60)
print("CREATING JOB-LEVEL DATASET")
print("=" * 60)

job_dataset = (
    df.groupby(["job_id", "job_title"])
    .agg(
        required_skills=("skill_name", lambda x: sorted(set(x)))
    )
    .reset_index()
)

job_dataset["number_of_skills"] = job_dataset["required_skills"].apply(len)

print("Total jobs:", len(job_dataset))

print()
print("Sample job records:")

for _, row in job_dataset.head(10).iterrows():
    print()
    print("Job ID:", row["job_id"])
    print("Job Title:", row["job_title"])
    print("Number of Skills:", row["number_of_skills"])
    print("Skills:", ", ".join(row["required_skills"][:15]))


print()
print("=" * 60)
print("SKILL COUNT SUMMARY")
print("=" * 60)

print(
    job_dataset["number_of_skills"].describe()
)


output_path = "ml/outputs/job_skill_dataset.csv"

save_df = job_dataset.copy()

save_df["required_skills"] = save_df["required_skills"].apply(
    lambda x: " | ".join(x)
)

save_df.to_csv(output_path, index=False)

print()
print("=" * 60)
print("DATASET SAVED")
print("=" * 60)

print("File:", output_path)
print("Rows:", len(save_df))
print("Columns:", list(save_df.columns))