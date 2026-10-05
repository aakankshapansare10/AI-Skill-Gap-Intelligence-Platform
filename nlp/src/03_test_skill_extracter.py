from skill_extracter import extract_skills


job_description = """
We are looking for a Data Analyst with experience in
Python, SQL, Power BI and Tableau.

Knowledge of Pandas and Machine Learning is preferred.
"""


skills = extract_skills(job_description)

print("Extracted Skills:")
for skill in skills:
    print("-", skill)
