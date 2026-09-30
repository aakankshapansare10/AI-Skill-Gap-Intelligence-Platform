from pathlib import Path
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, save_npz


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "normalized_job_skills.csv"
)

MATRIX_FILE = (
    ROOT / "data" / "processed"
    / "skill_features.npz"
)

METADATA_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_metadata.csv"
)

SKILLS_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_names.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("Loading normalized job skills dataset...")

df = pd.read_csv(INPUT_FILE)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


print("\nStandardized columns:")
print(df.columns.tolist())


# ============================================================
# 4. IDENTIFY COLUMNS
# ============================================================

job_column = None
title_column = None
skill_column = None


# Job ID
for column in ["jobid", "job_id", "job"]:
    if column in df.columns:
        job_column = column
        break


# Job title
for column in ["title", "job_title"]:
    if column in df.columns:
        title_column = column
        break


# Skill
for column in ["normalized_skill", "skill", "skills"]:
    if column in df.columns:
        skill_column = column
        break


if job_column is None:
    raise ValueError(
        "Job ID column not found."
    )

if title_column is None:
    raise ValueError(
        "Title column not found."
    )

if skill_column is None:
    raise ValueError(
        "Skill column not found."
    )


print("\nUsing columns:")
print("Job ID :", job_column)
print("Title  :", title_column)
print("Skill  :", skill_column)


# ============================================================
# 5. CLEAN DATA
# ============================================================

df[title_column] = (
    df[title_column]
    .fillna("")
    .astype(str)
    .str.strip()
)

df[skill_column] = (
    df[skill_column]
    .fillna("")
    .astype(str)
    .str.strip()
)


# Remove empty skills
df = df[df[skill_column] != ""]


# ============================================================
# 6. REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates(
    subset=[job_column, skill_column]
)


print("\nRows after duplicate removal:")
print(len(df))


# ============================================================
# 7. CREATE JOB AND SKILL INDEX
# ============================================================

jobs = (
    df[[job_column, title_column]]
    .drop_duplicates(subset=[job_column])
    .reset_index(drop=True)
)

skills = (
    df[skill_column]
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)


print("\nNumber of jobs:")
print(len(jobs))

print("\nNumber of unique skills:")
print(len(skills))


# ============================================================
# 8. CREATE INDEX MAPPINGS
# ============================================================

job_to_index = {
    job_id: index
    for index, job_id in enumerate(jobs[job_column])
}

skill_to_index = {
    skill: index
    for index, skill in enumerate(skills)
}


# ============================================================
# 9. CONVERT TO SPARSE MATRIX
# ============================================================

print("\nCreating sparse skill-feature matrix...")


row_indices = df[job_column].map(job_to_index).to_numpy()

column_indices = df[skill_column].map(skill_to_index).to_numpy()

data = np.ones(
    len(df),
    dtype=np.int8
)


skill_matrix = csr_matrix(
    (
        data,
        (row_indices, column_indices)
    ),
    shape=(
        len(jobs),
        len(skills)
    )
)


# ============================================================
# 10. SAVE SPARSE MATRIX
# ============================================================

save_npz(
    MATRIX_FILE,
    skill_matrix
)


# ============================================================
# 11. SAVE JOB METADATA
# ============================================================

jobs.to_csv(
    METADATA_FILE,
    index=False
)


# ============================================================
# 12. SAVE SKILL NAMES
# ============================================================

skills.to_frame(
    name="skill"
).to_csv(
    SKILLS_FILE,
    index=False
)


# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("SKILL FEATURES CREATED SUCCESSFULLY")
print("========================================")

print("\nSparse matrix shape:")
print(skill_matrix.shape)

print("\nNumber of stored values:")
print(skill_matrix.nnz)

print("\nMatrix density:")

density = (
    skill_matrix.nnz
    / (skill_matrix.shape[0] * skill_matrix.shape[1])
    * 100
)

print(f"{density:.6f}%")