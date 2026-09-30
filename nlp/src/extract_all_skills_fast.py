import re
import pandas as pd
import ahocorasick

from database import load_jobs
from skill_extraction import load_skills
from text_preprocessing import preprocess_text


def build_automaton(skills_df):
    """
    Build an Aho-Corasick automaton from the skill dictionary.
    This allows fast matching of many skills at once.
    """

    automaton = ahocorasick.Automaton()

    valid_skills = 0

    for _, row in skills_df.iterrows():

        skill_id = row["skill_id"]
        skill_name = row["skill_name"]

        if not isinstance(skill_name, str):
            continue

        normalized_skill = preprocess_text(skill_name)

        if not normalized_skill:
            continue

        # Store both ID and original name
        automaton.add_word(
            normalized_skill,
            (skill_id, skill_name)
        )

        valid_skills += 1

    automaton.make_automaton()

    return automaton, valid_skills


def extract_skills_fast(text, automaton):

    if not isinstance(text, str):
        return []

    normalized_text = preprocess_text(text)

    found = {}

    for end_position, skill_data in automaton.iter(
        normalized_text
    ):

        skill_id, skill_name = skill_data

        # Find the start position of the match
        start_position = (
            end_position
            - len(preprocess_text(skill_name))
            + 1
        )

        # Check word boundaries
        before_ok = (
            start_position == 0
            or not normalized_text[
                start_position - 1
            ].isalnum()
        )

        after_ok = (
            end_position == len(normalized_text) - 1
            or not normalized_text[
                end_position + 1
            ].isalnum()
        )

        if before_ok and after_ok:

            found[skill_id] = {
                "skill_id": skill_id,
                "skill_name": skill_name
            }

    return list(found.values())


def main():

    print("=" * 70)
    print("FAST NLP SKILL EXTRACTION")
    print("=" * 70)

    # --------------------------------------------------
    # Load jobs
    # --------------------------------------------------

    print("\nLoading jobs...")

    jobs_df = load_jobs()

    print(
        "Total jobs:",
        len(jobs_df)
    )

    # --------------------------------------------------
    # Load skills
    # --------------------------------------------------

    print("\nLoading skills...")

    skills_df = load_skills()

    print(
        "Total skills:",
        len(skills_df)
    )

    # --------------------------------------------------
    # Build optimized matcher
    # --------------------------------------------------

    print("\nBuilding optimized skill matcher...")

    automaton, valid_skills = build_automaton(
        skills_df
    )

    print(
        "Skills added to matcher:",
        valid_skills
    )

    # --------------------------------------------------
    # Test matcher
    # --------------------------------------------------

    print("\nTesting matcher...")

    test_text = """
    We are looking for a Data Scientist
    with Python, SQL and Machine Learning experience.
    """

    test_results = extract_skills_fast(
        test_text,
        automaton
    )

    print("\nTest results:")

    for skill in test_results:

        print(
            "-",
            skill["skill_id"],
            ":",
            skill["skill_name"]
        )

    # --------------------------------------------------
    # Process jobs
    # --------------------------------------------------

    print("\nStarting extraction for all jobs...\n")

    results = []

    total_jobs = len(jobs_df)

    for counter, (_, row) in enumerate(
        jobs_df.iterrows(),
        start=1
    ):

        extracted = extract_skills_fast(
            row["job_description"],
            automaton
        )

        for skill in extracted:

            results.append(
                {
                    "job_id": row["job_id"],
                    "skill_id": skill["skill_id"],
                    "skill_name": skill["skill_name"]
                }
            )

        if (
            counter % 100 == 0
            or counter == total_jobs
        ):

            print(
                f"Processed {counter}/{total_jobs} jobs"
            )

    # --------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------

    result_df = pd.DataFrame(results)

    if not result_df.empty:

        result_df = result_df.drop_duplicates(
            subset=[
                "job_id",
                "skill_id"
            ]
        )

    # --------------------------------------------------
    # Save output
    # --------------------------------------------------

    output_file = (
        "../../data/processed/"
        "job_skill_extraction.csv"
    )

    result_df.to_csv(
        output_file,
        index=False
    )

    # --------------------------------------------------
    # Final statistics
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETED")
    print("=" * 70)

    print(
        "Total job-skill matches:",
        len(result_df)
    )

    if not result_df.empty:

        print(
            "Jobs with extracted skills:",
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
        "\nSaved to:",
        output_file
    )


if __name__ == "__main__":
    main()