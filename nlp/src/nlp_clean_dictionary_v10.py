import pandas as pd
import re
from collections import Counter


# ============================================================
# FILE PATHS
# ============================================================

INPUT_FILE = r"..\..\data\processed\skills.csv"

OUTPUT_CLEAN = (
    r"..\..\data\processed\skills_dictionary_clean_v10.csv"
)

OUTPUT_REJECTED = (
    r"..\..\data\processed\skills_dictionary_rejected_v10.csv"
)


# ============================================================
# LEGITIMATE SHORT / TECHNICAL SKILLS
# ============================================================

ALLOWED_SHORT_SKILLS = {
    "2D",
    "3D",
    "4G",
    "5G",

    "A+",
    "A/P",
    "A/R",

    "API",
    "ATS",
    "AWS",

    "BI",

    "C#",
    "C+",
    "C++",

    "CAD",
    "CAE",
    "CAM",

    "CPU",
    "CRM",
    "CSS",
    "CV",

    "DB2",
    "DNS",

    "EC2",
    "EDA",
    "ELT",
    "ERP",
    "ES6",
    "ETL",

    "F#",

    "GA4",
    "Git",
    "GO",
    "GPU",

    "HCM",
    "HL7",
    "HR",

    "I/O",
    "IAM",
    "IOS",

    "KPI",

    "Mac",

    "n8n",

    "PCB",
    "PHP",
    "PLC",

    "QA",

    "R&D",
    "RAM",
    "RF",
    "ROI",

    "SAP",
    "SAS",
    "SDK",
    "SEM",
    "SEO",
    "SQL",

    "SSH",
    "SSL",

    "TCP",
    "UDP",

    "UI",
    "UX",

    "VBA",
    "VM",
    "VPN",

    "X++",
    "XML"
}


# ============================================================
# PROTECTED TECHNICAL SKILLS
# These are ALWAYS allowed.
# ============================================================

PROTECTED_SKILLS = {

    # Programming / development
    "python",
    "sql",
    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "c",
    "c++",
    "c#",
    "php",
    "ruby",
    "go",
    "rust",
    "scala",
    "kotlin",
    "swift",

    # Cloud
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "google cloud platform",
    "cloud",
    "cloud computing",

    # AI / ML / NLP
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "artificial intelligence",
    "computer vision",

    # Web
    "react",
    "angular",
    "node.js",
    "node js",
    "vue",
    "vue.js",
    "next.js",
    "express.js",

    # Data
    "data",
    "data analysis",
    "data analytics",
    "data science",
    "data engineering",

    # Databases
    "database",
    "databases",
    "mysql",
    "postgresql",
    "oracle",
    "sql server",
    "mongodb",
    "redis",

    # DevOps
    "docker",
    "kubernetes",
    "devops",
    "jenkins",
    "ansible",
    "terraform",

    # Version control
    "git",
    "github",
    "gitlab",

    # Data tools
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "opencv",

    # Big data
    "spark",
    "apache spark",
    "hadoop",
    "kafka",
    "airflow",

    # Business / productivity
    "excel",
    "power bi",
    "tableau",
    "powerpoint",
    "word",

    # Enterprise
    "sap",
    "crm",
    "erp",
    "salesforce",
    "servicenow",
    "jira",
    "confluence",

    # Security / networking
    "cyber security",
    "cybersecurity",
    "network security",
    "information security",
    "linux",
    "windows",
    "unix",

    # APIs
    "api",
    "rest api",
    "restful api",
    "graphql",

    # Design / engineering software
    "figma",
    "photoshop",
    "illustrator",
    "autocad",
    "solidworks",
    "catia",

    # Testing
    "selenium",
    "automation",
    "testing",

    # Legitimate domain-specific terms
    "21 cfr",
    "21 cfr part 11",
    "11kv substation",
    "24/7",
    "24x7",
    "24.7 ai",
}


# ============================================================
# GENERIC / NON-SKILL TERMS
# ============================================================

