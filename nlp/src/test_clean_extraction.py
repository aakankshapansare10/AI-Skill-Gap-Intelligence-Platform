import pandas as pd

from database import get_engine
from text_preprocessing import preprocess_text
from skill_extraction import (
    load_skills,
    build_automaton,
    extract_skills_from_text
)


# ============================================================
# TEST ONE PROBLEMATIC JOB
# ============================================================

JOB_ID = 240925000000


print("=" * 70)
print("CLEAN NLP EXTRACTION TEST")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load skills
# ------------------------------------------------------------

skills_df = load_skills()

print(f"\nSkills loaded: {len(skills_df):,}")


# ------------------------------------------------------------
# 2. Build Aho-Corasick matcher
# ------------------------------------------------------------

automaton = build_automaton(skills_df)


# ------------------------------------------------------------
# 3. Load the specific job
# ------------------------------------------------------------

engine = get_engine()

query = f"""
SELECT
    job_id,
    title,
    job_description
FROM public.jobs
WHERE job_id = {JOB_ID}
"""

job_df = pd.read_sql_query(query, engine)

engine.dispose()


# ------------------------------------------------------------
# 4. Check job exists
# ------------------------------------------------------------

if job_df.empty:
    print(f"\nERROR: Job {JOB_ID} was not found.")
    raise SystemExit


job = job_df.iloc[0]

print("\nJob found:")
print(f"Job ID: {job['job_id']}")
print(f"Title: {job['title']}")


# ------------------------------------------------------------
# 5. Extract skills
# ------------------------------------------------------------

description = job["job_description"]

extracted_skills = extract_skills_from_text(
    description,
    automaton
)


# ------------------------------------------------------------
# 6. Display results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EXTRACTION RESULT")
print("=" * 70)

print(f"\nTotal extracted skills: {len(extracted_skills):,}")


# ------------------------------------------------------------
# 7. Show all extracted skills
# ------------------------------------------------------------

print("\nExtracted skills:")

for skill in extracted_skills:
    print(
        f"{skill['skill_id']:>6}  "
        f"{skill['skill_name']}"
    )


# ------------------------------------------------------------
# 8. Short-skill analysis
# ------------------------------------------------------------

short_skills = []

for skill in extracted_skills:
    name = str(skill["skill_name"]).strip()

    if len(name) <= 2:
        short_skills.append(name)


print("\n" + "=" * 70)
print("SHORT SKILL CHECK")
print("=" * 70)

print(
    f"\nSkills with <= 2 characters: "
    f"{len(short_skills):,}"
)

if short_skills:
    print("\nThese are the <=2 character skills:")
    print(", ".join(short_skills))


# ------------------------------------------------------------
# 9. Final message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)