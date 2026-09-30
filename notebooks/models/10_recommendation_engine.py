from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_analysis.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "recommendations.csv"
)


# ============================================================
# 2. LOAD SKILL GAP ANALYSIS
# ============================================================

print("Loading skill gap analysis...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. RECOMMENDATION DATABASE
# ============================================================

recommendation_map = {

    # Programming
    "python":
        "Learn Python programming, data structures, functions, OOP and practical problem solving.",

    "java":
        "Learn Java programming, OOP, collections, exception handling and application development.",

    "c++":
        "Learn C++ programming, OOP, STL and problem solving.",

    "c#":
        "Learn C# programming, .NET fundamentals and object-oriented programming.",

    "javascript":
        "Learn JavaScript fundamentals, ES6, DOM manipulation and web development.",


    # Database
    "sql":
        "Learn SQL queries, joins, subqueries, aggregation, views and database design.",

    "dbms":
        "Learn database concepts, normalization, transactions, indexing and SQL.",

    "oracle":
        "Learn Oracle Database, SQL, PL/SQL and database administration fundamentals.",


    # Data
    "data analysis":
        "Learn data cleaning, exploratory data analysis, visualization and statistical analysis.",

    "data analytics":
        "Learn Python, Pandas, NumPy, visualization and statistical techniques for data analytics.",

    "statistics":
        "Learn descriptive statistics, probability, hypothesis testing, correlation and regression.",

    "data modeling":
        "Learn data modeling, ER diagrams, dimensional modeling and database design.",


    # Web
    "html":
        "Learn HTML5, semantic elements, forms and webpage structure.",

    "css":
        "Learn CSS, layouts, Flexbox, Grid, responsive design and styling.",

    "rest api":
        "Learn REST API concepts, HTTP methods, JSON, authentication and API development.",

    "web services":
        "Learn web services, REST, SOAP, HTTP and API integration.",


    # Cloud
    "aws":
        "Learn AWS fundamentals including EC2, S3, IAM, networking and cloud deployment.",

    "microsoft azure":
        "Learn Microsoft Azure fundamentals, virtual machines, storage, networking and cloud services.",

    "google cloud":
        "Learn Google Cloud fundamentals, compute, storage and cloud deployment.",


    # DevOps
    "docker":
        "Learn Docker containers, images, Dockerfiles, networking and container deployment.",

    "kubernetes":
        "Learn Kubernetes architecture, pods, deployments, services and container orchestration.",

    "devops":
        "Learn DevOps principles, CI/CD, version control, automation and cloud deployment.",

    "continuous integration":
        "Learn CI/CD concepts, automated testing, Git workflows and tools such as Jenkins or GitHub Actions.",

    "linux":
        "Learn Linux commands, file systems, permissions, shell scripting and system administration.",

    "automation":
        "Learn automation concepts, scripting, testing automation and workflow automation.",


    # Testing
    "software testing":
        "Learn software testing fundamentals, test cases, defect management and testing methodologies.",

    "automation testing":
        "Learn automated testing frameworks, Selenium and test case development.",

    "selenium":
        "Learn Selenium WebDriver, locators, test automation and browser automation.",


    # Java Framework
    "spring boot":
        "Learn Spring Boot, REST APIs, dependency injection, JPA and backend application development.",


    # SAP
    "sap":
        "Learn SAP fundamentals and explore relevant modules such as SAP MM, SD, FI or HCM.",


    # Management
    "project management":
        "Learn project planning, Agile, Scrum, task management, risk management and project coordination.",

    "management":
        "Develop management, leadership, planning, decision-making and team coordination skills.",

    "team management":
        "Learn team leadership, delegation, communication, conflict resolution and performance management.",


    # Business
    "business development":
        "Learn market analysis, lead generation, sales strategy, customer relationship management and business communication.",

    "marketing":
        "Learn digital marketing, SEO, social media marketing, content strategy and marketing analytics.",

    "market research":
        "Learn market research methods, data collection, customer analysis and market analysis.",

    "lead generation":
        "Learn lead generation strategies, prospecting, CRM tools, digital marketing and sales funnels.",

    "b2b sales":
        "Learn B2B sales strategies, prospecting, negotiation, CRM and relationship management.",

    "sales":
        "Develop sales techniques, customer handling, negotiation, communication and CRM skills.",

    "customer service":
        "Develop customer communication, problem solving, complaint handling and CRM skills.",


    # Communication
    "communication":
        "Improve verbal and written communication, presentation skills and professional communication.",

    "english":
        "Improve professional English, business communication, writing and presentation skills.",


    # HR
    "recruitment":
        "Learn recruitment processes, sourcing, interviewing, candidate screening and HR systems.",

    "hr generalist activities":
        "Learn HR operations, recruitment, onboarding, employee relations and performance management.",


    # Support
    "technical support":
        "Learn troubleshooting, ticket management, system diagnosis, networking and customer support.",

    "troubleshooting":
        "Develop systematic troubleshooting, debugging, root cause analysis and problem-solving skills.",

    "root cause analysis":
        "Learn root cause analysis techniques such as 5 Whys, Fishbone diagrams and systematic problem solving."
}


# ============================================================
# 4. GENERAL RECOMMENDATION
# ============================================================

def get_recommendation(skill):

    skill_lower = skill.strip().lower()

    if skill_lower in recommendation_map:
        return recommendation_map[skill_lower]

    return (
        f"Learn the fundamentals of {skill}, "
        f"practice through projects and gain "
        f"hands-on experience using real-world problems."
    )


# ============================================================
# 5. GENERATE RECOMMENDATIONS
# ============================================================

print("\nGenerating learning recommendations...")

recommendation_results = []


for _, row in df.iterrows():

    job_title = row["job_title"]

    missing_text = row["missing_skills"]

    if pd.isna(missing_text):
        missing_text = ""

    # Convert missing skills into a list
    if str(missing_text).strip():

        missing_skills = [
            skill.strip()
            for skill in str(missing_text).split(",")
            if skill.strip()
        ]

    else:
        missing_skills = []


    # Generate recommendation for every missing skill
    recommendations = []

    for skill in missing_skills:

        recommendation = get_recommendation(skill)

        recommendations.append(
            f"{skill}: {recommendation}"
        )


    # Combine recommendations
    recommendation_text = "\n".join(
        recommendations
    )


    recommendation_results.append(
        {
            "job_title":
                job_title,

            "student_skills":
                row["student_skills"],

            "missing_skills":
                ", ".join(missing_skills),

            "skill_gap_percentage":
                row["skill_gap_percentage"],

            "recommendations":
                recommendation_text
        }
    )


# ============================================================
# 6. CREATE OUTPUT DATAFRAME
# ============================================================

recommendation_df = pd.DataFrame(
    recommendation_results
)


# ============================================================
# 7. SAVE OUTPUT
# ============================================================

recommendation_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("RECOMMENDATION ENGINE RESULTS")
print("========================================")


for i in range(
    min(5, len(recommendation_df))
):

    row = recommendation_df.iloc[i]

    print("\n----------------------------------------")

    print(
        "Target Job:",
        row["job_title"]
    )

    print(
        "\nStudent Skills:"
    )

    print(
        row["student_skills"]
    )

    print(
        "\nMissing Skills:"
    )

    print(
        row["missing_skills"]
    )

    print(
        "\nSkill Gap:"
    )

    print(
        f"{row['skill_gap_percentage']}%"
    )

    print(
        "\nLearning Recommendations:"
    )

    print(
        row["recommendations"]
    )


# ============================================================
# 9. FINAL MESSAGE
# ============================================================

print("\n========================================")
print("RECOMMENDATION ENGINE COMPLETED")
print("========================================")

print("\nOutput file:")

print(OUTPUT_FILE)