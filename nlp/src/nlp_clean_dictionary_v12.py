import os
import re
import pandas as pd

# ============================================================
# NLP DICTIONARY CLEANING - V12
# ============================================================
# Input:
#   skills_dictionary_clean_v11.csv
#
# Output:
#   skills_dictionary_clean_v12.csv
#   skills_dictionary_rejected_v12.csv
#
# Purpose:
#   V12 removes remaining generic/job-description vocabulary
#   identified during V11 extraction validation while preserving
#   technical and professional skills.
# ============================================================


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v11.csv"
)

OUTPUT_CLEAN = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v12.csv"
)

OUTPUT_REJECTED = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_rejected_v12.csv"
)


# ------------------------------------------------------------
# PROTECTED TECHNICAL / PROFESSIONAL SKILLS
# ------------------------------------------------------------

PROTECTED_SKILLS = {
    # Programming
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "f#",
    "php",
    "vba",
    "x++",

    # Web
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "node js",
    "nodejs",
    "xml",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "oracle",
    "mongodb",
    "db2",

    # Cloud
    "aws",
    "azure",
    "microsoft azure",
    "google cloud",
    "gcp",
    "cloud computing",

    # DevOps
    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "jenkins",
    "terraform",
    "ansible",

    # Data / AI
    "machine learning",
    "machine-learning",
    "machinelearning",
    "deep learning",
    "deep-learning",
    "deeplearning",
    "nlp",
    "natural language processing",
    "natural language understanding",
    "artificial intelligence",
    "data science",
    "data analytics",
    "data engineering",

    # BI
    "power bi",
    "microsoft power bi",
    "tableau",
    "excel",
    "microsoft excel",
    "ms excel",
    "excel macros",
    "excel vba",

    # Enterprise
    "sap",
    "salesforce",
    "servicenow",
    "oracle erp",
    "erp",
    "crm",

    # Security
    "cybersecurity",
    "cyber security",
    "information security",
    "network security",
    "ethical hacking",
    "penetration testing",

    # Networking
    "tcp",
    "udp",
    "dns",
    "vpn",
    "ssl",
    "ssh",
    "iam",

    # Engineering / technical
    "cad",
    "cam",
    "cae",
    "pcb",
    "plc",
    "scada",
    "autocad",
    "solidworks",

    # Project / professional skills
    "project management",
    "product management",
    "program management",
    "risk management",
    "change management",
    "financial management",
    "performance management",

    # Common valid abbreviations
    "api",
    "sdk",
    "etl",
    "elt",
    "qa",
    "ui",
    "ux",
    "bi",
    "hr",
    "kpi",
    "roi",
    "seo",
    "sem",
    "ats",
    "ga4",
    "hcm",
    "hl7",
    "ec2",
    "es6",
    "n8n",
    "ios",
    "gpu",
    "cpu",
    "ram",
    "rf",
    "mac",
    "vm",

    # Other legitimate short technical skills
    "2d",
    "3d",
    "4g",
    "5g",
    "c+",
    "c++",
    "a+",
}


# ------------------------------------------------------------
# V12 TARGETED GENERIC / NON-SKILL TERMS
# ------------------------------------------------------------

GENERIC_TERMS = {
    # Identified directly from V11 validation
    "data",
    "profile",
    "profile",
    "cloud",
    "testing",
    "reports",
    "freshers",
    "implement",
    "insurance",
    "certification",
    "reporting",
    "analytical",
    "finance",
    "integration",
    "developing",
    "equivalent",
    "problem-solving",
    "market",
    "growth",
    "tech",
    "full time",
    "monitor",
    "call",
    "code",

    # Common generic words
    "strong",
    "high",
    "good",
    "basic",
    "excellent",
    "professional",
    "expertise",
    "experience",
    "knowledge",
    "skills",
    "skill",
    "ability",
    "responsibility",
    "responsibilities",
    "requirement",
    "requirements",
    "candidate",
    "candidates",
    "job",
    "jobs",
    "role",
    "roles",
    "work",
    "working",
    "team",
    "teams",
    "member",
    "members",
    "manager",
    "management",
    "lead",
    "leader",
    "leadership",
    "senior",
    "junior",
    "executive",
    "associate",
    "support",
    "service",
    "services",
    "business",
    "customer",
    "customers",
    "client",
    "clients",
    "company",
    "organization",
    "industry",
    "field",
    "office",
    "operations",
    "operation",
    "process",
    "processes",
    "planning",
    "delivery",
    "development",
    "develop",
    "documentation",
    "communication",
    "written",
    "verbal",
    "interpersonal",
    "public",
    "providing",
    "prepare",
    "preparing",
    "maintain",
    "maintaining",
    "maintenance",
    "monitoring",
    "problem",
    "problems",
    "similar",
    "global",
    "international",
    "complex",
    "time",
    "year",
    "years",
    "shift",
    "schedule",
    "quality",
    "performance",
    "production",
    "administration",
    "administrative",
    "environment",
    "company",
    "projects",
    "project",
    "tools",
    "systems",
    "system",
    "computer",
    "computer science",
    "science",
    "marketing",
    "financial",
    "financials",
    "sales",
    "selling",
    "upselling",
    "cross",
    "cross selling",
    "strategist",
    "adherence",
    "call",
    "calls",
    "written communication",
    "good communication",
    "excellent communication",
    "best practices",
    "clarity",
    "providing",
    "join",
    "growth",
    "market",
    "insurance",
    "banking",
    "finance",
    "financial",
    "freshers",
    "fresher",
    "full time",
    "part time",
}


