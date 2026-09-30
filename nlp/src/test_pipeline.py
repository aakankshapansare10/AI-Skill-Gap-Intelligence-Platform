from text_cleaner import clean_text
from skill_extracter import extract_skills
from skill_normalizer import normalize_skills


job_description = """
We need a Data Analyst who knows Python,
SQL, sklearn, postgres and PowerBI.
Experience with ML is preferred.
"""


cleaned_text = clean_text(job_description)

extracted_skills = extract_skills(cleaned_text)

normalized_skills = normalize_skills(extracted_skills)


print("Cleaned Text:")
print(cleaned_text)

print("\nExtracted Skills:")
print(extracted_skills)

print("\nNormalized Skills:")
print(normalized_skills)