GENERIC_TERMS = {

    "manager",
    "management",
    "senior",
    "junior",
    "lead",
    "leader",
    "executive",

    "engineer",
    "engineering",

    "developer",
    "development",

    "designer",
    "design",

    "architect",
    "architecture",

    "analyst",
    "associate",
    "consultant",
    "specialist",
    "professional",
    "officer",
    "director",
    "intern",
    "trainee",

    "process",
    "processes",
    "procedure",
    "procedures",

    "system",
    "systems",

    "tools",
    "tool",

    "office",

    "operations",
    "operation",

    "project",
    "projects",

    "product",
    "products",

    "company",
    "business",

    "organization",
    "organizations",

    "environment",

    "time",
    "shift",

    "performance",
    "quality",

    "compliance",

    "maintain",
    "maintenance",
    "manage",

    "handling",

    "support",

    "service",
    "services",

    "delivery",

    "build",
    "building",

    "make",
    "making",

    "work",
    "working",

    "job",
    "jobs",

    "strong",
    "high",
    "excellent",
    "good",
    "best",

    "complex",

    "direct",
    "prior",

    "experienced",
    "experience",

    "expertise",
    "knowledge",

    "skills",
    "skill",

    "ability",

    "responsibility",
    "responsibilities",

    "marketing",

    "sales",
    "selling",

    "customer",
    "customers",

    "client",
    "clients",

    "stakeholder",
    "stakeholders",

    "relationship",
    "relationships",

    "communication",

    "written",
    "verbal",

    "international",

    "career",
    "salary",
    "benefits",

    "hiring",
    "recruitment",

    "year",
    "years",

    "join",
    "joining",

    "target",
    "targets",

    "area",
    "field",

    "site",
    "home",

    "post",

    "account",
    "record",
    "records",

    "plan",
    "plans",

    "generation",

    "advantage",
    "concepts",
    "life",
    "power",
    "control",

    "improvement",
    "collaboration",
    "coordination",
}


# ============================================================
# EDUCATION / QUALIFICATION TERMS
# ============================================================

