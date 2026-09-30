SKILL_ALIASES = {
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "powerbi": "Power BI",
    "power bi": "Power BI",

    "ml": "Machine Learning",
    "machine-learning": "Machine Learning",

    "nlp": "Natural Language Processing",
}


def normalize_skill(skill):
    """
    Convert skill variations into a standard skill name.
    """

    key = skill.lower().strip()

    return SKILL_ALIASES.get(key, skill)


def normalize_skills(skills):
    """
    Normalize a list of extracted skills.
    """

    normalized = []

    for skill in skills:

        standard_skill = normalize_skill(skill)

        if standard_skill not in normalized:
            normalized.append(standard_skill)

    return normalized