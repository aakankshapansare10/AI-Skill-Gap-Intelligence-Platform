import pandas as pd

from database import load_jobs
from skill_extraction import load_skills
from skill_extraction import build_skill_dictionary
from skill_extraction import extract_skills


def extract_all_job_skills():

    # --------------------------------------------------
    # 1. Load jobs from PostgreSQL
    # --------------------------------------------------

    print("Loading jobs...")

    jobs_df = load_jobs()

    print("Jobs loaded:", len(jobs_df))

    # --------------------------------------------------
    # 2. Load skills from PostgreSQL
    # --------------------------------------------------

    print("\nLoading skills...")

    skills_df = load_skills()

    print("Skills loaded:", len(skills_df))

    # --------------------------------------------------
    # 3. Build skill dictionary
    # --------------------------------------------------

    print("\nBuilding skill dictionary...")

    skill_dictionary = build_skill_dictionary(skills_df)

    print(
        "Usable skills:",
        len(skill_dictionary)
    )

    # --------------------------------------------------
    # 4. Extract skills from every job
    # --------------------------------------------------

    results = []

    total_jobs = len(jobs_df)

    print("\nStarting skill extraction...\n")

    for counter, (_, row) in enumerate(
        jobs_df.iterrows(),
        start=1
    ):

        description = row["job_description"]

        extracted = extract_skills(
            description,
            skill_dictionary
        )

        for skill in extracted:

            results.append(
                {
                    "job_id": row["job_id"],
                    "skill_id": skill["skill_id"],
                    "skill_name": skill["skill_name"]
                }
            )

        # Progress message
        if counter % 100 == 0 or counter == total_jobs:

            print(
                f"Processed {counter}/{total_jobs} jobs"
            )

    # --------------------------------------------------
    # 5. Convert results to DataFrame
    # --------------------------------------------------

    result_df = pd.DataFrame(results)

    # --------------------------------------------------
    # 6. Remove duplicate job-skill combinations
    # --------------------------------------------------

    if not result_df.empty:

        result_df = result_df.drop_duplicates(
            subset=[
                "job_id",
                "skill_id"
            ]
        )

    return result_df


if __name__ == "__main__":

    result_df = extract_all_job_skills()

    # --------------------------------------------------
    # 7. Save NLP output
    # --------------------------------------------------

    output_file = (
        "../../data/processed/job_skill_extraction.csv"
    )

    result_df.to_csv(
        output_file,
        index=False
    )

    print("\n" + "=" * 70)

    print("EXTRACTION COMPLETED")

    print("=" * 70)

    print(
        "Total job-skill matches:",
        len(result_df)
    )

    if not result_df.empty:

        print(
            "Unique jobs with extracted skills:",
            result_df["job_id"].nunique()
        )

        print(
            "Unique extracted skills:",
            result_df["skill_id"].nunique()
        )

        print("\nFirst 20 results:")

        print(
            result_df.head(20).to_string(
                index=False
            )
        )

    print(
        "\nOutput saved to:",
        output_file
    )