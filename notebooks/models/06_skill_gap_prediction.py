from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from scipy.sparse import load_npz


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    ROOT / "data" / "processed"
    / "skill_prediction_model.pkl"
)

SKILLS_FILE = (
    ROOT / "data" / "processed"
    / "model_skill_names.csv"
)

X_TEST_FILE = (
    ROOT / "data" / "processed"
    / "X_test.npz"
)

TEST_METADATA_FILE = (
    ROOT / "data" / "processed"
    / "test_metadata.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_predictions.csv"
)


# ============================================================
# 2. LOAD MODEL
# ============================================================

print("Loading trained skill prediction model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# 3. LOAD SKILLS
# ============================================================

print("\nLoading model skill names...")

skill_data = pd.read_csv(SKILLS_FILE)

skill_names = (
    skill_data["skill"]
    .astype(str)
    .values
)

print(
    f"Number of model skills: {len(skill_names)}"
)


# ============================================================
# 4. LOAD TEST DATA
# ============================================================

print("\nLoading test job data...")

X_test = load_npz(X_TEST_FILE)

test_metadata = pd.read_csv(
    TEST_METADATA_FILE
)

print(
    f"Number of test jobs: {len(test_metadata)}"
)


# ============================================================
# 5. GET DECISION SCORES
# ============================================================

print("\nCalculating skill relevance scores...")

decision_scores = model.decision_function(
    X_test
)


# ============================================================
# 6. CONVERT SCORES TO NUMPY
# ============================================================

if hasattr(decision_scores, "toarray"):

    decision_scores = (
        decision_scores.toarray()
    )

else:

    decision_scores = np.asarray(
        decision_scores
    )


print("\nDecision score matrix shape:")

print(
    decision_scores.shape
)


# ============================================================
# 7. STUDENT SKILLS
# ============================================================

student_skills = [
    "Python",
    "SQL",
    "Excel",
    "Communication"
]


print("\n========================================")
print("STUDENT SKILLS")
print("========================================")

print(
    student_skills
)


# ============================================================
# 8. FUNCTION TO GET TOP SKILLS
# ============================================================

def get_top_skills(
    scores,
    skill_names,
    top_n=10
):

    # Get indices of highest scores

    top_indices = np.argsort(
        scores
    )[-top_n:][::-1]


    skills = []

    for index in top_indices:

        skills.append(
            skill_names[index]
        )

    return skills


# ============================================================
# 9. FUNCTION TO CALCULATE SKILL GAP
# ============================================================

def calculate_skill_gap(
    required_skills,
    student_skills
):

    required_set = {
        skill.strip().lower()
        for skill in required_skills
    }

    student_set = {
        skill.strip().lower()
        for skill in student_skills
    }


    matching_skills = (
        required_set.intersection(
            student_set
        )
    )


    missing_skills = (
        required_set - student_set
    )


    return (
        matching_skills,
        missing_skills
    )


# ============================================================
# 10. CREATE RESULTS
# ============================================================

results = []


# Number of skills to predict per job

TOP_SKILLS = 10


print(
    f"\nSelecting top {TOP_SKILLS} skills "
    "for each job..."
)


for i in range(
    len(test_metadata)
):

    job_title = test_metadata.iloc[i][
        "title"
    ]


    # Get model scores for this job

    scores = decision_scores[i]


    # Select highest scoring skills

    required_skills = get_top_skills(
        scores,
        skill_names,
        TOP_SKILLS
    )


    # Calculate skill gap

    matching_skills, missing_skills = (
        calculate_skill_gap(
            required_skills,
            student_skills
        )
    )


    # Calculate gap percentage

    total_required = len(
        required_skills
    )

    total_missing = len(
        missing_skills
    )


    if total_required > 0:

        gap_percentage = (
            total_missing /
            total_required
        ) * 100

    else:

        gap_percentage = 0


    # Store result

    results.append(
        {
            "job_title":
                job_title,

            "required_skills":
                ", ".join(
                    required_skills
                ),

            "student_skills":
                ", ".join(
                    student_skills
                ),

            "matching_skills":
                ", ".join(
                    sorted(
                        matching_skills
                    )
                ),

            "missing_skills":
                ", ".join(
                    sorted(
                        missing_skills
                    )
                ),

            "total_required_skills":
                total_required,

            "total_matching_skills":
                len(
                    matching_skills
                ),

            "total_missing_skills":
                total_missing,

            "skill_gap_percentage":
                round(
                    gap_percentage,
                    2
                )
        }
    )


# ============================================================
# 11. CREATE DATAFRAME
# ============================================================

results_df = pd.DataFrame(
    results
)


# ============================================================
# 12. SAVE RESULTS
# ============================================================

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 13. DISPLAY EXAMPLES
# ============================================================

print("\n========================================")
print("IMPROVED SKILL GAP PREDICTION")
print("========================================")


for i in range(
    min(5, len(results_df))
):

    row = results_df.iloc[i]


    print("\n----------------------------------------")

    print(
        "Job:",
        row["job_title"]
    )


    print(
        "\nRequired skills:"
    )

    print(
        row["required_skills"]
    )


    print(
        "\nStudent skills:"
    )

    print(
        row["student_skills"]
    )


    print(
        "\nMatching skills:"
    )

    print(
        row["matching_skills"]
    )


    print(
        "\nMissing skills:"
    )

    print(
        row["missing_skills"]
    )


    print(
        "\nSkill gap:"
        f" {row['skill_gap_percentage']}%"
    )


# ============================================================
# 14. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("IMPROVED SKILL GAP PREDICTION COMPLETED")
print("========================================")

print("\nOutput file:")

print(
    OUTPUT_FILE
)