# ------------------------------------------------------------
# JOB / EDUCATION / PERSONAL INFORMATION
# ------------------------------------------------------------

NON_SKILL_PHRASES = {
    "freshers",
    "fresher",
    "full time",
    "part time",
    "equivalent",
    "experience",
    "years of experience",
    "candidate",
    "candidates",
    "job description",
    "job role",
    "responsibilities",
    "requirements",
    "qualification",
    "qualifications",
    "education",
    "degree",
    "diploma",
    "graduate",
    "graduation",
    "post graduate",
    "postgraduate",
    "under graduate",
    "undergraduate",
    "10th pass",
    "12th pass",
    "2025 pass out",
}


# ------------------------------------------------------------
# DESCRIPTION PHRASE DETECTION
# ------------------------------------------------------------

DESCRIPTION_PATTERNS = [
    r"\bshould have\b",
    r"\bmust have\b",
    r"\bmust be\b",
    r"\bshould be\b",
    r"\bwill be\b",
    r"\bresponsible for\b",
    r"\blooking for\b",
    r"\bwe are looking\b",
    r"\bability to\b",
    r"\bexperience in\b",
    r"\bexperience with\b",
    r"\bknowledge of\b",
    r"\bproficiency in\b",
    r"\bproficient in\b",
    r"\bfamiliar with\b",
    r"\bworking with\b",
    r"\bworked on\b",
    r"\bworked with\b",
    r"\bstrong knowledge\b",
    r"\bstrong experience\b",
    r"\bgood knowledge\b",
    r"\bexcellent knowledge\b",
    r"\bexcellent communication\b",
    r"\bgood communication\b",
    r"\bstrong communication\b",
    r"\byears? of\b",
    r"\b\d+\+?\s*years?\b",
]


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).strip().lower()

    text = re.sub(r"\s+", " ", text)

    return text


def canonicalize(text):
    """
    Keep the V11 canonical value where possible.
    """
    text = str(text).strip()

    mapping = {
        "microsoft azure": "Azure",
        "ms azure": "Azure",
        "native azure": "Azure",
        "azure cloud": "Azure",

        "natural language processing": "NLP",
        "natural language understanding": "NLP",
        "nlp models": "NLP",
        "nlp generative": "NLP",

        "microsoft excel": "Excel",
        "ms excel": "Excel",
        "ms - excel": "Excel",
        "advance excel": "Excel",
        "advanced excel": "Excel",
        "advanced ms excel": "Excel",
        "basic excel": "Excel",
        "excel macros": "Excel",
        "excel vba": "Excel",

        "microsoft sql": "SQL",
        "ms sql": "SQL",

        "microsoft power bi": "Power BI",

        "node js": "Node.js",
        "nodejs": "Node.js",

        "machine-learning": "Machine Learning",
        "machinelearning": "Machine Learning",

        "deep-learning": "Deep Learning",
        "deeplearning": "Deep Learning",

        "javascript": "JavaScript",

        "typescript": "TypeScript",
    }

    return mapping.get(normalize(text), text)


def is_protected_skill(text):
    return normalize(text) in PROTECTED_SKILLS


def is_generic(text):
    return normalize(text) in GENERIC_TERMS


def is_non_skill_phrase(text):
    return normalize(text) in NON_SKILL_PHRASES


