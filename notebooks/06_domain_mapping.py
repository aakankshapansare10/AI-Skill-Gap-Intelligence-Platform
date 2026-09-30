import pandas as pd
import re

INPUT_PATH = "data/processed/cleaned_job_postings.csv"
OUTPUT_PATH = "data/processed/job_domains.csv"

df = pd.read_csv("C:/Users/ANTARA/Downloads/indian_job_market_2025.csv")

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 6 - JOB DOMAIN MAPPING")
print("=" * 70)

print(f"Total job postings: {len(df):,}")

# --------------------------------------------------
# DOMAIN KEYWORDS
# --------------------------------------------------

domain_keywords = {

    "Data Science": [
        "data scientist",
        "data science",
        "data analyst",
        "data analytics",
        "machine learning",
        "ml engineer",
        "ai engineer",
        "artificial intelligence",
        "deep learning",
        "nlp engineer",
        "data engineer",
        "business intelligence",
        "bi analyst"
    ],

    "Software Development": [
        "software engineer",
        "software developer",
        "application developer",
        "web developer",
        "backend developer",
        "back end developer",
        "frontend developer",
        "front end developer",
        "full stack developer",
        "fullstack developer",
        "python developer",
        "java developer",
        "javascript developer",
        "php developer",
        "dot net developer",
        ".net developer",
        "mobile developer",
        "android developer",
        "ios developer",
        "react developer",
        "node developer"
    ],

    "IT & Infrastructure": [
        "system administrator",
        "systems administrator",
        "network administrator",
        "network engineer",
        "cloud engineer",
        "cloud administrator",
        "devops engineer",
        "devops",
        "site reliability engineer",
        "sre",
        "technical support",
        "it support",
        "it administrator",
        "cyber security",
        "cybersecurity",
        "security engineer",
        "information security"
    ],

    "Finance & Accounting": [
        "accountant",
        "accounting",
        "financial analyst",
        "finance analyst",
        "finance manager",
        "financial manager",
        "investment analyst",
        "investment banking",
        "auditor",
        "audit",
        "tax analyst",
        "taxation",
        "chartered accountant",
        "ca",
        "accounts executive",
        "accounts manager"
    ],

    "Sales": [
        "sales executive",
        "sales manager",
        "sales representative",
        "sales associate",
        "business development executive",
        "business development manager",
        "business development",
        "account executive",
        "territory sales",
        "relationship manager",
        "sales consultant"
    ],

    "Marketing": [
        "marketing executive",
        "marketing manager",
        "digital marketing",
        "marketing specialist",
        "seo",
        "sem",
        "social media",
        "content marketing",
        "brand manager",
        "marketing analyst",
        "growth marketing",
        "performance marketing"
    ],

    "Human Resources": [
        "human resources",
        "hr executive",
        "hr manager",
        "hr specialist",
        "hr recruiter",
        "recruiter",
        "recruitment",
        "talent acquisition",
        "talent management",
        "people operations",
        "payroll"
    ],

    "Healthcare": [
        "doctor",
        "physician",
        "nurse",
        "nursing",
        "medical",
        "healthcare",
        "hospital",
        "pharmacist",
        "pharmacy",
        "clinical",
        "medical officer",
        "lab technician",
        "radiologist",
        "dentist"
    ],

    "Engineering": [
        "mechanical engineer",
        "mechanical engineering",
        "civil engineer",
        "civil engineering",
        "electrical engineer",
        "electrical engineering",
        "electronics engineer",
        "electronics engineering",
        "chemical engineer",
        "chemical engineering",
        "industrial engineer",
        "automotive engineer",
        "production engineer",
        "manufacturing engineer"
    ],

    "Product Management": [
        "product manager",
        "product management",
        "product owner",
        "associate product manager",
        "product analyst",
        "product specialist"
    ],

    "Operations": [
        "operations manager",
        "operations executive",
        "operations analyst",
        "operations associate",
        "business operations",
        "supply chain",
        "logistics",
        "warehouse",
        "procurement",
        "operations specialist"
    ],

    "Design": [
        "graphic designer",
        "ui designer",
        "ux designer",
        "ui ux designer",
        "product designer",
        "visual designer",
        "web designer",
        "creative designer",
        "motion designer",
        "fashion designer"
    ],

    "Customer Service": [
        "customer service",
        "customer support",
        "customer care",
        "call center",
        "call centre",
        "technical support executive",
        "support executive",
        "customer success"
    ],

    "Education": [
        "teacher",
        "teaching",
        "lecturer",
        "professor",
        "trainer",
        "tutor",
        "education",
        "academic",
        "faculty"
    ]
}


# --------------------------------------------------
# DOMAIN CLASSIFICATION FUNCTION
# --------------------------------------------------

def classify_domain(title):

    if pd.isna(title):
        return "Other"

    title = str(title).lower().strip()

    title = re.sub(r"\s+", " ", title)

    matched_domains = []

    for domain, keywords in domain_keywords.items():

        for keyword in keywords:

            if keyword in title:
                matched_domains.append(domain)
                break

    if len(matched_domains) == 0:
        return "Other"

    # Priority for cases where a title matches
    # more than one domain

    priority = [
        "Data Science",
        "Software Development",
        "IT & Infrastructure",
        "Finance & Accounting",
        "Human Resources",
        "Healthcare",
        "Engineering",
        "Product Management",
        "Marketing",
        "Sales",
        "Operations",
        "Design",
        "Customer Service",
        "Education"
    ]

    for domain in priority:

        if domain in matched_domains:
            return domain

    return matched_domains[0]


# --------------------------------------------------
# APPLY DOMAIN CLASSIFICATION
# --------------------------------------------------

df["domain"] = df["title"].apply(
    classify_domain
)


# --------------------------------------------------
# CREATE OUTPUT DATASET
# --------------------------------------------------

domain_data = df[
    [
        "jobId",
        "title",
        "domain"
    ]
].copy()

domain_data = domain_data.drop_duplicates(
    subset=["jobId"]
)

domain_data = domain_data.reset_index(
    drop=True
)


# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

domain_data.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("DOMAIN MAPPING RESULTS")
print("=" * 70)

print(
    f"Jobs classified: "
    f"{len(domain_data):,}"
)

print(
    f"Unique domains: "
    f"{domain_data['domain'].nunique():,}"
)

print("\nJobs per domain:")

domain_counts = (
    domain_data["domain"]
    .value_counts()
)

print(
    domain_counts.to_string()
)


print("\n" + "=" * 70)
print("SAMPLE DOMAIN CLASSIFICATIONS")
print("=" * 70)

print(
    domain_data
    .head(50)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print("OTHER / UNCLASSIFIED JOBS")
print("=" * 70)

other_jobs = domain_data[
    domain_data["domain"] == "Other"
]

print(
    f"Other jobs: "
    f"{len(other_jobs):,}"
)

print("\nSample Other jobs:")

print(
    other_jobs
    .head(30)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print("STEP 6 COMPLETED")
print("=" * 70)

print("Domain mapping saved to:")
print(OUTPUT_PATH)