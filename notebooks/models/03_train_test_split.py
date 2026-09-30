from pathlib import Path

import pandas as pd
import numpy as np

from scipy.sparse import load_npz, save_npz
from sklearn.model_selection import train_test_split


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

# Input files
SKILL_MATRIX_FILE = (
    ROOT / "data" / "processed"
    / "skill_features.npz"
)

TITLE_FEATURE_FILE = (
    ROOT / "data" / "processed"
    / "title_tfidf_features.npz"
)

JOB_METADATA_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_metadata.csv"
)


# Output files
X_TRAIN_FILE = (
    ROOT / "data" / "processed"
    / "X_train.npz"
)

X_TEST_FILE = (
    ROOT / "data" / "processed"
    / "X_test.npz"
)

Y_TRAIN_FILE = (
    ROOT / "data" / "processed"
    / "y_train.npz"
)

Y_TEST_FILE = (
    ROOT / "data" / "processed"
    / "y_test.npz"
)

TRAIN_METADATA_FILE = (
    ROOT / "data" / "processed"
    / "train_metadata.csv"
)

TEST_METADATA_FILE = (
    ROOT / "data" / "processed"
    / "test_metadata.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("Loading feature matrices...")

X = load_npz(TITLE_FEATURE_FILE)

Y = load_npz(SKILL_MATRIX_FILE)

metadata = pd.read_csv(JOB_METADATA_FILE)


print("\nTitle feature matrix shape:")
print(X.shape)

print("\nSkill target matrix shape:")
print(Y.shape)

print("\nMetadata shape:")
print(metadata.shape)


# ============================================================
# 3. CHECK DATA ALIGNMENT
# ============================================================

if X.shape[0] != Y.shape[0]:
    raise ValueError(
        "X and Y have different numbers of jobs."
    )

if X.shape[0] != len(metadata):
    raise ValueError(
        "Feature matrices and metadata are not aligned."
    )


print("\nData alignment check: PASSED")


# ============================================================
# 4. CREATE JOB INDICES
# ============================================================

indices = np.arange(X.shape[0])


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

print("\nCreating train/test split...")

train_indices, test_indices = train_test_split(
    indices,
    test_size=0.20,
    random_state=42
)


print("\nTraining jobs:")
print(len(train_indices))

print("\nTesting jobs:")
print(len(test_indices))


# ============================================================
# 6. CREATE TRAINING FEATURES
# ============================================================

X_train = X[train_indices]

X_test = X[test_indices]


# ============================================================
# 7. CREATE TRAINING TARGETS
# ============================================================

Y_train = Y[train_indices]

Y_test = Y[test_indices]


# ============================================================
# 8. SAVE TRAIN / TEST MATRICES
# ============================================================

save_npz(
    X_TRAIN_FILE,
    X_train
)

save_npz(
    X_TEST_FILE,
    X_test
)

save_npz(
    Y_TRAIN_FILE,
    Y_train
)

save_npz(
    Y_TEST_FILE,
    Y_test
)


# ============================================================
# 9. SAVE METADATA
# ============================================================

train_metadata = metadata.iloc[
    train_indices
].reset_index(drop=True)

test_metadata = metadata.iloc[
    test_indices
].reset_index(drop=True)


train_metadata.to_csv(
    TRAIN_METADATA_FILE,
    index=False
)

test_metadata.to_csv(
    TEST_METADATA_FILE,
    index=False
)


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("TRAIN / TEST SPLIT COMPLETED")
print("========================================")

print("\nX_train shape:")
print(X_train.shape)

print("\nX_test shape:")
print(X_test.shape)

print("\nY_train shape:")
print(Y_train.shape)

print("\nY_test shape:")
print(Y_test.shape)

print("\nTraining metadata:")
print(train_metadata.shape)

print("\nTesting metadata:")
print(test_metadata.shape)


# ============================================================
# 11. CHECK SPARSITY
# ============================================================

print("\nX_train non-zero values:")
print(X_train.nnz)

print("\nX_test non-zero values:")
print(X_test.nnz)

print("\nY_train non-zero values:")
print(Y_train.nnz)

print("\nY_test non-zero values:")
print(Y_test.nnz)


# ============================================================
# 12. OUTPUT FILES
# ============================================================

print("\nFiles created:")

print(X_TRAIN_FILE)
print(X_TEST_FILE)
print(Y_TRAIN_FILE)
print(Y_TEST_FILE)
print(TRAIN_METADATA_FILE)
print(TEST_METADATA_FILE)