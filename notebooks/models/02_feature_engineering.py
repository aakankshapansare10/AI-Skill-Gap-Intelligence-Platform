from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_metadata.csv"
)

FEATURE_FILE = (
    ROOT / "data" / "processed"
    / "title_tfidf_features.npz"
)

VECTORIZER_FILE = (
    ROOT / "notebooks" / "models"
    / "tfidf_vectorizer.pkl"
)


# ============================================================
# 2. LOAD JOB METADATA
# ============================================================

print("Loading job metadata...")

df = pd.read_csv(INPUT_FILE)

print("\nColumns:")
print(df.columns.tolist())

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 3. FIND TITLE COLUMN
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


title_column = None

for column in ["title", "job_title"]:
    if column in df.columns:
        title_column = column
        break


if title_column is None:
    raise ValueError(
        "Job title column was not found."
    )


print("\nUsing title column:")
print(title_column)


# ============================================================
# 4. CLEAN JOB TITLES
# ============================================================

df[title_column] = (
    df[title_column]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
)


# ============================================================
# 5. TF-IDF FEATURE ENGINEERING
# ============================================================

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)


X_title = vectorizer.fit_transform(
    df[title_column]
)


# ============================================================
# 6. SAVE SPARSE TF-IDF MATRIX
# ============================================================

save_npz(
    FEATURE_FILE,
    X_title
)


# ============================================================
# 7. SAVE VECTORIZER
# ============================================================

joblib.dump(
    vectorizer,
    VECTORIZER_FILE
)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("FEATURE ENGINEERING COMPLETED")
print("========================================")

print("\nTF-IDF matrix shape:")
print(X_title.shape)

print("\nNumber of non-zero values:")
print(X_title.nnz)

print("\nNumber of text features:")
print(len(vectorizer.get_feature_names_out()))

print("\nTF-IDF feature file:")
print(FEATURE_FILE)

print("\nVectorizer file:")
print(VECTORIZER_FILE)