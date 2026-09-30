import pandas as pd

# --------------------------------------------------
# AI SKILL GAP INTELLIGENCE PLATFORM
#  DATA UNDERSTANDING
# --------------------------------------------------

# Load the dataset
DATA_PATH = "data/raw/indian_job_postings.csv"

df = pd.read_csv("E:/3rd year/pbl/indian_job_market_2025.csv")

# --------------------------------------------------
# BASIC INFORMATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("DATA UNDERSTANDING REPORT")
print("=" * 70)

print(f"\nDataset Shape:")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}")

# --------------------------------------------------
# COLUMN INFORMATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("COLUMN INFORMATION")
print("=" * 70)

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Missing %": (df.isnull().mean() * 100).round(2).values,
    "Unique Values": [df[column].nunique() for column in df.columns]
})

print(column_info.to_string(index=False))

# --------------------------------------------------
# FIRST FIVE RECORDS
# --------------------------------------------------

print("\n" + "=" * 70)
print("FIRST 5 JOB POSTINGS")
print("=" * 70)

print(df.head().to_string())

# --------------------------------------------------
# DUPLICATE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")

# --------------------------------------------------
# JOB TITLE ANALYSIS
# --------------------------------------------------

if "title" in df.columns:

    print("\n" + "=" * 70)
    print("JOB TITLE ANALYSIS")
    print("=" * 70)

    print(f"Unique job titles: {df['title'].nunique():,}")

    print("\nTop 20 job titles:")

    print(
        df["title"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# COMPANY ANALYSIS
# --------------------------------------------------

if "companyName" in df.columns:

    print("\n" + "=" * 70)
    print("COMPANY ANALYSIS")
    print("=" * 70)

    print(f"Unique companies: {df['companyName'].nunique():,}")

    print("\nTop 20 companies:")

    print(
        df["companyName"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# LOCATION ANALYSIS
# --------------------------------------------------

if "location" in df.columns:

    print("\n" + "=" * 70)
    print("LOCATION ANALYSIS")
    print("=" * 70)

    print(f"Unique locations: {df['location'].nunique():,}")

    print("\nTop 20 locations:")

    print(
        df["location"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# SKILL FIELD ANALYSIS
# --------------------------------------------------

if "tagsAndSkills" in df.columns:

    print("\n" + "=" * 70)
    print("SKILL FIELD ANALYSIS")
    print("=" * 70)

    missing_skills = df["tagsAndSkills"].isna().sum()

    print(f"Missing skill values: {missing_skills:,}")

    print("\nSample skill values:")

    print(
        df["tagsAndSkills"]
        .dropna()
        .head(10)
        .to_string(index=False)
    )

# --------------------------------------------------
# JOB DESCRIPTION ANALYSIS
# --------------------------------------------------

if "jobDescription" in df.columns:

    print("\n" + "=" * 70)
    print("JOB DESCRIPTION ANALYSIS")
    print("=" * 70)

    missing_descriptions = df["jobDescription"].isna().sum()

    unique_descriptions = df["jobDescription"].nunique()

    print(f"Missing descriptions : {missing_descriptions:,}")
    print(f"Unique descriptions  : {unique_descriptions:,}")

    description_lengths = (
        df["jobDescription"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    print(f"Average description length : {description_lengths.mean():.2f}")
    print(f"Minimum description length : {description_lengths.min():,}")
    print(f"Maximum description length : {description_lengths.max():,}")

# --------------------------------------------------
# EXPERIENCE ANALYSIS
# --------------------------------------------------

if "experience" in df.columns:

    print("\n" + "=" * 70)
    print("EXPERIENCE ANALYSIS")
    print("=" * 70)

    print(
        df["experience"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# SALARY ANALYSIS
# --------------------------------------------------

if "salary" in df.columns:

    print("\n" + "=" * 70)
    print("SALARY ANALYSIS")
    print("=" * 70)

    print(
        df["salary"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# POSTING INFORMATION
# --------------------------------------------------

if "jobUploaded" in df.columns:

    print("\n" + "=" * 70)
    print("JOB POSTING INFORMATION")
    print("=" * 70)

    print(
        df["jobUploaded"]
        .value_counts()
        .head(20)
        .to_string()
    )

# --------------------------------------------------
# DATASET SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

print(f"Total job postings       : {len(df):,}")
print(f"Total columns            : {len(df.columns):,}")
print(f"Duplicate rows           : {df.duplicated().sum():,}")

if "title" in df.columns:
    print(f"Unique job titles        : {df['title'].nunique():,}")

if "companyName" in df.columns:
    print(f"Unique companies         : {df['companyName'].nunique():,}")

if "location" in df.columns:
    print(f"Unique locations         : {df['location'].nunique():,}")

if "jobDescription" in df.columns:
    print(f"Unique job descriptions  : {df['jobDescription'].nunique():,}")

if "tagsAndSkills" in df.columns:
    print(f"Missing skill values     : {df['tagsAndSkills'].isna().sum():,}")

if "jobDescription" in df.columns:
    print(f"Missing descriptions     : {df['jobDescription'].isna().sum():,}")

print("\nData understanding completed successfully.")
print("=" * 70)