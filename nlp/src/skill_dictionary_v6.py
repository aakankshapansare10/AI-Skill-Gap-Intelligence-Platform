import os
import re
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills.csv"
)

OUTPUT_CLEAN = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v6.csv"
)

OUTPUT_REJECTED = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_rejected_v6.csv"
)


# ============================================================
# SHORT SKILLS THAT ARE ALLOWED
# ============================================================

ALLOWED_SHORT_SKILLS = {
    "2d", "3d", "4g", "5g",
    "a+", "api", "ats", "aws",
    "bi", "c#", "c++",
    "cad", "cae", "cam",
    "cpu", "crm", "css", "cv",
    "db2", "dns", "ec2", "eda",
    "elt", "erp", "es6", "etl",
    "f#", "ga4", "gpu",
    "hcm", "hl7", "hr",
    "iam", "ios", "kpi",
    "mac", "n8n",
    "pcb", "php", "plc",
    "qa", "ram", "rf", "roi",
    "sap", "sas", "sdk",
    "sem", "seo", "sql",
    "ssh", "ssl",
    "tcp", "udp",
    "ui", "ux",
    "vba", "vm", "vpn",
    "x++", "xml"
}


# ============================================================
# GENERIC TERMS TO REMOVE
# ============================================================

GENERIC_TERMS = {
    "skills",
    "skill",
    "team",
    "teams",
    "management",
    "manage",
    "system",
    "systems",
    "time",
    "science",
    "project",
    "projects",
    "shift",
    "clients",
    "client",
    "financial",
    "finance",
    "global",
    "public",
    "providing",
    "provide",
    "prepare",
    "call",
    "growth",
    "basic",
    "clarity",
    "functional",
    "dynamic",
    "travel",
    "similar",
    "part",
    "review",
    "local",
    "tasks",
    "core",
    "focus",
    "platform",
    "office",
    "career",
    "salary",
    "company",
    "business",
    "industry",
    "field",
    "service",
    "services",
    "customer",
    "customers",
    "technical",
    "technology",
    "software",
    "application",
    "applications",
    "development",
    "develop",
    "developing",
    "requirements",
    "planning",
    "documentation",
    "leadership",
    "relationship",
    "experience",
    "education",
    "qualification",
    "process",
    "processes",
    "environment",
    "product",
    "products",
    "activities",
    "handling",
    "identify",
    "implement",
    "implementation",
    "building",
    "build",
    "analysis",
    "analytical",
    "performance",
    "tools",
    "quality",
    "expertise",
    "operations",
    "operation",
    "computer",
    "associate",
    "professional",
    "support",
    "communication",
    "sales",
    "marketing",
    "compliance",
    "standards",
    "training",
    "english",
    "reporting",
    "reports",
    "strategy",
    "market",
    "monitor",
    "monitoring",
    "maintaining",
    "maintenance",
    "execution",
    "administration",
    "interpersonal",
    "bank",
    "banking",
    "accounts",
    "accounting",
    "health",
    "research",
    "policies",
    "procedures",
    "tasks",
    "learning",
    "dynamic",
    "travel",
    "fresher",
    "freshers",
    "full time",
    "masters",
    "master",
    "certification",
    "certifications"
}


# ============================================================
# NON-SKILL PHRASES
# ============================================================

NON_SKILL_PHRASES = {
    "good communication",
    "excellent communication",
    "well communication",
    "be degree",
    "all degree",
    "any degree",
    "any graduate",
    "all graduate",
    "graduate",
    "graduation",
    "degree",
    "bachelor",
    "master degree",
    "masters degree",
    "minimum qualification",
    "required qualification",
    "years of experience",
    "year of experience",
    "experience required",
    "job description",
    "job role",
    "job title",
    "job profile",
    "work experience",
    "full time",
    "part time",
    "sales executive"
}


# ============================================================
# JOB / ROLE WORDS
# ============================================================

