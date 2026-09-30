from database import load_jobs
from skill_extraction import load_skills
from skill_extraction import build_skill_dictionary
from skill_extraction import extract_skills


# Load jobs
jobs_df = load_jobs()

# Load skills
skills_df = load_skills()

# Build efficient skill dictionary
skill_dictionary = build_skill_dictionary(skills_df)

print("Total jobs:", len(jobs_df))
print("Total skills:", len(skills_df))
print("Usable skills:", len(skill_dictionary))


# Test first 5 jobs
for _, row in jobs_df.head(5).iterrows():

    print("\n" + "=" * 80)

    print("Job ID:", row["job_id"])
    print("Title:", row["title"])

    print("\nDescription:")
    print(row["job_description"])

    extracted = extract_skills(
        row["job_description"],
        skill_dictionary
    )

    print("\nExtracted Skills:")

    if extracted:

        for skill in extracted:
            print(
                "-",
                skill["skill_id"],
                ":",
                skill["skill_name"]
            )

    else:

        print("No known skills detected.")