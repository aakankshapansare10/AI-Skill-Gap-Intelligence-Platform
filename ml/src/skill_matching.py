import pandas as pd


def normalize_skill(skill):
    return skill.strip().lower()


def calculate_skill_match(student_skills, required_skills):

    student_set = {
        normalize_skill(skill)
        for skill in student_skills
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
    }

    matching_skills = student_set.intersection(required_set)

    missing_skills = required_set.difference(student_set)

    if len(required_set) > 0:
        skill_gap_percentage = (
            len(missing_skills) / len(required_set)
        ) * 100
    else:
        skill_gap_percentage = 0

    if len(required_set) > 0:
        job_match_score = (
            len(matching_skills) / len(required_set)
        )
    else:
        job_match_score = 0

    return {
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "skill_gap_percentage": round(skill_gap_percentage, 2),
        "job_match_score": round(job_match_score, 4)
    }


if __name__ == "__main__":

    print("=" * 60)
    print("TESTING SKILL MATCHING")
    print("=" * 60)

    student_skills = [
        "Python",
        "SQL",
        "Excel",
        "Machine Learning"
    ]

    required_skills = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau"
    ]

    result = calculate_skill_match(
        student_skills,
        required_skills
    )

    print()
    print("Student Skills:")
    print(student_skills)

    print()
    print("Required Job Skills:")
    print(required_skills)

    print()
    print("Matching Skills:")
    print(result["matching_skills"])

    print()
    print("Missing Skills:")
    print(result["missing_skills"])

    print()
    print("Skill Gap Percentage:")
    print(result["skill_gap_percentage"], "%")

    print()
    print("Job Match Score:")
    print(result["job_match_score"])

    print()
    print("=" * 60)
    print("SKILL MATCHING TEST COMPLETED")
    print("=" * 60)