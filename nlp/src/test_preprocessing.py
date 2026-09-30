from database import load_jobs
from text_preprocessing import preprocess_text


# Load jobs from PostgreSQL
df = load_jobs()

print("Total jobs:", len(df))

print("\nOriginal job description:")
print(df.loc[0, "job_description"])


print("\n" + "=" * 80)
print("\nPreprocessed job description:")
print(
    preprocess_text(
        df.loc[0, "job_description"]
    )
)