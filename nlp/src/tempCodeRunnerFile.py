import os
import re
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

# skill_dictionary.py is inside:
# AI_skill_gaps_intelligence_platform\nlp\src

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

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
    "skills_dictionary_clean_v3.csv"
)

REJECTED_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "skills_dictionary_rejected_v3.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

# Legitimate short technical skills/abbreviations.
# These are allowed even though they are short.
ALLOWED_SHORT_SKILLS = {
    "ai",
    "ml",
    "nlp",
    "cv",
    "qa",
    "vm",
    "api",
    "sdk",
    "sql",
    "nosql",
    "crm",
    "erp",
    "sap",
    "aws",
    "gcp",
    "iam",
    "etl",
    "elt",
    "bi",
    "kpi",
    "okr",
    "roi",
    "seo",
    "sem",
    "hr",
    "hcm",
    "ats",
    "ui",
    "ux",
    "ux/ui",
    "ios",
    "mac",
    "gpu",
    "cpu",
    "ram",
    "rom",
    "tcp",
    "udp",
    "dns",
    "vpn",
    "ssl",
    "tls",
    "ssh",
    "xml",
    "json",
    "html",
    "css",
    "php",
    "c",
    "c++",
    "c#",
    "r",
    "go",
    "abap",
    "sas",
    "vba",
    "vlsi",
    "eda",
    "plc",
    "scada",
    "cad",
    "cam",
    "cae",
    "pcb",
    "rf",
    "5g",
    "4g",
    "2d",
    "3d",
    "x++",
    "n8n",
    "aws",
    "azure",
    "gcp",
}


# ============================================================
# GENERIC WORDS
# ============================================================

# Words that are usually too generic to be useful as skills.
GENERIC_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "build",
    "building",
    "business",
    "career",
    "company",
    "complex",
    "control",
    "customer",
    "data",
    "delivery",
    "develop",
    "developing",
    "development",
    "education",
    "environment",
    "equivalent",
    "experienced",
    "experience",
    "field",
    "functional",
    "growth",
    "handling",
    "high",
    "identify",
    "industry",
    "join",
    "key",
    "manage",
    "management",
    "process",
    "processes",
    "problem",
    "project",
    "report",
    "reporting",
    "salary",
    "science",
    "skill",
    "skills",
    "software",
    "strong",
    "system",
    "systems",
    "targets",
    "team",
    "teams",
    "technical",
    "technology",
    "training",
    "written",
    "year",
    "years",
    "work",
    "working",
    "etc",
    "all",
    "any",
    "only",
    "part",
    "time",
    "high",
    "low",
    "new",
    "old",
    "good",
    "great",
    "excellent",
    "required",
    "requirements",
    "qualification",
    "qualifications",
    "responsibilities",
    "activities",
    "application",
    "applications",
    "company",
    "client",
    "clients",
    "candidate",
    "candidates",
    "job",
    "jobs",
    "role",
    "roles",
    "position",
    "positions",
    "degree",
    "graduate",
    "graduates",
    "bachelor",
    "master",
    "product",
    "products",
    "service",
    "services",
}


# ============================================================
# NON-SKILL PHRASES
# ============================================================

NON_SKILL_PHRASES = {
    "job description",
    "job descriptions",
    "job profile",
    "job profiles",
    "good communication",
    "strong communication",
    "excellent communication",
    "well communication",
    "excellent sourcing negotiation skills required",
    "all degree",
    "any graduate",
    "under graduate",
    "ca freshers only",
    "freshers only",
    "salary",
    "company",
    "job",
    "career",
    "join",
    "year",
    "years",
    "experience required",
    "work experience",
    "relevant experience",
    "required skills",
    "technical skills",
    "communication skills",
    "strong skills",
    "good skills",
}


# ============================================================
# QUALIFICATION / EXPERIENCE PATTERNS
# ============================================================

QUALIFICATION_PATTERNS = [
    r"\b\d+(?:st|nd|rd|th)\s+pass\b",
    r"\b\d+(?:st|nd|rd|th)\s+class\b",
    r"\b\d+(?:st|nd|rd|th)\b",
    r"\bany\s+degree\b",
    r"\ball\s+degree\b",
    r"\bany\s+graduate\b",
    r"\ball\s+graduate\b",
    r"\bunder\s+graduate\b",
    r"\bpost\s+graduate\b",
    r"\bpostgraduate\b",
    r"\bgraduate\b",
    r"\bgraduation\b",
    r"\bbachelor(?:'s)?\b",
    r"\bmaster(?:'s)?\b",
    r"\bdiploma\b",
    r"\biti\b",
    r"\bqualification\b",
    r"\bqualifications\b",
    r"\bfreshers?\b",
    r"\bfresher\b",
    r"\bca\s+freshers?\b",
]

