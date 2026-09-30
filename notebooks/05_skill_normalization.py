import pandas as pd
import re

INPUT_PATH = "data/processed/job_skills.csv"
OUTPUT_PATH = "data/processed/normalized_job_skills.csv"

df = pd.read_csv(INPUT_PATH)

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 5 - SKILL NORMALIZATION")
print("=" * 70)

print(f"Original job-skill records: {len(df):,}")
print(f"Original unique skills: {df['skill'].nunique():,}")


def normalize_skill(skill):
    skill = str(skill).strip()

    skill = re.sub(r"\s+", " ", skill)

    skill = skill.strip(" ,.;:-_")

    skill_lower = skill.lower()

    aliases = {
        "python": "Python",
        "python programming": "Python",
        "python language": "Python",

        "sql": "SQL",
        "structured query language": "SQL",

        "java": "Java",
        "java programming": "Java",

        "javascript": "JavaScript",
        "java script": "JavaScript",
        "js": "JavaScript",

        "typescript": "TypeScript",

        "c++": "C++",
        "cpp": "C++",

        "c#": "C#",
        "c sharp": "C#",

        "html": "HTML",
        "html5": "HTML",

        "css": "CSS",
        "css3": "CSS",

        "react": "React",
        "reactjs": "React",
        "react.js": "React",

        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",

        "angular": "Angular",
        "angularjs": "Angular",

        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "vue.js": "Vue.js",

        "power bi": "Power BI",
        "powerbi": "Power BI",
        "power-bi": "Power BI",

        "tableau": "Tableau",

        "excel": "Microsoft Excel",
        "ms excel": "Microsoft Excel",
        "microsoft excel": "Microsoft Excel",

        "ms office": "Microsoft Office",
        "m.s office": "Microsoft Office",
        "microsoft office": "Microsoft Office",
        "msoffice": "Microsoft Office",

        "machine learning": "Machine Learning",
        "ml": "Machine Learning",

        "artificial intelligence": "Artificial Intelligence",
        "ai": "Artificial Intelligence",

        "deep learning": "Deep Learning",
        "dl": "Deep Learning",

        "natural language processing": "Natural Language Processing",
        "nlp": "Natural Language Processing",

        "data science": "Data Science",
        "data analytics": "Data Analytics",
        "data analysis": "Data Analysis",

        "pandas": "Pandas",
        "numpy": "NumPy",

        "scikit learn": "Scikit-learn",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",

        "matplotlib": "Matplotlib",
        "seaborn": "Seaborn",
        "plotly": "Plotly",

        "tensorflow": "TensorFlow",
        "keras": "Keras",
        "pytorch": "PyTorch",

        "aws": "AWS",
        "amazon web services": "AWS",

        "azure": "Microsoft Azure",
        "microsoft azure": "Microsoft Azure",

        "gcp": "Google Cloud Platform",
        "google cloud": "Google Cloud Platform",
        "google cloud platform": "Google Cloud Platform",

        "docker": "Docker",
        "kubernetes": "Kubernetes",

        "git": "Git",
        "github": "GitHub",
        "git hub": "GitHub",

        "jenkins": "Jenkins",

        "spark": "Apache Spark",
        "apache spark": "Apache Spark",

        "hadoop": "Hadoop",
        "hive": "Apache Hive",
        "apache hive": "Apache Hive",

        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",

        "mysql": "MySQL",

        "mongodb": "MongoDB",
        "mongo db": "MongoDB",

        "rest": "REST API",
        "rest api": "REST API",
        "restful api": "REST API",

        "fastapi": "FastAPI",
        "fast api": "FastAPI",

        "flask": "Flask",
        "django": "Django",

        "communication skills": "Communication",
        "communication": "Communication",

        "customer service": "Customer Service",
        "customer support": "Customer Support",

        "business development": "Business Development",
        "project management": "Project Management",

        "sales": "Sales",
        "marketing": "Marketing",

        "sap": "SAP"
    }

    if skill_lower in aliases:
        return aliases[skill_lower]

    if skill.isupper() and len(skill) <= 5:
        return skill

    return skill


df["normalized_skill"] = df["skill"].apply(normalize_skill)

df = df[
    [
        "jobId",
        "title",
        "skill",
        "normalized_skill"
    ]
]

df = df.drop_duplicates(
    subset=[
        "jobId",
        "normalized_skill"
    ]
)

df = df.reset_index(drop=True)

df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 70)
print("NORMALIZATION RESULTS")
print("=" * 70)

print(
    f"Final job-skill records: "
    f"{len(df):,}"
)

print(
    f"Unique original skills: "
    f"{df['skill'].nunique():,}"
)

print(
    f"Unique normalized skills: "
    f"{df['normalized_skill'].nunique():,}"
)

print("\nSample normalized skills:")

print(
    df[
        [
            "skill",
            "normalized_skill"
        ]
    ]
    .drop_duplicates()
    .head(50)
    .to_string(index=False)
)

print("\nTop 30 normalized skills:")

top_skills = (
    df["normalized_skill"]
    .value_counts()
    .head(30)
)

print(top_skills.to_string())

print("\nNormalized dataset saved to:")

print(OUTPUT_PATH)

print("\nStep 5 completed successfully.")

print("=" * 70)