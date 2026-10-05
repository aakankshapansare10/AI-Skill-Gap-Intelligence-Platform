import pandas as pd
import re
from collections import Counter

INPUT_FILE = r"..\..\data\processed\skills.csv"

OUTPUT_CLEAN = r"..\..\data\processed\skills_dictionary_clean_v9.csv"
OUTPUT_REJECTED = r"..\..\data\processed\skills_dictionary_rejected_v9.csv"


# ============================================================
# LEGITIMATE SHORT / TECHNICAL SKILLS
# ============================================================

ALLOWED_SHORT_SKILLS = {
    "2D", "3D", "4G", "5G",
    "A+", "A/P", "A/R",
    "API", "ATS", "AWS",
    "BI",
    "C#", "C+", "C++",
    "CAD", "CAE", "CAM",
    "CPU", "CRM", "CSS", "CV",
    "DB2", "DNS",
    "EC2", "EDA", "ELT", "ERP", "ES6", "ETL",
    "F#",
    "GA4", "GPU",
    "HCM", "HL7", "HR",
    "I/O", "IAM", "IOS",
    "KPI",
    "Mac",
    "n8n",
    "PCB", "PHP", "PLC",
    "QA",
    "R&D", "RAM", "RF", "ROI",
    "SAP", "SAS", "SDK", "SEM", "SEO", "SQL",
    "SSH", "SSL",
    "TCP", "UDP",
    "UI", "UX",
    "VBA", "VM", "VPN",
    "X++", "XML"
}


# ============================================================
# IMPORTANT TECHNICAL SKILLS
# ============================================================

PROTECTED_SKILLS = {
    "python",
    "sql",
    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "react",
    "angular",
    "node.js",
    "power bi",
    "tableau",
    "excel",
    "git",
    "github",
    "gitlab",
    "data",
    "data analysis",
    "data analytics",
    "data science",
    "automation",
    "testing",
    "software development",
    "web development",
    "cyber security",
    "cybersecurity",
    "network security",
    "information security",
    "cloud",
    "cloud computing",
    "devops",
    "database",
    "databases",
    "api",
    "rest api",
    "restful api",
    "graphql",
    "linux",
    "windows",
    "unix",
    "powerpoint",
    "word",
    "mongodb",
    "mysql",
    "postgresql",
    "oracle",
    "sql server",
    "sap",
    "crm",
    "erp",
    "tensorflow",
    "pytorch",
    "opencv",
    "scikit-learn",
    "pandas",
    "numpy",
    "spark",
    "hadoop",
    "airflow",
    "kafka",
    "gcp",
    "google cloud",
    "firebase",
    "figma",
    "photoshop",
    "illustrator",
    "autocad",
    "solidworks",
    "catia",
    "salesforce",
    "servicenow",
    "jira",
    "confluence",
    "selenium",
    "jenkins",
    "ansible",
    "terraform",
    "kotlin",
    "swift",
    "php",
    "ruby",
    "go",
    "rust",
    "scala",
    "c",
    "c++",
    "c#",
}


# ============================================================
# GENERIC / ROLE WORDS
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
# EXPERIENCE / JOB-DESCRIPTION PATTERNS
# ============================================================