ROLE_WORDS = {
    "manager",
    "senior",
    "junior",
    "executive",
    "engineer",
    "engineering",
    "developer",
    "associate",
    "analyst",
    "officer",
    "lead",
    "leader",
    "director",
    "consultant",
    "specialist",
    "administrator",
    "supervisor",
    "coordinator",
    "intern",
    "trainee",
    "recruiter",
    "architect",
    "assistant",
    "representative",
    "professional",
    "designer",
    "designer events"
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(skill):
    skill = str(skill).strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_skill(skill):

    original = str(skill).strip()
    normalized = normalize_skill(original)

    if not normalized:
        return "empty"

    # --------------------------------------------------------
    # Explicit non-skill phrases
    # --------------------------------------------------------

    if normalized in NON_SKILL_PHRASES:
        return "non_skill_phrase"

    # --------------------------------------------------------
    # Generic terms
    # --------------------------------------------------------

    if normalized in GENERIC_TERMS:
        return "generic"

    # --------------------------------------------------------
    # Role words
    # --------------------------------------------------------

    if normalized in ROLE_WORDS:
        return "job_role"

    # --------------------------------------------------------
    # Very short skills
    # --------------------------------------------------------

    if len(normalized) == 1:

        if normalized.isalpha():
            return "invalid_short_skill"

    if len(normalized) <= 3:

        if normalized in ALLOWED_SHORT_SKILLS:
            return None

        # Reject alphabetic short terms
        if normalized.isalpha():
            return "invalid_short_skill"

        # Reject numeric/alphanumeric noise
        if any(ch.isdigit() for ch in normalized):
            return "invalid_short_skill"

    # --------------------------------------------------------
    # Qualification / experience phrases
    # --------------------------------------------------------

    qualification_patterns = [
        r"\b\d+\+?\s*(year|years|yr|yrs)\b",
        r"\b\d+\s*to\s*\d+\s*(year|years|yr|yrs)\b",
        r"\b\d+\s*(year|years|yr|yrs)\s*(of)?\s*experience\b",
        r"\bexperience\s*(required|needed)\b",
        r"\bminimum\s+qualification\b",
        r"\brequired\s+qualification\b",
        r"\b\d+(th|st|nd|rd)\s*(pass|class)?\b",
        r"\b\d+\+?\s*age\b",
        r"\bgraduate\b",
        r"\bgraduation\b",
        r"\bdegree\b",
        r"\bbachelor\b",
        r"\bmaster\b",
        r"\bmasters\b"
    ]

    for pattern in qualification_patterns:

        if re.search(pattern, normalized):
            return "experience_or_qualification"

    # --------------------------------------------------------
    # Obvious sentence / description phrases
    # --------------------------------------------------------

    words = normalized.split()

    if len(words) >= 10:
        return "sentence_or_description"

    if len(words) >= 7:
        if any(
            word in {
                "experience",
                "required",
                "skills",
                "responsibilities",
                "candidate",
                "years",
                "role",
                "project",
                "knowledge"
            }
            for word in words
        ):
            return "sentence_or_description"

    # --------------------------------------------------------
    # Excessive punctuation
    # --------------------------------------------------------

    if len(normalized) <= 6:

        alpha_num = sum(
            ch.isalnum()
            for ch in normalized
        )

        if alpha_num <= 1:
            return "special_character_noise"

    return None


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("SKILL DICTIONARY CLEANING - V6")
print("=" * 70)

print("\nInput file:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal skills: {len(df):,}")


accepted = []
rejected = []

seen_normalized = set()

for _, row in df.iterrows():

    skill_id = int(row["skill_id"])
    skill_name = str(row["skill_name"]).strip()

    normalized = normalize_skill(skill_name)

    # --------------------------------------------------------
    # Duplicate normalized skills
    # --------------------------------------------------------

    if normalized in seen_normalized:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "rejection_reason": "duplicate_normalized_skill"
        })

        continue

    seen_normalized.add(normalized)

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    reason = classify_skill(skill_name)

    if reason is not None:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "rejection_reason": reason
        })

    else:

        accepted.append({
            "skill_id": skill_id,
            "skill_name": skill_name
        })


# ============================================================
# SAVE
# ============================================================

clean_df = pd.DataFrame(
    accepted,
    columns=[
        "skill_id",
        "skill_name"
    ]
)

rejected_df = pd.DataFrame(
    rejected,
    columns=[
        "skill_id",
        "skill_name",
        "rejection_reason"
    ]
)

clean_df.to_csv(
    OUTPUT_CLEAN,
    index=False
)

rejected_df.to_csv(
    OUTPUT_REJECTED,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V6 CLEANING COMPLETED")
print("=" * 70)

print(f"\nOriginal skills: {len(df):,}")
print(f"Accepted skills : {len(clean_df):,}")
print(f"Rejected skills : {len(rejected_df):,}")

print("\nRejection reasons:")

print(
    rejected_df["rejection_reason"]
    .value_counts()
    .to_string()
)


# ============================================================
# CHECK IMPORTANT TERMS
# ============================================================

CHECK_TERMS = [
    "skills",
    "Team",
    "Management",
    "Data",
    "DESIGN",
    "manage",
    "Teams",
    "Systems",
    "Time",
    "Science",
    "PROJECT",
    "Shift",
    "Compliance",
    "Marketing",
    "Financial",
    "clients",
    "FRESHERS",
    "System",
    "Good Communication",
    "TESTING",
    "ENGLISH",
    "TRAINING",
    "standards",
    "Certification",
    "Excellent Communication",
    "Automation",
    "Python",
    "SQL",
    "Java",
    "JavaScript",
    "AWS",
    "Docker",
    "Kubernetes",
    "Machine Learning",
    "Deep Learning",
    "React",
    "Angular",
    "Node.js",
    "Power BI",
    "Tableau"
]

print("\n" + "=" * 70)
print("CHECKING IMPORTANT TERMS")
print("=" * 70)

clean_normalized = {
    normalize_skill(x)
    for x in clean_df["skill_name"]
}

for term in CHECK_TERMS:

    normalized = normalize_skill(term)

    if normalized in clean_normalized:
        print(f"PRESENT: {term}")
    else:
        print(f"REMOVED : {term}")


# ============================================================
# SHORT SKILLS
# ============================================================

short_df = clean_df[
    clean_df["skill_name"]
    .astype(str)
    .str.len() <= 3
]

print(
    f"\nSkills with <= 3 characters remaining: "
    f"{len(short_df):,}"
)

if not short_df.empty:

    print("\nRemaining short skills:")

    print(
        short_df[
            ["skill_id", "skill_name"]
        ]
        .to_string(index=False)
    )


# ============================================================
# SAMPLE
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE OF V6 CLEANED SKILLS")
print("=" * 70)

print(
    clean_df.head(100)
    .to_string(index=False)
)


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print("\nClean V6 dictionary:")
print(OUTPUT_CLEAN)

print("\nRejected V6 dictionary:")
print(OUTPUT_REJECTED)

print("\nIMPORTANT:")
print("V1-V5 dictionary files were NOT modified.")
print("PostgreSQL was NOT modified.")