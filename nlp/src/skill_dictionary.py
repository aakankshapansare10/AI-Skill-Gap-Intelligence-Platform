import os
import re
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


# ============================================================
# INPUT / OUTPUT FILES
# ============================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills.csv"
)

CLEAN_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills_dictionary_clean_v5.csv"
)

REJECTED_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills_dictionary_rejected_v5.csv"
)


# ============================================================
# START
# ============================================================

print("=" * 70)
print("SKILL DICTIONARY CLEANING - V5")
print("=" * 70)

print("\nChecking input file...")

if not os.path.exists(INPUT_FILE):

    raise FileNotFoundError(
        f"\nInput file not found:\n{INPUT_FILE}"
    )

print(
    f"Input file:\n{INPUT_FILE}"
)


# ============================================================
# LOAD RAW SKILLS
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

required_columns = [
    "skill_id",
    "skill_name"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Missing required column: {column}"
        )

df = df.dropna(
    subset=[
        "skill_id",
        "skill_name"
    ]
).copy()

df["skill_id"] = df[
    "skill_id"
].astype(int)

df["skill_name"] = (
    df["skill_name"]
    .astype(str)
    .str.strip()
)

print(
    f"\nOriginal skills: "
    f"{len(df):,}"
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(value):

    value = str(value).strip().lower()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


# ============================================================
# LEGITIMATE SHORT TECHNICAL SKILLS
# ============================================================

ALLOWED_SHORT_SKILLS = {
    "2d",
    "3d",
    "4g",
    "5g",

    "a+",
    "api",
    "ats",
    "aws",

    "bi",
    "c#",
    "c++",
    "cad",
    "cae",
    "cam",
    "cpu",
    "crm",
    "css",

    "cv",

    "db2",
    "dns",

    "ec2",
    "eda",
    "elt",
    "erp",
    "es6",
    "etl",

    "f#",

    "ga4",
    "gpu",

    "hcm",
    "hl7",
    "hr",

    "iam",
    "ios",

    "kpi",

    "mac",

    "n8n",

    "pcb",
    "php",
    "plc",

    "qa",

    "ram",
    "rf",
    "roi",

    "sap",
    "sas",
    "sdk",
    "sem",
    "seo",
    "sql",
    "ssh",
    "ssl",

    "tcp",

    "udp",
    "ui",
    "ux",

    "vba",
    "vm",
    "vpn",

    "x++",
    "xml",
}


# ============================================================
# JOB ROLE / POSITION WORDS
# ============================================================

ROLE_WORDS = {
    "manager",
    "senior",
    "junior",
    "executive",
    "engineer",
    "engineering",
    "developer",
    "development",
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
}


# ============================================================
# GENERIC BUSINESS / JOB WORDS
# ============================================================

GENERIC_WORDS = {
    "communication",
    "sales",
    "support",
    "maintain",
    "tools",
    "performance",
    "office",
    "hiring",
    "operations",
    "computer",
    "quality",
    "expertise",
    "analysis",
    "projects",
    "relationship",
    "planning",
    "insurance",
    "international",
    "finance",
    "reports",
    "leadership",
    "banking",
    "documentation",
    "stakeholders",
    "analytical",

    "company",
    "salary",
    "career",
    "delivery",
    "customer",
    "client",
    "problem",
    "application",
    "build",
    "building",
    "technical",
    "technology",
    "software",

    "cross",
    "selling",
    "strategist",
    "schedule",
    "adherence",

    "managerial",
    "professional",
    "expertise",
    "activities",
    "handling",
    "identify",
    "implement",
    "develop",
    "developing",
    "process",
    "processes",
    "requirements",
    "environment",
    "product",
    "products",
    "service",
    "services",
    "business",
    "industry",
    "field",
    "education",
    "qualification",
    "experience",
    "experienced",
    "equivalent",
    "year",
    "years",
    "written",
    "high",
    "complex",
    "strong",
    "key",
    "all",
    "any",
    "join",
    "targets",
}


# ============================================================
# NON-SKILL PHRASES
# ============================================================

NON_SKILL_PHRASES = {
    "be degree",
    "under graduate",
    "job description",
    "well communication",
    "ca freshers only",
    "all degree",
    "any graduate",
    "10th pass",
    "12th pass",
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
    "job role",
    "job title",
    "job profile",
    "work experience",
}


# ============================================================
# QUALIFICATION / EXPERIENCE PATTERNS
# ============================================================

QUALIFICATION_PATTERNS = [

    r"\b\d+(st|nd|rd|th)\s+pass\b",

    r"\b\d+\s*years?\s+of\s+experience\b",

    r"\b\d+\+?\s*years?\s+experience\b",

    r"\bmin(imum)?\s+\d+\s*[-to]+\s*\d+\b",

    r"\bany\s+(graduate|degree)\b",

    r"\b(all|any)\s+degree\b",

    r"\bbachelor'?s?\s+degree\b",

    r"\bmaster'?s?\s+degree\b",

    r"\bdegree\s+required\b",

    r"\bqualification\s+required\b",

    r"\bexperience\s+required\b",
]


# ============================================================
# DESCRIPTION-LIKE PHRASES
# ============================================================

DESCRIPTION_PATTERNS = [

    r"\bskills?\s+required\b",

    r"\bknowledge\s+of\b",

    r"\bexperience\s+in\b",

    r"\bproficiency\s+in\b",

    r"\bability\s+to\b",

    r"\bresponsible\s+for\b",

    r"\bmust\s+have\b",

    r"\bshould\s+have\b",

    r"\brequired\s+skills?\b",

    r"\bexcellent\s+\w+\s+skills?\b",

    r"\bstrong\s+\w+\s+skills?\b",

    r"\b\d+\s+end[- ]to[- ]end\b",

    r"\bimplementations?\b",
]


# ============================================================
# SENTENCE DETECTION
# ============================================================

def looks_like_sentence(skill):

    text = str(skill).strip()

    words = text.split()

    # Long phrases are more likely to be descriptions
    if len(words) >= 10:
        return True

    # Too many punctuation marks
    punctuation_count = len(
        re.findall(
            r"[,:;!?]",
            text
        )
    )

    if punctuation_count >= 2:
        return True

    # Numbered-list style
    if re.search(
        r"^\s*\d+[\.\)]",
        text
    ):
        return True

    return False


# ============================================================
# QUALIFICATION / EXPERIENCE CHECK
# ============================================================

def looks_like_qualification(skill):

    text = normalize_skill(skill)

    for pattern in QUALIFICATION_PATTERNS:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            return True

    return False


# ============================================================
# DESCRIPTION CHECK
# ============================================================

def looks_like_description(skill):

    text = normalize_skill(skill)

    for pattern in DESCRIPTION_PATTERNS:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            return True

    return False


# ============================================================
# SPECIAL CHARACTER / NUMERIC NOISE
# ============================================================

def looks_like_special_noise(skill):

    text = str(skill).strip()

    if not text:
        return True

    # Extremely long numeric strings
    if re.fullmatch(
        r"[\d\s._/-]+",
        text
    ):
        return True

    # Mostly symbols
    alphanumeric_count = len(
        re.findall(
            r"[A-Za-z0-9]",
            text
        )
    )

    if alphanumeric_count == 0:
        return True

    return False


# ============================================================
# SHORT SKILL VALIDATION
# ============================================================

def invalid_short_skill(skill):

    text = normalize_skill(skill)

    # Explicitly allowed
    if text in ALLOWED_SHORT_SKILLS:
        return False

    # One character is not useful as standalone skill
    if len(text) <= 1:
        return True

    # Two or three character alphabetic fragments
    if len(text) <= 3 and text.isalpha():
        return True

    # Short numeric/alphanumeric fragments
    if len(text) <= 3 and re.search(
        r"\d",
        text
    ):
        return True

    return False


# ============================================================
# MAIN CLEANING
# ============================================================

clean_rows = []
rejected_rows = []

seen_normalized = set()

reason_counts = {}


def reject(row, reason):

    row_copy = row.copy()

    row_copy["rejection_reason"] = reason

    rejected_rows.append(
        row_copy
    )

    reason_counts[reason] = (
        reason_counts.get(
            reason,
            0
        ) + 1
    )


for _, row in df.iterrows():

    skill_id = int(
        row["skill_id"]
    )

    skill_name = str(
        row["skill_name"]
    ).strip()

    normalized = normalize_skill(
        skill_name
    )


    # --------------------------------------------------------
    # EMPTY
    # --------------------------------------------------------

    if not normalized:

        reject(
            row,
            "empty"
        )

        continue


    # --------------------------------------------------------
    # DUPLICATE NORMALIZED SKILL
    # --------------------------------------------------------

    if normalized in seen_normalized:

        reject(
            row,
            "duplicate_normalized_skill"
        )

        continue

    seen_normalized.add(
        normalized
    )


    # --------------------------------------------------------
    # EXPLICIT NON-SKILL PHRASE
    # --------------------------------------------------------

    if normalized in NON_SKILL_PHRASES:

        reject(
            row,
            "non_skill_phrase"
        )

        continue


    # --------------------------------------------------------
    # ROLE WORD
    # --------------------------------------------------------

    if normalized in ROLE_WORDS:

        reject(
            row,
            "job_role"
        )

        continue


    # --------------------------------------------------------
    # GENERIC WORD
    # --------------------------------------------------------

    if normalized in GENERIC_WORDS:

        reject(
            row,
            "generic"
        )

        continue


    # --------------------------------------------------------
    # SHORT SKILL
    # --------------------------------------------------------

    if invalid_short_skill(
        skill_name
    ):

        reject(
            row,
            "invalid_short_skill"
        )

        continue


    # --------------------------------------------------------
    # QUALIFICATION
    # --------------------------------------------------------

    if looks_like_qualification(
        skill_name
    ):

        reject(
            row,
            "experience_or_qualification"
        )

        continue


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    if looks_like_description(
        skill_name
    ):

        reject(
            row,
            "sentence_or_description"
        )

        continue


    # --------------------------------------------------------
    # SENTENCE
    # --------------------------------------------------------

    if looks_like_sentence(
        skill_name
    ):

        reject(
            row,
            "sentence_or_description"
        )

        continue


    # --------------------------------------------------------
    # SPECIAL / NUMERIC NOISE
    # --------------------------------------------------------

    if looks_like_special_noise(
        skill_name
    ):

        reject(
            row,
            "special_character_noise"
        )

        continue


    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    clean_rows.append({
        "skill_id": skill_id,
        "skill_name": skill_name
    })


# ============================================================
# CREATE DATAFRAMES
# ============================================================

clean_df = pd.DataFrame(
    clean_rows,
    columns=[
        "skill_id",
        "skill_name"
    ]
)

rejected_df = pd.DataFrame(
    rejected_rows,
    columns=[
        "skill_id",
        "skill_name",
        "rejection_reason"
    ]
)


# ============================================================
# SAVE OUTPUT
# ============================================================

clean_df.to_csv(
    CLEAN_FILE,
    index=False,
    encoding="utf-8"
)

rejected_df.to_csv(
    REJECTED_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V5 CLEANING COMPLETED")
print("=" * 70)

print(
    f"\nOriginal skills: "
    f"{len(df):,}"
)

print(
    f"Accepted skills : "
    f"{len(clean_df):,}"
)

print(
    f"Rejected skills : "
    f"{len(rejected_df):,}"
)


print("\nRejection reasons:")

for reason, count in sorted(
    reason_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"  {reason}: {count:,}"
    )


# ============================================================
# CHECK IMPORTANT TERMS
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "CHECKING PREVIOUSLY SUSPICIOUS TERMS:"
)

print("=" * 70)

terms_to_check = [
    "manager",
    "communication",
    "sales",
    "support",
    "engineer",
    "executive",
    "senior",
    "lead",
    "engineering",
    "maintain",
    "tools",
    "performance",
    "developer",
    "office",
    "hiring",
    "operations",
    "computer",
    "quality",
    "professional",
    "expertise",
    "analysis",
    "associate",
    "cross",
    "selling",
    "strategist",
    "schedule",
    "adherence",
    "be degree",
    "company",
    "salary",
    "career",
    "delivery",
    "customer",
    "client",
    "problem",
    "application",
    "build",
    "building",
    "technical",
    "technology",
    "software",
]


for term in terms_to_check:

    exists = (
        clean_df[
            clean_df["skill_name"]
            .astype(str)
            .str.lower()
            == term.lower()
        ]
        .shape[0]
        > 0
    )

    if exists:

        print(
            f"STILL PRESENT: {term}"
        )

    else:

        print(
            f"REMOVED: {term}"
        )


# ============================================================
# SHORT SKILL CHECK
# ============================================================

short_clean = clean_df[
    clean_df["skill_name"]
    .astype(str)
    .str.len()
    <= 3
]

print(
    "\nSkills with <= 3 characters "
    "remaining: "
    f"{len(short_clean):,}"
)

if not short_clean.empty:

    print(
        "\nRemaining short skills:"
    )

    print(
        short_clean[
            [
                "skill_id",
                "skill_name"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# IMPORTANT TECHNICAL SKILLS CHECK
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "IMPORTANT TECHNICAL SKILLS:"
)

print("=" * 70)

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

    exists = (
        clean_df[
            clean_df["skill_name"]
            .astype(str)
            .str.lower()
            == skill.lower()
        ]
        .shape[0]
        > 0
    )

    if exists:

        print(
            f"PRESENT: {skill}"
        )

    else:

        print(
            f"NOT IN CLEAN DICTIONARY: {skill}"
        )


# ============================================================
# SAMPLE ACCEPTED SKILLS
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "SAMPLE OF CLEANED SKILLS:"
)

print("=" * 70)

print(
    clean_df.head(100).to_string(
        index=False
    )
)


# ============================================================
# FILE LOCATIONS
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "OUTPUT FILES:"
)

print("=" * 70)

print(
    "\nClean V5 dictionary:"
)

print(
    CLEAN_FILE
)

print(
    "\nRejected V5 dictionary:"
)

print(
    REJECTED_FILE
)

print(
    "\nIMPORTANT:"
)

print(
    "Previous V1-V4 dictionary files were NOT modified."
)

print(
    "PostgreSQL was NOT modified."
)