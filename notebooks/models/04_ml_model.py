from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from scipy.sparse import load_npz

from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

X_TRAIN_FILE = (
    ROOT / "data" / "processed"
    / "X_train.npz"
)

Y_TRAIN_FILE = (
    ROOT / "data" / "processed"
    / "y_train.npz"
)

SKILL_NAMES_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_names.csv"
)

MODEL_FILE = (
    ROOT / "data" / "processed"
    / "skill_prediction_model.pkl"
)

SELECTED_SKILLS_FILE = (
    ROOT / "data" / "processed"
    / "model_skill_names.csv"
)


# ============================================================
# 2. LOAD TRAINING DATA
# ============================================================

print("Loading training data...")

X_train = load_npz(X_TRAIN_FILE)

Y_train = load_npz(Y_TRAIN_FILE)

skill_names = pd.read_csv(
    SKILL_NAMES_FILE
)["skill"].astype(str).values


print("\nX_train shape:")
print(X_train.shape)

print("\nY_train shape:")
print(Y_train.shape)

print("\nNumber of skills:")
print(len(skill_names))


# ============================================================
# 3. FIND MOST FREQUENT SKILLS
# ============================================================

print("\nFinding most frequent skills...")

skill_frequency = np.asarray(
    Y_train.sum(axis=0)
).ravel()


# Number of skills used by the model
TOP_SKILLS = 300


# Get indices of the most frequent skills
top_skill_indices = np.argsort(
    skill_frequency
)[-TOP_SKILLS:]


# Sort them from most frequent to least frequent
top_skill_indices = top_skill_indices[
    np.argsort(
        skill_frequency[top_skill_indices]
    )[::-1]
]


selected_skill_names = (
    skill_names[top_skill_indices]
)


print("\nNumber of selected skills:")
print(len(selected_skill_names))


print("\nTop 20 skills:")

for i, skill in enumerate(
    selected_skill_names[:20],
    start=1
):
    index = top_skill_indices[i - 1]

    print(
        f"{i}. {skill} "
        f"({int(skill_frequency[index])} jobs)"
    )


# ============================================================
# 4. SELECT TARGET COLUMNS
# ============================================================

Y_train_selected = (
    Y_train[:, top_skill_indices]
)


print("\nSelected target matrix shape:")
print(Y_train_selected.shape)


# ============================================================
# 5. CREATE ML MODEL
# ============================================================

print("\nCreating ML model...")

base_model = SGDClassifier(
    loss="log_loss",
    penalty="l2",
    alpha=0.0001,
    max_iter=100,
    tol=1e-3,
    random_state=42
)


model = OneVsRestClassifier(
    base_model,
    n_jobs=-1
)


# ============================================================
# 6. TRAIN MODEL
# ============================================================

print("\nTraining model...")
print("This may take some time.")

model.fit(
    X_train,
    Y_train_selected
)


print("\nModel training completed!")


# ============================================================
# 7. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)


# ============================================================
# 8. SAVE SELECTED SKILL NAMES
# ============================================================

pd.DataFrame(
    {
        "skill": selected_skill_names,
        "frequency": skill_frequency[
            top_skill_indices
        ].astype(int)
    }
).to_csv(
    SELECTED_SKILLS_FILE,
    index=False
)


# ============================================================
# 9. MODEL INFORMATION
# ============================================================

print("\n========================================")
print("ML MODEL TRAINING COMPLETED")
print("========================================")

print("\nModel:")
print("One-vs-Rest SGD Classifier")

print("\nTraining samples:")
print(X_train.shape[0])

print("\nInput features:")
print(X_train.shape[1])

print("\nSkills predicted by model:")
print(len(selected_skill_names))

print("\nModel file:")
print(MODEL_FILE)

print("\nSelected skills file:")
print(SELECTED_SKILLS_FILE)