def looks_like_description(text):
    value = normalize(text)

    for pattern in DESCRIPTION_PATTERNS:
        if re.search(pattern, value):
            return True

    return False


def looks_like_sentence(text):
    value = str(text).strip()

    # Too long to reasonably be a standalone skill
    if len(value) > 100:
        return True

    # Multiple sentence-like clauses
    if value.count(",") >= 3:
        return True

    if value.count(";") >= 2:
        return True

    if re.search(r"\b(and|or)\b", value.lower()) and len(value.split()) > 10:
        return True

    return False


def looks_like_numeric_noise(text):
    value = normalize(text)

    # Pure numeric / code-like values
    if re.fullmatch(r"\d+", value):
        return True

    if re.fullmatch(r"\d+(\.\d+)?", value):
        return True

    # Salary-like
    if re.search(r"\b\d+\s*lpa\b", value):
        return True

    # Age-like
    if re.search(r"\b\d+\+?\s*age\b", value):
        return True

    # Pass-out years
    if re.search(r"\b20\d{2}\s*pass\s*out\b", value):
        return True

    # Time expressions
    if re.fullmatch(r"\d+\s*(am|pm)", value):
        return True

    # 24/7 style availability phrase
    if value in {"24/7", "24x7", "247.ai"}:
        return True

    return False


def looks_like_role_fragment(text):
    value = normalize(text)

    role_fragments = {
        "manager",
        "senior manager",
        "junior manager",
        "executive",
        "associate",
        "developer",
        "engineer",
        "designer",
        "analyst",
        "consultant",
        "specialist",
        "recruiter",
        "administrator",
        "administrator",
        "director",
        "officer",
        "lead",
        "leader",
        "strategist",
        "intern",
        "trainee",
        "architect",
    }

    return value in role_fragments


# ------------------------------------------------------------
# LOAD V11 DICTIONARY
# ------------------------------------------------------------

print("=" * 70)
print("NLP DICTIONARY CLEANING - V12")
print("=" * 70)

print("\nLoading V11 dictionary...")

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"\nV11 dictionary not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print(f"Input rows: {len(df):,}")

required_columns = {"skill_id", "skill_name"}

missing = required_columns - set(df.columns)

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )


# ------------------------------------------------------------
# PROCESS
# ------------------------------------------------------------

accepted_rows = []
rejected_rows = []

seen_canonical = set()

for _, row in df.iterrows():

    skill_id = row["skill_id"]
    skill_name = str(row["skill_name"]).strip()

    if not skill_name:
        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "empty_skill"
        })
        continue

    normalized = normalize(skill_name)
    canonical = canonicalize(skill_name)
    canonical_normalized = normalize(canonical)

    # --------------------------------------------------------
    # PROTECTED SKILLS ALWAYS SURVIVE
    # --------------------------------------------------------

    if is_protected_skill(skill_name):
        if canonical_normalized in seen_canonical:
            rejected_rows.append({
                "skill_id": skill_id,
                "skill_name": skill_name,
                "reason": "duplicate_canonical_skill"
            })
            continue

        seen_canonical.add(canonical_normalized)

        accepted_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "canonical_skill_name": canonical
        })

        continue

    # --------------------------------------------------------
    # INVALID SHORT SKILLS
    # --------------------------------------------------------

    if len(normalized) <= 1:

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "invalid_short_skill"
        })

        continue

    # Two/three-character alphabetic values are rejected unless
    # explicitly protected.
    if (
        len(normalized) <= 3
        and normalized.isalpha()
        and normalized not in PROTECTED_SKILLS
    ):
        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "invalid_short_skill"
        })
        continue

    # --------------------------------------------------------
    # GENERIC TERMS
    # --------------------------------------------------------

    if is_generic(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "generic"
        })

        continue

    # --------------------------------------------------------
    # NON-SKILL PHRASES
    # --------------------------------------------------------

    if is_non_skill_phrase(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "non_skill_phrase"
        })

        continue

    # --------------------------------------------------------
    # NUMERIC / PERSONAL INFORMATION
    # --------------------------------------------------------

    if looks_like_numeric_noise(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "numeric_or_personal_information"
        })

        continue

    # --------------------------------------------------------
    # JOB ROLE FRAGMENTS
    # --------------------------------------------------------

    if looks_like_role_fragment(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "job_role"
        })

        continue

    # --------------------------------------------------------
    # DESCRIPTION PHRASES
    # --------------------------------------------------------

    if looks_like_description(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "description_phrase"
        })

        continue

    # --------------------------------------------------------
    # SENTENCE-LIKE VALUES
    # --------------------------------------------------------

    if looks_like_sentence(skill_name):

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "sentence_or_description"
        })

        continue

    # --------------------------------------------------------
    # DUPLICATE CANONICAL SKILL
    # --------------------------------------------------------

    if canonical_normalized in seen_canonical:

        rejected_rows.append({
            "skill_id": skill_id,
            "skill_name": skill_name,
            "reason": "duplicate_canonical_skill"
        })

        continue

    seen_canonical.add(canonical_normalized)

    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    accepted_rows.append({
        "skill_id": skill_id,
        "skill_name": skill_name,
        "canonical_skill_name": canonical
    })


