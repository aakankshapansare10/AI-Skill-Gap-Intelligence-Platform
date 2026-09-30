from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from scipy.sparse import load_npz

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    hamming_loss
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

X_TEST_FILE = (
    ROOT / "data" / "processed"
    / "X_test.npz"
)

Y_TEST_FILE = (
    ROOT / "data" / "processed"
    / "y_test.npz"
)

MODEL_FILE = (
    ROOT / "data" / "processed"
    / "skill_prediction_model.pkl"
)

SKILLS_FILE = (
    ROOT / "data" / "processed"
    / "model_skill_names.csv"
)

ALL_SKILLS_FILE = (
    ROOT / "data" / "processed"
    / "skill_feature_names.csv"
)

TEST_METADATA_FILE = (
    ROOT / "data" / "processed"
    / "test_metadata.csv"
)

RESULT_FILE = (
    ROOT / "data" / "processed"
    / "model_evaluation_results.csv"
)


# ============================================================
# 2. LOAD TEST DATA
# ============================================================

print("Loading test data...")

X_test = load_npz(X_TEST_FILE)

Y_test_full = load_npz(Y_TEST_FILE)

print("\nX_test shape:")
print(X_test.shape)

print("\nY_test shape:")
print(Y_test_full.shape)


# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

print("\nLoading trained model...")

model = joblib.load(MODEL_FILE)


# ============================================================
# 4. LOAD MODEL SKILL NAMES
# ============================================================

skill_data = pd.read_csv(SKILLS_FILE)

skill_names = (
    skill_data["skill"]
    .astype(str)
    .values
)

print("\nNumber of model skills:")
print(len(skill_names))


# ============================================================
# 5. LOAD ALL SKILL NAMES
# ============================================================

all_skill_names = (
    pd.read_csv(ALL_SKILLS_FILE)["skill"]
    .astype(str)
    .values
)


# Create skill → column index mapping

skill_to_index = {
    skill: index
    for index, skill in enumerate(all_skill_names)
}


# ============================================================
# 6. FIND MODEL SKILL INDICES
# ============================================================

selected_indices = []

valid_skill_names = []

for skill in skill_names:

    if skill in skill_to_index:

        selected_indices.append(
            skill_to_index[skill]
        )

        valid_skill_names.append(skill)


skill_names = np.array(
    valid_skill_names
)


print("\nNumber of matching model skills:")
print(len(skill_names))


# ============================================================
# 7. SELECT TEST TARGETS
# ============================================================

Y_test = Y_test_full[
    :,
    selected_indices
]


print("\nSelected Y_test shape:")
print(Y_test.shape)


# ============================================================
# 8. CONVERT TEST TARGET TO NUMPY
# ============================================================

if hasattr(Y_test, "toarray"):

    Y_test_dense = Y_test.toarray()

else:

    Y_test_dense = np.asarray(Y_test)


print("\nY_test evaluation shape:")
print(Y_test_dense.shape)


# ============================================================
# 9. MAKE PREDICTIONS
# ============================================================

print("\nMaking predictions...")

Y_pred = model.predict(X_test)


print("\nRaw prediction type:")
print(type(Y_pred))


# ============================================================
# 10. CONVERT PREDICTIONS CORRECTLY
# ============================================================

if hasattr(Y_pred, "toarray"):

    # Direct sparse matrix
    Y_pred_dense = Y_pred.toarray()

elif isinstance(Y_pred, np.ndarray):

    if Y_pred.dtype == object:

        # Model may return an object containing sparse matrix
        if Y_pred.ndim == 0:

            Y_pred = Y_pred.item()

        elif len(Y_pred) == 1:

            Y_pred = Y_pred[0]

        else:

            Y_pred = Y_pred.tolist()

        if hasattr(Y_pred, "toarray"):

            Y_pred_dense = Y_pred.toarray()

        else:

            Y_pred_dense = np.asarray(Y_pred)

    else:

        Y_pred_dense = Y_pred

else:

    Y_pred_dense = np.asarray(Y_pred)


# ============================================================
# 11. CHECK PREDICTION SHAPE
# ============================================================

print("\nY_pred evaluation shape:")
print(Y_pred_dense.shape)


# ============================================================
# 12. FINAL SHAPE CHECK
# ============================================================

