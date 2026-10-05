from text_cleaner import clean_text


sample_text = """
We are looking for a Data Analyst.

The candidate should have experience with
Python, SQL, Power BI and Tableau.
"""


cleaned = clean_text(sample_text)

print("Original:")
print(sample_text)

print("\nCleaned:")
print(cleaned)