# ------------------------------------------------------------
# DATAFRAMES
# ------------------------------------------------------------

clean_df = pd.DataFrame(accepted_rows)
rejected_df = pd.DataFrame(rejected_rows)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("V12 CLEANING COMPLETED")
print("=" * 70)

print(f"Original skills : {len(df):,}")
print(f"Accepted skills : {len(clean_df):,}")
print(f"Rejected skills : {len(rejected_df):,}")

print("\nREJECTION REASONS:")

if len(rejected_df) > 0:
    print(
        rejected_df["reason"]
        .value_counts()
        .to_string()
    )
else:
    print("No rejected skills.")


# ------------------------------------------------------------
# TECHNICAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TECHNICAL DICTIONARY CHECK")
print("=" * 70)

technical_skills = [
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

clean_normalized = set(
    clean_df["canonical_skill_name"]
    .astype(str)
    .map(normalize)
)

for skill in technical_skills:

    if normalize(skill) in clean_normalized:
        print(f"{skill}: PRESENT")
    else:
        print(f"{skill}: NOT IN CLEAN DICTIONARY")


# ------------------------------------------------------------
# GENERIC TERM CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("GENERIC TERM CHECK")
print("=" * 70)

remaining_generic = []

for skill in clean_df["canonical_skill_name"].astype(str):

    if normalize(skill) in GENERIC_TERMS:
        remaining_generic.append(skill)

if remaining_generic:
    print("WARNING - generic terms still present:")
    for skill in sorted(set(remaining_generic)):
        print(skill)
else:
    print("No explicitly blocked generic terms remain.")


# ------------------------------------------------------------
# V11 PROBLEMATIC TERMS CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("V11 PROBLEMATIC TERM CHECK")
print("=" * 70)

v11_problematic = [
    "Data",
    "ProFile",
    "CLOUD",
    "TESTING",
    "REPORTS",
    "FRESHERS",
    "implement",
    "Insurance",
    "Certification",
    "Reporting",
    "Analytical",
    "FINANCE",
    "INTEGRATION",
    "developing",
    "equivalent",
    "Problem-Solving",
    "Market",
    "Growth",
    "TECH",
    "full time",
    "Monitor",
    "Call",
    "code",
    "Providing",
    "Public",
    "Clarity",
    "similar",
]

clean_values = set(
    clean_df["canonical_skill_name"]
    .astype(str)
    .map(normalize)
)

for term in v11_problematic:

    if normalize(term) in clean_values:
        print(f"STILL PRESENT: {term}")
    else:
        print(f"REMOVED: {term}")


# ------------------------------------------------------------
# SHORT SKILL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SHORT SKILLS <=3")
print("=" * 70)

short_df = clean_df[
    clean_df["canonical_skill_name"]
    .astype(str)
    .map(normalize)
    .str.len()
    <= 3
]

print(f"Count: {len(short_df)}")

if len(short_df) > 0:

    for skill in sorted(
        short_df["canonical_skill_name"]
        .astype(str)
        .unique(),
        key=lambda x: (len(x), x.lower())
    ):
        print(skill)


# ------------------------------------------------------------
# SAMPLE CLEAN SKILLS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SAMPLE CLEAN SKILLS")
print("=" * 70)

print(
    clean_df[
        ["skill_id", "skill_name", "canonical_skill_name"]
    ]
    .head(30)
    .to_string(index=False)
)


# ------------------------------------------------------------
# OUTPUT PATHS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(f"Clean V12 dictionary:")
print(OUTPUT_CLEAN)

print(f"\nRejected V12 dictionary:")
print(OUTPUT_REJECTED)

print("\nPostgreSQL was NOT modified.")
print("=" * 70)