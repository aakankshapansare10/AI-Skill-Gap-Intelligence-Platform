import pandas as pd
import re

INPUT_PATH = "data/raw/indian_job_postings.csv"
OUTPUT_PATH = "data/processed/cleaned_job_postings.csv"

df = pd.read_csv("C:/Users/ruhig/Downloads/indian_job_market_2025.csv")

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("DATA CLEANING")
print("=" * 70)

print(f"Original rows: {len(df):,}")
print(f"Original columns: {len(df.columns):,}")

# Remove completely empty rows
df = df.dropna(how="all")

# Remove exact duplicate rows
before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = before_duplicates - len(df)

print(f"Duplicate rows removed: {duplicates_removed:,}")

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
)

# Text columns
text_columns = [
    "title",
    "companyName",
    "tagsAndSkills",
    "jobDescription",
    "location",
    "experience",
    "salary",
    "jobUploaded"
]

# Fill missing text values and remove extra spaces
for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# Function to clean text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Apply text cleaning
for column in [
    "title",
    "companyName",
    "tagsAndSkills",
    "jobDescription",
    "location",
    "experience",
    "salary"
]:
    if column in df.columns:
        df[column] = df[column].apply(clean_text)

# Remove rows without job title
if "title" in df.columns:

    before_title_filter = len(df)

    df = df[
        (df["title"] != "") &
        (df["title"].str.lower() != "nan")
    ]

    removed = before_title_filter - len(df)

    print(f"Rows without job title removed: {removed:,}")

# Remove rows without job description
if "jobDescription" in df.columns:

    before_description_filter = len(df)

    df = df[
        (df["jobDescription"] != "") &
        (df["jobDescription"].str.lower() != "nan")
    ]

    removed = before_description_filter - len(df)

    print(f"Rows without job description removed: {removed:,}")

# Calculate description length
if "jobDescription" in df.columns:

    df["description_length"] = (
        df["jobDescription"].str.len()
    )

# Remove extremely short job descriptions
if "description_length" in df.columns:

    before_length_filter = len(df)

    df = df[
        df["description_length"] >= 50
    ]

    removed = before_length_filter - len(df)

    print(f"Very short descriptions removed: {removed:,}")

# Standardize skills formatting
if "tagsAndSkills" in df.columns:

    df["tagsAndSkills"] = (
        df["tagsAndSkills"]
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.replace(r"\s*;\s*", "; ", regex=True)
    )

# Remove columns that are not required
# for the skill-gap intelligence system
columns_to_drop = [
    "ReviewsCount",
    "AggregateRating"
]

existing_columns = [
    column
    for column in columns_to_drop
    if column in df.columns
]

df = df.drop(
    columns=existing_columns
)

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 70)
print("CLEANING COMPLETED")
print("=" * 70)

print(f"Final rows: {len(df):,}")
print(f"Final columns: {len(df.columns):,}")

print("\nRemaining missing values:")

print(
    df.isnull()
    .sum()
    .to_string()
)

print("\nColumns in cleaned dataset:")

print(
    df.columns.tolist()
)

print("\nCleaned dataset saved to:")

print(OUTPUT_PATH)

print("\nData cleaning completed successfully.")

print("=" * 70)