import pandas as pd

INPUT_PATH = "data/processed/cleaned_job_postings.csv"

df = pd.read_csv("E:/3rd year/pbl/indian_job_market_2025.csv")

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 3 - SKILL ANALYSIS")
print("=" * 70)

print(f"Total job postings: {len(df):,}")

print("\n" + "=" * 70)
print("SKILL INFORMATION")
print("=" * 70)

print(f"Missing skill values: {df['tagsAndSkills'].isna().sum():,}")
print(f"Unique skill entries: {df['tagsAndSkills'].nunique():,}")

print("\n" + "=" * 70)
print("SAMPLE SKILL ENTRIES")
print("=" * 70)

sample_skills = (
    df["tagsAndSkills"]
    .dropna()
    .head(30)
)

for number, skills in enumerate(sample_skills, start=1):
    print(f"{number}. {skills}")

print("\n" + "=" * 70)
print("MOST COMMON SKILL ENTRIES")
print("=" * 70)

skill_counts = (
    df["tagsAndSkills"]
    .dropna()
    .value_counts()
    .head(30)
)

print(skill_counts.to_string())

print("\n" + "=" * 70)
print("JOB DESCRIPTION INFORMATION")
print("=" * 70)

description_lengths = (
    df["jobDescription"]
    .fillna("")
    .astype(str)
    .str.len()
)

print(
    f"Unique job descriptions: "
    f"{df['jobDescription'].nunique():,}"
)

print(
    f"Average description length: "
    f"{description_lengths.mean():.2f}"
)

print(
    f"Minimum description length: "
    f"{description_lengths.min():,}"
)

print(
    f"Maximum description length: "
    f"{description_lengths.max():,}"
)

print("\n" + "=" * 70)
print("SKILL ANALYSIS COMPLETED")
print("=" * 70)