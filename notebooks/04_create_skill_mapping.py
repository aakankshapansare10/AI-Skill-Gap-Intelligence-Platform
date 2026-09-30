import pandas as pd

INPUT_PATH = "data/processed/cleaned_job_postings.csv"
OUTPUT_PATH = "data/processed/job_skills.csv"

df = pd.read_csv("E:/3rd year/pbl/indian_job_market_2025.csv")

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 3B - JOB SKILL MAPPING")
print("=" * 70)

print(f"Total job postings: {len(df):,}")

skill_data = df[
    ["jobId", "title", "tagsAndSkills"]
].copy()

skill_data = skill_data.dropna(
    subset=["tagsAndSkills"]
)

skill_data["tagsAndSkills"] = (
    skill_data["tagsAndSkills"]
    .astype(str)
    .str.strip()
)

skill_data = skill_data[
    skill_data["tagsAndSkills"] != ""
]

skill_data["skill"] = (
    skill_data["tagsAndSkills"]
    .str.split(",")
)

skill_data = skill_data.explode(
    "skill"
)

skill_data["skill"] = (
    skill_data["skill"]
    .astype(str)
    .str.strip()
)

skill_data["skill"] = (
    skill_data["skill"]
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
)

skill_data = skill_data[
    skill_data["skill"] != ""
]

skill_data = skill_data[
    ["jobId", "title", "skill"]
]

skill_data = skill_data.drop_duplicates()

skill_data = skill_data.reset_index(
    drop=True
)

skill_data.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 70)
print("JOB-SKILL MAPPING CREATED")
print("=" * 70)

print(
    f"Total job-skill records: "
    f"{len(skill_data):,}"
)

print(
    f"Unique jobs: "
    f"{skill_data['jobId'].nunique():,}"
)

print(
    f"Unique skills: "
    f"{skill_data['skill'].nunique():,}"
)

print("\nSample job-skill records:")

print(
    skill_data
    .head(30)
    .to_string(index=False)
)

print("\nTop 30 skills:")

skill_counts = (
    skill_data["skill"]
    .value_counts()
    .head(30)
)

print(
    skill_counts.to_string()
)

print("\nJob-skill mapping saved to:")
print(OUTPUT_PATH)

print("\nStep 3B completed successfully.")

print("=" * 70)