EDUCATION_TERMS = {

    "10th",
    "10th pass",

    "11th",
    "11th pass",

    "12th",
    "12th pass",

    "12 class",
    "12th class",

    "any degree",
    "any graduate",
    "any graduation",

    "degree",
    "diploma",
    "diploma holder",

    "iti",

    "graduate",
    "graduation",

    "post graduate",
    "postgraduate",

    "under graduate",
    "undergraduate",

    "bachelor",
    "bachelors",

    "master",
    "masters",

    "phd",
    "doctorate",
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(text):

    return re.sub(
        r"\s+",
        " ",
        str(text).strip()
    ).lower()


# ============================================================
# SHORT SKILL CHECK
# ============================================================

def is_allowed_short_skill(skill):

    normalized = normalize_skill(skill)

    return any(
        normalized == normalize_skill(x)
        for x in ALLOWED_SHORT_SKILLS
    )


def is_invalid_short_skill(skill):

    if is_allowed_short_skill(skill):
        return False

    compact = re.sub(
        r"\s+",
        "",
        skill
    )

    # One-character terms
    if len(compact) <= 1:
        return True

    # Two / three alphabetic characters
    if len(compact) <= 3 and compact.isalpha():
        return True

    # Very short numeric codes
    if (
        len(compact) <= 3
        and any(ch.isdigit() for ch in compact)
    ):
        return True

    return False


# ============================================================
# NUMERIC / PERSONAL INFORMATION NOISE
# ============================================================

def is_numeric_or_personal_info(skill):

    text = skill.strip().lower()

    # Pure number
    if re.fullmatch(
        r"\d+(?:\.\d+)?",
        text
    ):
        return True

    # Age
    if re.search(
        r"\b\d+\+?\s*age\b",
        text
    ):
        return True

    # Salary
    if re.search(
        r"\b\d+(?:\.\d+)?\s*lpa\b",
        text
    ):
        return True

    # Pass-out year
    if re.search(
        r"\b20\d{2}\s+pass\s*out\b",
        text
    ):
        return True

    # Numeric ranges
    if re.fullmatch(
        r"\d+\s*(?:to|-)\s*\d+.*",
        text
    ):
        return True

    # Numeric-heavy codes
    digits = sum(
        ch.isdigit()
        for ch in text
    )

    letters = sum(
        ch.isalpha()
        for ch in text
    )

    if (
        digits >= 4
        and digits > letters
    ):
        return True

    return False


# ============================================================
# EDUCATION CHECK
# ============================================================

def is_education_term(skill):

    normalized = normalize_skill(skill)

    if normalized in EDUCATION_TERMS:
        return True

    if re.search(
        r"\b(?:10th|11th|12th|degree|diploma|"
        r"iti|graduate|graduation|postgraduate|"
        r"post graduate|bachelor|master|phd)\b",
        normalized
    ):
        return True

    return False


# ============================================================
# EXPERIENCE / DESCRIPTION CHECK
# ============================================================

def is_description_phrase(skill):

    text = skill.strip()

    patterns = [

        r"\b\d+\s*(?:to|-)\s*\d+\s*years?\b",

        r"\b\d+\+?\s*years?\b",

        r"\b\d+\+?\s*yrs?\b",

        r"\byears?\s+of\s+experience\b",

        r"\byrs?\s+of\s+experience\b",

        r"\bexperience\s+in\b",

        r"\bexperience\s+with\b",

        r"\bknowledge\s+of\b",

        r"\bknowledge\s+in\b",

        r"\bmust\s+have\b",

        r"\bshould\s+have\b",

        r"\bresponsible\s+for\b",

        r"\blooking\s+for\b",

        r"\bability\s+to\b",

        r"\bproficient\s+in\b",

        r"\bpreferred\b",

        r"\brequired\b",
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return True

    return False


# ============================================================
# JOB ROLE / LIST FRAGMENT CHECK
# ============================================================

def is_role_or_list_fragment(skill):

    text = skill.strip()

    normalized = normalize_skill(text)

    # Numbered list entries
    if re.match(
        r"^\s*\d+[\.\)]\s+",
        text
    ):
        return True

    # First-line / first-party phrases
    if re.search(
        r"\b1st\s+(?:line|party)\b",
        normalized
    ):
        return True

    # Number + recruitment / sales
    if re.search(
        r"\b\d+\s+.*\b(recruitment|sales)\b",
        normalized
    ):
        return True

    # End-to-end implementation
    if re.search(
        r"\bend[- ]to[- ]end\b",
        normalized
    ):
        return True

    # Implementation phrase
    if re.search(
        r"\bimplementation[s]?\b",
        normalized
    ):
        return True

    # "2 Way Matching"
    if re.search(
        r"\b\d+\s+way\s+matching\b",
        normalized
    ):
        return True

    # Wheeler / vehicle sales
    if re.search(
        r"\bwheeler\b",
        normalized
    ):
        return True

    return False


# ============================================================
# SENTENCE CHECK
# ============================================================

def looks_like_sentence(text):

    words = text.split()

    # Very long phrase
    if len(words) >= 12:
        return True

    # Medium sentence-like phrase
    if (
        len(words) >= 8
        and any(
            word.lower() in {
                "and",
                "or",
                "with",
                "for",
                "the",
                "of",
                "to",
                "in",
                "on",
                "at",
                "from",
                "required",
                "preferred",
                "responsible",
            }
            for word in words
        )
    ):
        return True

    return False


# ============================================================
# SPECIAL CHARACTER NOISE
# ============================================================

def is_special_character_noise(skill):

    if not skill.strip():
        return True

    if re.fullmatch(
        r"[\W_]+",
        skill.strip()
    ):
        return True

    return False


# ============================================================
# GENERIC CHECK
# ============================================================

def is_generic_term(skill):

    normalized = normalize_skill(skill)

    # Protected technical skills are never generic
    if normalized in PROTECTED_SKILLS:
        return False

    normalized_generic_terms = {
        normalize_skill(x)
        for x in GENERIC_TERMS
    }

    return normalized in normalized_generic_terms


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("NLP SKILL DICTIONARY CLEANING - V10")
print("=" * 70)


# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

df = pd.read_csv(
    INPUT_FILE
)

df["skill_name"] = (
    df["skill_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)


accepted = []
rejected = []

seen_normalized = set()


# ------------------------------------------------------------
# PROCESS
# ------------------------------------------------------------

for _, row in df.iterrows():

    skill_id = int(
        row["skill_id"]
    )

    skill = row["skill_name"].strip()

    # Empty
    if not skill:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "empty_skill"
        })

        continue


    normalized = normalize_skill(skill)


    # Duplicate
    if normalized in seen_normalized:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "duplicate_normalized_skill"
        })

        continue


    seen_normalized.add(normalized)


    # --------------------------------------------------------
    # PROTECTED TECHNICAL SKILL
    # --------------------------------------------------------

    if normalized in PROTECTED_SKILLS:

        accepted.append({
            "skill_id": skill_id,
            "skill_name": skill
        })

        continue


    # --------------------------------------------------------
    # SPECIAL CHARACTER NOISE
    # --------------------------------------------------------

    if is_special_character_noise(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "special_character_noise"
        })

        continue


    # --------------------------------------------------------
    # SHORT NOISE
    # --------------------------------------------------------

    if is_invalid_short_skill(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "invalid_short_skill"
        })

        continue


    # --------------------------------------------------------
    # NUMERIC / PERSONAL INFORMATION
    # --------------------------------------------------------

    if is_numeric_or_personal_info(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "numeric_or_personal_information"
        })

        continue


    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    if is_education_term(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "education_or_qualification"
        })

        continue


    # --------------------------------------------------------
    # ROLE / LIST FRAGMENT
    # --------------------------------------------------------

    if is_role_or_list_fragment(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "job_role_or_list_fragment"
        })

        continue


    # --------------------------------------------------------
    # GENERIC
    # --------------------------------------------------------

    if is_generic_term(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "generic"
        })

        continue


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    if is_description_phrase(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "experience_or_description_phrase"
        })

        continue


    # --------------------------------------------------------
    # HASHTAG / NON-SKILL
    # --------------------------------------------------------

    if skill.startswith("#"):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "non_skill_phrase"
        })

        continue


    # --------------------------------------------------------
    # SENTENCE
    # --------------------------------------------------------

    if looks_like_sentence(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "sentence_or_description"
        })

        continue


    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    accepted.append({
        "skill_id": skill_id,
        "skill_name": skill
    })