EXPERIENCE_PATTERNS = [
    r"\b\d+\+?\s*years?\s+of\s+experience\b",
    r"\b\d+\+?\s*yrs?\s+of\s+experience\b",
    r"\b\d+\+?\s*years?\s+experience\b",
    r"\b\d+\+?\s*yrs?\s+experience\b",
    r"\b\d+\+?\s*years?\s+in\b",
    r"\b\d+\+?\s*yrs?\s+in\b",
    r"\bminimum\s+\d+\s+years?\b",
    r"\b\d+\s*-\s*\d+\s+years?\b",
    r"\bexperience\s+required\b",
    r"\byears?\s+experience\b",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize a skill name for comparison.
    """

    if pd.isna(text):
        return ""

    text = str(text).strip()

    # Replace line breaks/tabs with spaces
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_for_compare(text):
    """
    Normalize text for duplicate comparison.
    """

    text = normalize_text(text)

    text = text.lower()

    # Normalize ampersand
    text = text.replace("&", " and ")

    # Collapse spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SENTENCE / DESCRIPTION DETECTION
# ============================================================

def looks_like_sentence(text):
    """
    Detect obvious job-description fragments.
    """

    text_lower = text.lower().strip()

    # Very long entries are usually descriptions rather than skills.
    if len(text_lower) > 120:
        return True

    # Multiple sentences
    if text_lower.count(".") >= 2:
        return True

    # Sentence-style phrases
    sentence_patterns = [
        r"\bskills?\s+required\b",
        r"\bexperience\s+in\b",
        r"\bexperience\s+with\b",
        r"\bknowledge\s+of\b",
        r"\bability\s+to\b",
        r"\bresponsible\s+for\b",
        r"\bshould\s+have\b",
        r"\bmust\s+have\b",
        r"\bwill\s+be\s+responsible\b",
        r"\blooking\s+for\b",
        r"\bthe\s+candidate\b",
        r"\bcandidate\s+should\b",
        r"\bexcellent\s+\w+\s+skills\b",
        r"\bstrong\s+\w+\s+skills\b",
        r"\bgood\s+\w+\s+skills\b",
        r"\brequired\s+skills\b",
    ]

    for pattern in sentence_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


# ============================================================
# QUALIFICATION / EXPERIENCE DETECTION
# ============================================================

def looks_like_qualification_or_experience(text):
    text_lower = text.lower().strip()

    for pattern in QUALIFICATION_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    for pattern in EXPERIENCE_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False


# ============================================================
# GENERIC SKILL DETECTION
# ============================================================

def is_generic_skill(text):
    """
    Reject exact generic words.
    """

    normalized = normalize_for_compare(text)

    return normalized in GENERIC_WORDS


# ============================================================
# SHORT SKILL VALIDATION
# ============================================================

def is_valid_short_skill(text):
    """
    Allow legitimate technical abbreviations.
    Reject random 1-3 character strings.
    """

    normalized = normalize_for_compare(text)

    # Explicitly allowed technical abbreviations
    if normalized in ALLOWED_SHORT_SKILLS:
        return True

    # One character
    if len(normalized) <= 1:
        return False

    # Two or three character alphabetic strings are suspicious
    if len(normalized) <= 3 and normalized.isalpha():
        return False

    return True


# ============================================================
# SPECIAL CHARACTER / NUMERIC NOISE
# ============================================================

def looks_like_special_character_noise(text):
    normalized = normalize_text(text)

    # Empty
    if not normalized:
        return True

    # Mostly numbers
    if re.fullmatch(r"[\d\s\-\+/.,]+", normalized):
        return True

    # Starts with hashtags used like description fragments
    if normalized.startswith("#"):
        return True

    # Excessive punctuation
    punctuation_count = len(re.findall(r"[^A-Za-z0-9\s+#./&()_-]", normalized))

    if punctuation_count > 3:
        return True

    # Repeated separators
    if "###" in normalized or "///" in normalized:
        return True

    return False


# ============================================================
# NOISE DETECTION
# ============================================================

def looks_like_noise(text):
    normalized = normalize_text(text)

    if not normalized:
        return "empty"

    if looks_like_special_character_noise(normalized):
        return "special_character_noise"

    if not is_valid_short_skill(normalized):
        return "invalid_short_skill"

    if looks_like_qualification_or_experience(normalized):
        return "experience_or_qualification"

    if looks_like_sentence(normalized):
        return "sentence_or_description"

    if is_generic_skill(normalized):
        return "generic"

    normalized_compare = normalize_for_compare(normalized)

    if normalized_compare in NON_SKILL_PHRASES:
        return "non_skill_phrase"

    return None


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("SKILL DICTIONARY CLEANING - V3")
    print("=" * 70)

    print("\nChecking input file...")
    print("Input file:")
    print(INPUT_FILE)

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"\nInput file not found:\n{INPUT_FILE}"
        )

    print("\nLoading skills CSV...")

    df = pd.read_csv(
        INPUT_FILE,
        dtype={
            "skill_id": "Int64",
            "skill_name": "string"
        }
    )

    print(f"Original skills: {len(df):,}")

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = {"skill_id", "skill_name"}

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}\n"
            f"Available columns: {list(df.columns)}"
        )

    # --------------------------------------------------------
    # Process each skill
    # --------------------------------------------------------

    accepted_rows = []
    rejected_rows = []

    seen_normalized = set()

    for _, row in df.iterrows():

        skill_id = row["skill_id"]
        original_skill = row["skill_name"]

        skill = normalize_text(original_skill)

        reason = looks_like_noise(skill)

        if reason:

            rejected_rows.append({
                "skill_id": skill_id,
                "skill_name": skill,
                "rejection_reason": reason
            })

            continue

        # ----------------------------------------------------
        # Duplicate normalized skill detection
        # ----------------------------------------------------

        normalized = normalize_for_compare(skill)

        if normalized in seen_normalized:

            rejected_rows.append({
                "skill_id": skill_id,
                "skill_name": skill,
                "rejection_reason": "duplicate_normalized_skill"
            })

            continue

        seen_normalized.add(normalized)

        accepted_rows.append({
            "skill_id": skill_id,
            "skill_name": skill
        })

    # --------------------------------------------------------
    # Create output DataFrames
    # --------------------------------------------------------

    clean_df = pd.DataFrame(
        accepted_rows,
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

    # --------------------------------------------------------
    # Save files
    # --------------------------------------------------------

    clean_df.to_csv(
        CLEAN_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    rejected_df.to_csv(
        REJECTED_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("CLEANING COMPLETE")
    print("=" * 70)

    print(f"\nOriginal skills : {len(df):,}")
    print(f"Accepted skills : {len(clean_df):,}")
    print(f"Rejected skills : {len(rejected_df):,}")

    print("\nRejection reasons:")

    if len(rejected_df) > 0:

        counts = rejected_df["rejection_reason"].value_counts()

        for reason, count in counts.items():
            print(f"  {reason}: {count:,}")

    # --------------------------------------------------------
    # Output paths
    # --------------------------------------------------------

    print("\nOutput files:")

    print(f"Clean dictionary:")
    print(CLEAN_FILE)

    print(f"\nRejected dictionary:")
    print(REJECTED_FILE)

    # ========================================================
    # CHECK SUSPICIOUS TERMS
    # ========================================================

    print("\n" + "=" * 70)
    print("CHECKING PREVIOUSLY SUSPICIOUS TERMS")
    print("=" * 70)

    suspicious_terms = [
        "manage",
        "teams",
        "develop",
        "processes",
        "environment",
        "product",
        "company",
        "salary",
        "career",
        "job description",
        "well communication",
        "be degree",
        "under graduate",
        "year",
        "written",
        "targets",
        "application",
        "problem",
        "build",
        "building",
        "high",
        "technical",
        "technology",
        "software",
        "customer",
        "client",
        "delivery",
    ]

    clean_normalized = {
        normalize_for_compare(x)
        for x in clean_df["skill_name"].astype(str)
    }

    for term in suspicious_terms:

        if normalize_for_compare(term) in clean_normalized:
            print(f"STILL PRESENT : {term}")
        else:
            print(f"REMOVED       : {term}")

    # ========================================================
    # SHORT SKILL CHECK
    # ========================================================

    print("\n" + "=" * 70)
    print("CHECKING SHORT SKILLS")
    print("=" * 70)

    short_skills = clean_df[
        clean_df["skill_name"].astype(str).str.len() <= 3
    ]

    print(
        f"Skills with <= 3 characters remaining: "
        f"{len(short_skills):,}"
    )

    if len(short_skills) > 0:

        print("\nShort skills remaining:")

        print(
            short_skills[
                ["skill_id", "skill_name"]
            ].head(100).to_string(index=False)
        )

    # ========================================================
    # FINISH
    # ========================================================

    print("\n" + "=" * 70)
    print("V3 DICTIONARY CLEANING FINISHED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()