PHRASE_PATTERNS = [
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


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(text):
    return re.sub(r"\s+", " ", str(text).strip()).lower()


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

    compact = re.sub(r"\s+", "", skill)

    if len(compact) <= 1:
        return True

    if len(compact) <= 3 and compact.isalpha():
        return True

    if len(compact) <= 3 and any(ch.isdigit() for ch in compact):
        return True

    return False


# ============================================================
# NUMERIC / CODE-LIKE NOISE
# ============================================================

def is_numeric_noise(skill):

    text = skill.strip()

    # Pure numbers
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return True

    # Mostly numeric codes such as 1040, 1065, 14001
    digits = sum(ch.isdigit() for ch in text)
    letters = sum(ch.isalpha() for ch in text)

    if digits >= 4 and digits > letters:
        return True

    # Values such as 000 to 25, 0-30 bucket
    if re.fullmatch(r"\d+\s*(?:to|-)\s*\d+.*", text, re.IGNORECASE):
        return True

    return False


# ============================================================
# EDUCATION CHECK
# ============================================================

def is_education_term(skill):

    normalized = normalize_skill(skill)

    if normalized in EDUCATION_TERMS:
        return True

    # Any phrase containing common qualification words
    if re.search(
        r"\b(?:10th|11th|12th|degree|diploma|iti|graduate|graduation|"
        r"postgraduate|post graduate|bachelor|master|phd)\b",
        normalized
    ):
        return True

    return False


# ============================================================
# SENTENCE CHECK
# ============================================================

def looks_like_sentence(text):

    words = text.split()

    if len(words) >= 12:
        return True

    if len(words) >= 8 and any(
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
    ):
        return True

    return False


# ============================================================
# SPECIAL CHARACTER NOISE
# ============================================================

def is_special_character_noise(skill):

    if not skill.strip():
        return True

    if re.fullmatch(r"[\W_]+", skill.strip()):
        return True

    return False


# ============================================================
# GENERIC TERM CHECK
# ============================================================

def is_generic_term(skill):

    normalized = normalize_skill(skill)

    if normalized in PROTECTED_SKILLS:
        return False

    return normalized in {
        normalize_skill(x)
        for x in GENERIC_TERMS
    }


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("NLP SKILL DICTIONARY CLEANING - V9")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["skill_name"] = (
    df["skill_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

accepted = []
rejected = []

seen_normalized = set()

for _, row in df.iterrows():

    skill_id = int(row["skill_id"])
    skill = row["skill_name"].strip()

    if not skill:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "empty_skill"
        })

        continue

    normalized = normalize_skill(skill)

    # --------------------------------------------------------
    # DUPLICATE
    # --------------------------------------------------------

    if normalized in seen_normalized:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "duplicate_normalized_skill"
        })

        continue

    seen_normalized.add(normalized)

    # --------------------------------------------------------
    # PROTECTED TECHNICAL SKILLS
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
    # SHORT SKILLS
    # --------------------------------------------------------

    if is_invalid_short_skill(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "invalid_short_skill"
        })

        continue

    # --------------------------------------------------------
    # NUMERIC NOISE
    # --------------------------------------------------------

    if is_numeric_noise(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "numeric_or_code_noise"
        })

        continue

    # --------------------------------------------------------
    # EDUCATION / QUALIFICATION
    # --------------------------------------------------------

    if is_education_term(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "education_or_qualification"
        })

        continue

    # --------------------------------------------------------
    # GENERIC TERMS
    # --------------------------------------------------------

    if is_generic_term(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "generic"
        })

        continue

    # --------------------------------------------------------
    # EXPERIENCE / DESCRIPTION PHRASES
    # --------------------------------------------------------

    matched_phrase = False

    for pattern in PHRASE_PATTERNS:

        if re.search(
            pattern,
            skill,
            flags=re.IGNORECASE
        ):
            matched_phrase = True
            break

    if matched_phrase:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "experience_or_description_phrase"
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
    # HASHTAGS
    # --------------------------------------------------------

    if skill.startswith("#"):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "non_skill_phrase"
        })

        continue

    # --------------------------------------------------------
    # NUMBERED LIST ITEMS
    # --------------------------------------------------------

    if re.match(r"^\s*\d+[\.\)]\s+", skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "non_skill_phrase"
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
# SAVE
# ============================================================

clean_df = pd.DataFrame(accepted)
rejected_df = pd.DataFrame(rejected)

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
print("V9 CLEANING COMPLETED")
print("=" * 70)

print(f"Original skills : {len(df):,}")
print(f"Accepted skills : {len(clean_df):,}")
print(f"Rejected skills : {len(rejected_df):,}")

print()
print("REJECTION REASONS:")

reason_counts = Counter(rejected_df["reason"])

for reason, count in reason_counts.most_common():

    print(f"  {reason}: {count:,}")


# ============================================================
# TECHNICAL CHECK
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
        print(f"{skill}: PRESENT")
    else:
        print(f"{skill}: NOT IN CLEAN DICTIONARY")


# ============================================================
# GENERIC CHECK
# ============================================================

print()
print("=" * 70)
print("GENERIC TERM CHECK")
print("=" * 70)

remaining_generic = []

generic_normalized = {
    normalize_skill(x)
    for x in GENERIC_TERMS
}

for skill in clean_df["skill_name"]:

    normalized = normalize_skill(skill)

    if (
        normalized in generic_normalized
        and normalized not in PROTECTED_SKILLS
    ):
        remaining_generic.append(skill)

if remaining_generic:

    for skill in sorted(set(remaining_generic)):
        print(skill)

else:

    print("No explicitly blocked generic terms remain.")


# ============================================================
# SHORT SKILLS
# ============================================================

print()
print("=" * 70)
print("SHORT SKILLS <=3 CHARACTERS")
print("=" * 70)

short_skills = []

for skill in clean_df["skill_name"]:

    compact = re.sub(r"\s+", "", skill)

    if len(compact) <= 3:
        short_skills.append(skill)

print(f"Count: {len(short_skills)}")

for skill in sorted(
    short_skills,
    key=lambda x: x.lower()
):
    print(skill)


# ============================================================
# CHECK KNOWN BAD EXAMPLES
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
    "1040s",
    "1065",
    "1099 Recruitment",
    "10th",
    "10th Pass",
    "11th",
    "12 class",
    "12th",
    "12th Pass",
    "12TH / ITI / DIPLOMA / ANY DEGREE",
    "1st LINE MANAGER",
    "1st Party Collection",
    "2 End-to-End Implementations",
]

clean_lookup = {
    normalize_skill(x)
    for x in clean_df["skill_name"]
}

for skill in known_noise:

    if normalize_skill(skill) in clean_lookup:
        print(f"STILL PRESENT: {skill}")
    else:
        print(f"REMOVED: {skill}")


# ============================================================
# SAMPLE
# ============================================================

print()
print("=" * 70)
print("SAMPLE ACCEPTED SKILLS")
print("=" * 70)

for skill in clean_df["skill_name"].head(30):

    print(skill)


print()
print("Clean dictionary saved to:")
print(OUTPUT_CLEAN)

print()
print("Rejected dictionary saved to:")
print(OUTPUT_REJECTED)

print()
print("PostgreSQL data was NOT modified.")

print("=" * 70)