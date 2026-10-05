import re


SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "C#",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Power BI",
    "Tableau",
    "Excel",
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "Linux",
]


def extract_skills(text):
    """
    Extract known skills from text.
    """

    if not isinstance(text, str):
        return []

    found_skills = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            found_skills.append(skill)

    return found_skills