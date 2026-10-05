import pandas as pd
import re
from collections import Counter

# ============================================================
# NLP SKILL DICTIONARY CLEANING - V8
# ============================================================

INPUT_FILE = r"..\..\data\processed\skills.csv"

OUTPUT_CLEAN = r"..\..\data\processed\skills_dictionary_clean_v8.csv"
OUTPUT_REJECTED = r"..\..\data\processed\skills_dictionary_rejected_v8.csv"


# ============================================================
# IMPORTANT LEGITIMATE SHORT / TECHNICAL SKILLS
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
    "PCB", "PHP", "PLC",
    "QA",
    "R&D", "RAM", "RF", "ROI",
    "SAP", "SAS", "SDK", "SEM", "SEO", "SQL",
    "SSH", "SSL",
    "TCP", "UDP",
    "UI", "UX",
    "VBA", "VM", "VPN",
    "X++", "XML",
    "n8n"
}


# ============================================================
# TECHNICAL / DOMAIN SKILLS THAT SHOULD NOT BE REMOVED
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
    "git",
    "github",
    "gitlab",
    "linux",
    "windows",
    "unix",
    "excel",
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
    "azure",
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
# GENERIC / ROLE / NON-SKILL TERMS
# ============================================================

GENERIC_TERMS = {
    # roles / seniority
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

    # generic work words
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

    # generic adjectives / verbs
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

    # generic business language
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
    "company",
    "career",
    "salary",
    "benefits",
    "hiring",
    "recruitment",

    # generic words frequently appearing as false skills
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
    "organization",
}


# ============================================================
# NON-SKILL PHRASE INDICATORS
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
    r"\bshould\s+be\b",
    r"\bresponsible\s+for\b",
    r"\blooking\s+for\b",
    r"\bability\s+to\b",
    r"\bproficient\s+in\b",
    r"\bexcellent\s+communication\b",
    r"\bgood\s+communication\b",
    r"\bstrong\s+communication\b",
]


# ============================================================
# SENTENCE DETECTION
# ============================================================

def looks_like_sentence(text):
    words = text.split()

    if len(words) >= 12:
        return True

    if len(words) >= 8 and any(
        word.lower() in {
            "and", "or", "with", "for", "the", "of",
            "to", "in", "on", "at", "from", "required",
            "preferred", "responsible"
        }
        for word in words
    ):
        return True

    return False


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(text):
    text = str(text).strip()

    text = re.sub(r"\s+", " ", text)

    return text.lower()


# ============================================================
# SHORT SKILL CHECK
# ============================================================

def is_allowed_short_skill(skill):
    normalized = normalize_skill(skill)

    for allowed in ALLOWED_SHORT_SKILLS:
        if normalized == normalize_skill(allowed):
            return True

    return False


def is_invalid_short_skill(skill):
    normalized = normalize_skill(skill)
    compact = re.sub(r"\s+", "", skill)

    if is_allowed_short_skill(skill):
        return False

    # Single character
    if len(compact) <= 1:
        return True

    # Very short alphabetic word
    if len(compact) <= 3 and compact.isalpha():
        return True

    # Short strings containing digits
    if len(compact) <= 3 and any(ch.isdigit() for ch in compact):
        return True

    return False


# ============================================================
# SPECIAL CHARACTER NOISE
# ============================================================

def is_special_character_noise(skill):
    compact = skill.strip()

    if not compact:
        return True

    if re.fullmatch(r"[\W_]+", compact):
        return True

    return False


# ============================================================
# GENERIC TERM CHECK
# ============================================================

def is_generic_term(skill):
    normalized = normalize_skill(skill)

    if normalized in PROTECTED_SKILLS:
        return False

    if normalized in {normalize_skill(x) for x in GENERIC_TERMS}:
        return True

    return False


# ============================================================
# MAIN CLEANING
# ============================================================

print("=" * 70)
print("NLP SKILL DICTIONARY CLEANING - V8")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["skill_name"] = df["skill_name"].fillna("").astype(str).str.strip()

records = []
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
    # Duplicate normalized skills
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
    # Special character noise
    # --------------------------------------------------------

    if is_special_character_noise(skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "special_character_noise"
        })
        continue

    # --------------------------------------------------------
    # Short skills
    # --------------------------------------------------------

    if is_invalid_short_skill(skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "invalid_short_skill"
        })
        continue

    # --------------------------------------------------------
    # Protected technical skills ALWAYS survive
    # --------------------------------------------------------

    if normalized in PROTECTED_SKILLS:
        accepted.append({
            "skill_id": skill_id,
            "skill_name": skill
        })
        continue

    # --------------------------------------------------------
    # Generic terms
    # --------------------------------------------------------

    if is_generic_term(skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "generic"
        })
        continue

    # --------------------------------------------------------
    # Sentence / description
    # --------------------------------------------------------

    if looks_like_sentence(skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "sentence_or_description"
        })
        continue

    # --------------------------------------------------------
    # Phrase patterns
    # --------------------------------------------------------

    matched_phrase = False

    for pattern in PHRASE_PATTERNS:
        if re.search(pattern, skill, flags=re.IGNORECASE):
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
    # Reject obvious hashtag / list fragments
    # --------------------------------------------------------

    if skill.startswith("#"):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "non_skill_phrase"
        })
        continue

    # --------------------------------------------------------
    # Reject obvious numbered-list fragments
    # --------------------------------------------------------

    if re.match(r"^\s*\d+[\.\)]\s+", skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "non_skill_phrase"
        })
        continue

    # --------------------------------------------------------
    # Otherwise accept
    # --------------------------------------------------------

    accepted.append({
        "skill_id": skill_id,
        "skill_name": skill
    })


# ============================================================
# SAVE OUTPUT
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
print("V8 CLEANING COMPLETED")
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
# CHECK IMPORTANT TECHNICAL SKILLS
# ============================================================

print()
print("=" * 70)
print("TECHNICAL DICTIONARY CHECK")
print("=" * 70)

clean_normalized = {
    normalize_skill(x)
    for x in clean_df["skill_name"].tolist()
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
    status = (
        "PRESENT"
        if normalize_skill(skill) in clean_normalized
        else "NOT IN CLEAN DICTIONARY"
    )

    print(f"{skill}: {status}")


# ============================================================
# GENERIC TERM CHECK
# ============================================================

print()
print("=" * 70)
print("GENERIC TERM CHECK")
print("=" * 70)

remaining_generic = []

for skill in clean_df["skill_name"]:

    normalized = normalize_skill(skill)

    if normalized in {
        normalize_skill(x)
        for x in GENERIC_TERMS
    }:
        if normalized not in PROTECTED_SKILLS:
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

for skill in sorted(short_skills, key=lambda x: x.lower()):
    print(skill)


# ============================================================
# SAMPLE ACCEPTED SKILLS
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