# ============================================================
# SAVE OUTPUT
# ============================================================

clean_df = pd.DataFrame(
    accepted
)

rejected_df = pd.DataFrame(
    rejected
)


clean_df.to_csv(
    OUTPUT_CLEAN,
    index=False,
    encoding="utf-8"
)

rejected_df.to_csv(
    OUTPUT_REJECTED,
    index=False,
    encoding="utf-8"
)


# ============================================================
# REPORT
# ============================================================

print()
print("=" * 70)
print("V10 CLEANING COMPLETED")
print("=" * 70)

print(
    f"Original skills : {len(df):,}"
)

print(
    f"Accepted skills : {len(clean_df):,}"
)

print(
    f"Rejected skills : {len(rejected_df):,}"
)


# ============================================================
# REJECTION REASONS
# ============================================================

print()
print("REJECTION REASONS:")

reason_counts = Counter(
    rejected_df["reason"]
)

for reason, count in reason_counts.most_common():

    print(
        f"  {reason}: {count:,}"
    )


# ============================================================
# TECHNICAL DICTIONARY CHECK
# ============================================================

print()
print("=" * 70)
print("TECHNICAL DICTIONARY CHECK")
print("=" * 70)


clean_normalized = {
    normalize_skill(x)
    for x in clean_df["skill_name"]
}


technical_check = [

    "Python",
    "SQL",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",

    "AWS",
    "Azure",

    "Docker",
    "Kubernetes",

    "Machine Learning",
    "Deep Learning",
    "NLP",

    "React",
    "Angular",
    "Node.js",

    "Power BI",
    "Tableau",
    "Excel",

    "Git",
]


for skill in technical_check:

    if normalize_skill(skill) in clean_normalized:

        print(
            f"{skill}: PRESENT"
        )

    else:

        print(
            f"{skill}: NOT IN CLEAN DICTIONARY"
        )


# ============================================================
# KNOWN NOISE CHECK
# ============================================================

print()
print("=" * 70)
print("KNOWN NOISE CHECK")
print("=" * 70)


known_noise = [

    "0-30 bucket",
    "000 to 25",
    "10.0",
    "1040",
    "1065",

    "1099 Recruitment",

    "10th Pass",
    "12th Pass",

    "12TH / ITI / DIPLOMA / ANY DEGREE",

    "1st LINE MANAGER",
    "1st Party Collection",

    "2 End-to-End Implementations",
    "2 HFM implementations",
    "2 Way Matching",

    "2 Wheeler Sales",
    "2 wheeler part sales",
    "2-wheeler",
    "2/4 Wheeler",

    "2025 Pass Out",
    "25 LPA",
    "27+ age",
]


clean_lookup = {
    normalize_skill(x)
    for x in clean_df["skill_name"]
}


for skill in known_noise:

    if normalize_skill(skill) in clean_lookup:

        print(
            f"STILL PRESENT: {skill}"
        )

    else:

        print(
            f"REMOVED: {skill}"
        )


# ============================================================
# SHORT SKILLS
# ============================================================

print()
print("=" * 70)
print("SHORT SKILLS <=3 CHARACTERS")
print("=" * 70)


short_skills = []


for skill in clean_df["skill_name"]:

    compact = re.sub(
        r"\s+",
        "",
        skill
    )

    if len(compact) <= 3:

        short_skills.append(skill)


print(
    f"Count: {len(short_skills)}"
)


for skill in sorted(
    short_skills,
    key=lambda x: x.lower()
):

    print(skill)


# ============================================================
# OUTPUT PATHS
# ============================================================

print()
print(
    "Clean dictionary saved to:"
)

print(
    OUTPUT_CLEAN
)

print()
print(
    "Rejected dictionary saved to:"
)

print(
    OUTPUT_REJECTED
)

print()
print(
    "PostgreSQL data was NOT modified."
)

print("=" * 70)