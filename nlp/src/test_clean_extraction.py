import pandas as pd
import ahocorasick

from database import get_engine
from text_preprocessing import preprocess_text


def load_clean_skills():

    print("Loading CLEAN skill dictionary...")

    skills_df = pd.read_csv(
        "../../data/processed/skills_dictionary_clean.csv"
    )

    print(f"Clean skills loaded: {len(skills_df):,}")

    return skills_df


def build_automaton(skills_df):

    print("\nBuilding Aho-Corasick matcher...")

    automaton = ahocorasick.Automaton()

    pattern_to_skill = {}

    for _, row in skills_df.iterrows():

        skill_id = int(row["skill_id"])
        skill_name = str(row["skill_name"]).strip()

        normalized = preprocess_text(skill_name).strip()

        if not normalized:
            continue

        # Reject one-character alphabetic terms
        if len(normalized) == 1 and normalized.isalpha():
            continue

        pattern = f" {normalized} "

        if pattern not in pattern_to_skill:

            pattern_to_skill[pattern] = {
                "skill_id": skill_id,
                "skill_name": skill_name
            }

    for pattern, skill in pattern_to_skill.items():

        automaton.add_word(
            pattern,
            skill
        )

    automaton.make_automaton()

    print(
        f"Usable patterns: {len(pattern_to_skill):,}"
    )

    return automaton


def extract_skills(text, automaton):

    normalized_text = preprocess_text(
        text
    ).strip()

    padded_text = f" {normalized_text} "

    found = {}

    for _, skill in automaton.iter(
        padded_text
    ):

        skill_id = skill["skill_id"]

        if skill_id not in found:

            found[skill_id] = skill

    return list(found.values())


def load_test_job():

    engine = get_engine()

    query = """
        SELECT job_id, title, job_description
        FROM public.jobs
        WHERE job_id = 240925000000
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    engine.dispose()

    return df


if __name__ == "__main__":

    print("=" * 70)
    print("CLEAN NLP EXTRACTION TEST")
    print("=" * 70)

    skills_df = load_clean_skills()

    automaton = build_automaton(
        skills_df
    )

    job_df = load_test_job()

    if job_df.empty:

        print(
            "\nERROR: Test job not found."
        )

        exit()

    job = job_df.iloc[0]

    print("\nTest Job:")
    print(f"Job ID: {job['job_id']}")
    print(f"Title : {job['title']}")

    results = extract_skills(
        job["job_description"],
        automaton
    )

    print(
        f"\nExtracted skills: {len(results)}"
    )

    print("\nExtracted skill list:")

    for skill in results:

        print(
            f"{skill['skill_id']:>6} | "
            f"{skill['skill_name']}"
        )

    short_skills = [
        skill
        for skill in results
        if len(str(skill["skill_name"]).strip()) <= 2
    ]

    print(
        f"\nSkills <= 2 characters: "
        f"{len(short_skills)}"
    )

    if short_skills:

        print("\nWARNING - short skills found:")

        for skill in short_skills:

            print(
                skill["skill_id"],
                skill["skill_name"]
            )

    print("\nTest completed.")