if Y_test_dense.shape != Y_pred_dense.shape:

    raise ValueError(
        f"Shape mismatch!\n"
        f"Y_test: {Y_test_dense.shape}\n"
        f"Y_pred: {Y_pred_dense.shape}"
    )


print("\nShape check: PASSED")


# ============================================================
# 13. CALCULATE PRECISION
# ============================================================

print("\nCalculating evaluation metrics...")


precision = precision_score(
    Y_test_dense,
    Y_pred_dense,
    average="micro",
    zero_division=0
)


# ============================================================
# 14. CALCULATE RECALL
# ============================================================

recall = recall_score(
    Y_test_dense,
    Y_pred_dense,
    average="micro",
    zero_division=0
)


# ============================================================
# 15. CALCULATE F1 SCORE
# ============================================================

f1 = f1_score(
    Y_test_dense,
    Y_pred_dense,
    average="micro",
    zero_division=0
)


# ============================================================
# 16. CALCULATE HAMMING LOSS
# ============================================================

hamming = hamming_loss(
    Y_test_dense,
    Y_pred_dense
)


# ============================================================
# 17. DISPLAY MAIN RESULTS
# ============================================================

print("\n========================================")
print("MODEL EVALUATION RESULTS")
print("========================================")

print(
    f"\nPrecision    : {precision:.4f}"
)

print(
    f"Recall       : {recall:.4f}"
)

print(
    f"F1 Score     : {f1:.4f}"
)

print(
    f"Hamming Loss : {hamming:.6f}"
)


# ============================================================
# 18. PER-SKILL PERFORMANCE
# ============================================================

print("\nCalculating per-skill performance...")


skill_precision = precision_score(
    Y_test_dense,
    Y_pred_dense,
    average=None,
    zero_division=0
)


skill_recall = recall_score(
    Y_test_dense,
    Y_pred_dense,
    average=None,
    zero_division=0
)


skill_f1 = f1_score(
    Y_test_dense,
    Y_pred_dense,
    average=None,
    zero_division=0
)


# ============================================================
# 19. CREATE RESULTS DATAFRAME
# ============================================================

skill_results = pd.DataFrame(
    {
        "skill": skill_names,
        "precision": skill_precision,
        "recall": skill_recall,
        "f1_score": skill_f1
    }
)


# Sort by F1 score

skill_results = skill_results.sort_values(
    "f1_score",
    ascending=False
)


# ============================================================
# 20. SAVE EVALUATION RESULTS
# ============================================================

skill_results.to_csv(
    RESULT_FILE,
    index=False
)


# ============================================================
# 21. TOP 10 SKILLS
# ============================================================

print("\n========================================")
print("TOP 10 SKILLS BY F1 SCORE")
print("========================================")

print(
    skill_results
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 22. BOTTOM 10 SKILLS
# ============================================================

print("\n========================================")
print("BOTTOM 10 SKILLS BY F1 SCORE")
print("========================================")

print(
    skill_results
    .tail(10)
    .to_string(index=False)
)


# ============================================================
# 23. ACTUAL VS PREDICTED EXAMPLES
# ============================================================

print("\n========================================")
print("ACTUAL VS PREDICTED EXAMPLES")
print("========================================")


test_metadata = pd.read_csv(
    TEST_METADATA_FILE
)


number_of_examples = min(
    5,
    len(test_metadata)
)


for i in range(number_of_examples):

    # Actual skill indices

    actual_indices = np.where(
        Y_test_dense[i] == 1
    )[0]


    # Predicted skill indices

    predicted_indices = np.where(
        Y_pred_dense[i] == 1
    )[0]


    # Convert indices to skill names

    actual_skills = [
        skill_names[index]
        for index in actual_indices
    ]


    predicted_skills = [
        skill_names[index]
        for index in predicted_indices
    ]


    print("\n----------------------------------------")

    print(
        "Job:",
        test_metadata.iloc[i]["title"]
    )


    print("\nActual skills:")

    print(
        actual_skills[:15]
    )


    print("\nPredicted skills:")

    print(
        predicted_skills[:15]
    )


# ============================================================
# 24. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("EVALUATION COMPLETED SUCCESSFULLY")
print("========================================")

print("\nEvaluation file saved at:")

print(RESULT_FILE)