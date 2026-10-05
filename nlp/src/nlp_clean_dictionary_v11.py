import pandas as pd
import re


# ============================================================
# FILE PATHS
# ============================================================

INPUT_FILE = r"..\..\data\processed\skills_dictionary_clean_v10.csv"

OUTPUT_FILE = r"..\..\data\processed\skills_dictionary_clean_v11.csv"

REJECTED_FILE = r"..\..\data\processed\skills_dictionary_rejected_v11.csv"


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):

    text = str(text).strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def normalized_lower(text):

    return normalize_text(text).lower()


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
    "c+",
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
    "git",
    "go",
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
    "xml",
    "x++"
}


# ============================================================
# CANONICAL ALIASES
#
# These map source variants to a canonical skill name.
# ============================================================

CANONICAL_ALIASES = {

    # --------------------------------------------------------
    # AZURE
    # --------------------------------------------------------

    "microsoft azure": "Azure",
    "ms azure": "Azure",
    "native azure": "Azure",
    "azure cloud": "Azure",
    "cloud azure": "Azure",

    # --------------------------------------------------------
    # NLP
    # --------------------------------------------------------

    "natural language processing": "NLP",
    "nlp models": "NLP",
    "nlp generative": "NLP",

    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    "microsoft excel": "Excel",
    "ms excel": "Excel",
    "ms - excel": "Excel",
    "advance excel": "Excel",
    "advanced excel": "Excel",
    "advanced ms excel": "Excel",
    "basic excel": "Excel",
    "excel macros": "Excel",
    "excel vba": "Excel",

    # --------------------------------------------------------
    # COMMON TECHNICAL VARIANTS
    # --------------------------------------------------------

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

    "typescript": "TypeScript"
}


# ============================================================
# GENERIC WORDS / PHRASES
#
# These should NOT be treated as standalone skills.
# ============================================================

GENERIC_TERMS = {

    "team",
    "teams",
    "technical",
    "industry",
    "qualification",
    "education",
    "software",
    "develop",
    "development",
    "computer",
    "science",
    "standards",
    "analysis",
    "technology",
    "problem",
    "activities",
    "identify",
    "english",
    "financial",
    "training",
    "application",
    "job description",
    "requirements",
    "experience",
    "knowledge",
    "skills",
    "skill",
    "work",
    "working",
    "support",
    "process",
    "processes",
    "management",
    "manage",
    "manager",
    "lead",
    "leadership",
    "senior",
    "junior",
    "executive",
    "associate",
    "professional",
    "responsibility",
    "responsibilities",
    "good communication",
    "excellent communication",
    "communication",
    "strong",
    "high",
    "performance",
    "quality",
    "operations",
    "office",
    "company",
    "clients",
    "customer",
    "customers",
    "service",
    "services",
    "field",
    "domain",
    "project",
    "projects",
    "delivery",
    "documentation",
    "planning",
    "relationship",
    "relationships",
    "requirements",
    "tools",
    "tool",
    "system",
    "systems",
    "computer science",
    "functional",
    "financial",
    "activities",
    "identify",
    "cross",
    "selling",
    "sales",
    "shift",
    "schedule",
    "adherence"
}


# ============================================================
# DESCRIPTION / LIST PHRASES
# ============================================================

DESCRIPTION_PATTERNS = [

    r"\b\d+\s*(years?|yrs?)\b",

    r"\b\d+\s*\+\s*(years?|yrs?)\b",

    r"\b\d+\s*(months?)\b",

    r"\bpass\s*out\b",

    r"\b\d+(st|nd|rd|th)\b",

    r"\b\d+\s*lpa\b",

    r"\bage\s*\d+\b",

    r"\b\d+\s*to\s*\d+\b",

    r"\bexcellent\s+\w+\s+skills\b",

    r"\bgood\s+\w+\s+skills\b",

    r"\bstrong\s+\w+\s+skills\b",

    r"\bproficiency\s+in\b",

    r"\bfamiliar\s+with\b",

    r"\bexperience\s+in\b",

    r"\bknowledge\s+of\b",

    r"\bresponsible\s+for\b",

    r"\bability\s+to\b",

    r"\bshould\s+have\b",

    r"\bmust\s+have\b"
]


# ============================================================
# SPECIAL PHRASES THAT ARE NOT STANDALONE SKILLS
# ============================================================

NON_SKILL_PHRASES = {

    "2 way matching",
    "2 end-to-end implementations",
    "2 hfM implementations",
    "1st line manager",
    "1st party collection",
    "1099 recruitment",
    "2025 pass out",
    "25 lpa",
    "27+ age",
    "2 wheeler sales",
    "2 wheeler part sales",
    "2-wheeler",
    "2/4 wheeler"
}


# ============================================================
# FUNCTION: DESCRIPTION CHECK
# ============================================================

def looks_like_description(skill):

    value = normalized_lower(skill)

    for pattern in DESCRIPTION_PATTERNS:

        if re.search(
            pattern,
            value,
            flags=re.IGNORECASE
        ):

            return True

    return False


# ============================================================
# FUNCTION: SHORT SKILL CHECK
# ============================================================

def is_invalid_short_skill(skill):

    value = normalized_lower(skill)

    if len(value) <= 1:

        return True

    if len(value) <= 3:

        if value in ALLOWED_SHORT_SKILLS:

            return False

        # Single letters are not accepted
        if re.fullmatch(
            r"[a-z]",
            value
        ):

            return True

        # Numeric/code fragments
        if re.search(
            r"\d",
            value
        ):

            return True

        # Two/three-letter random fragments
        if re.fullmatch(
            r"[a-z]{2,3}",
            value
        ):

            return True

    return False


# ============================================================
# FUNCTION: CANONICAL NAME
# ============================================================

def get_canonical_name(skill):

    value = normalized_lower(skill)

    if value in CANONICAL_ALIASES:

        return CANONICAL_ALIASES[value]

    return normalize_text(skill)


# ============================================================
# LOAD V10
# ============================================================

print("=" * 70)
print("NLP DICTIONARY CLEANING - V11")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Input skills: {len(df):,}"
)


# ============================================================
# PROCESS
# ============================================================

accepted = []

rejected = []

seen_canonical = set()

reason_counts = {}


for _, row in df.iterrows():

    skill_id = int(
        row["skill_id"]
    )

    original_skill = normalize_text(
        row["skill_name"]
    )

    if not original_skill:

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "empty"
            }
        )

        reason_counts["empty"] = (
            reason_counts.get("empty", 0) + 1
        )

        continue


    lower_skill = normalized_lower(
        original_skill
    )


    # --------------------------------------------------------
    # SPECIAL NON-SKILL PHRASES
    # --------------------------------------------------------

    if lower_skill in {
        normalized_lower(x)
        for x in NON_SKILL_PHRASES
    }:

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "non_skill_phrase"
            }
        )

        reason_counts[
            "non_skill_phrase"
        ] = (
            reason_counts.get(
                "non_skill_phrase",
                0
            ) + 1
        )

        continue


    # --------------------------------------------------------
    # SHORT SKILL CHECK
    # --------------------------------------------------------

    if is_invalid_short_skill(
        original_skill
    ):

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "invalid_short_skill"
            }
        )

        reason_counts[
            "invalid_short_skill"
        ] = (
            reason_counts.get(
                "invalid_short_skill",
                0
            ) + 1
        )

        continue


    # --------------------------------------------------------
    # GENERIC TERM
    # --------------------------------------------------------

    if lower_skill in GENERIC_TERMS:

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "generic"
            }
        )

        reason_counts[
            "generic"
        ] = (
            reason_counts.get(
                "generic",
                0
            ) + 1
        )

        continue


    # --------------------------------------------------------
    # DESCRIPTION PHRASE
    # --------------------------------------------------------

    if looks_like_description(
        original_skill
    ):

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "description_phrase"
            }
        )

        reason_counts[
            "description_phrase"
        ] = (
            reason_counts.get(
                "description_phrase",
                0
            ) + 1
        )

        continue


    # --------------------------------------------------------
    # CANONICAL NAME
    # --------------------------------------------------------

    canonical_name = get_canonical_name(
        original_skill
    )

    canonical_key = normalized_lower(
        canonical_name
    )


    # --------------------------------------------------------
    # DUPLICATE CANONICAL SKILL
    # --------------------------------------------------------

    if canonical_key in seen_canonical:

        rejected.append(
            {
                "skill_id": skill_id,
                "skill_name": original_skill,
                "reason": "duplicate_canonical_skill"
            }
        )

        reason_counts[
            "duplicate_canonical_skill"
        ] = (
            reason_counts.get(
                "duplicate_canonical_skill",
                0
            ) + 1
        )

        continue


    seen_canonical.add(
        canonical_key
    )


    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    accepted.append(
        {
            "skill_id": skill_id,
            "skill_name": original_skill,
            "canonical_skill_name": canonical_name
        }
    )


# ============================================================
# SAVE
# ============================================================

accepted_df = pd.DataFrame(
    accepted
)

rejected_df = pd.DataFrame(
    rejected
)


accepted_df.to_csv(
    OUTPUT_FILE,
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

print()
print("=" * 70)
print("V11 CLEANING COMPLETED")
print("=" * 70)

print(
    f"Original skills : {len(df):,}"
)

print(
    f"Accepted skills : {len(accepted_df):,}"
)

print(
    f"Rejected skills : {len(rejected_df):,}"
)


print()
print("REJECTION REASONS:")

for reason, count in sorted(
    reason_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"  {reason}: {count:,}"
    )


# ============================================================
# CANONICAL CHECK
# ============================================================

print()
print("=" * 70)
print("CANONICAL TECHNICAL SKILL CHECK")
print("=" * 70)

technical_checks = [
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
    "Git"
]


for skill in technical_checks:

    found = (
        accepted_df[
            "canonical_skill_name"
        ]
        .astype(str)
        .str.lower()
        .eq(
            skill.lower()
        )
        .any()
    )

    status = (
        "PRESENT"
        if found
        else "NOT PRESENT"
    )

    print(
        f"{skill}: {status}"
    )


# ============================================================
# GENERIC CHECK
# ============================================================

print()
print("=" * 70)
print("GENERIC TERM CHECK")
print("=" * 70)

remaining_generic = []

for skill in accepted_df[
    "canonical_skill_name"
].astype(str):

    if normalized_lower(skill) in GENERIC_TERMS:

        remaining_generic.append(
            skill
        )


if remaining_generic:

    print(
        "WARNING - generic terms remain:"
    )

    for skill in sorted(
        set(remaining_generic)
    ):

        print(
            f"  {skill}"
        )

else:

    print(
        "No explicitly blocked generic terms remain."
    )


# ============================================================
# CANONICAL ALIAS CHECK
# ============================================================

print()
print("=" * 70)
print("CANONICAL ALIAS CHECK")
print("=" * 70)

for source, target in CANONICAL_ALIASES.items():

    matches = accepted_df[
        accepted_df[
            "canonical_skill_name"
        ]
        .astype(str)
        .str.lower()
        .eq(
            target.lower()
        )
    ]

    if len(matches) > 0:

        print(
            f"{source} -> {target}"
        )


# ============================================================
# OUTPUT
# ============================================================

print()
print("=" * 70)

print(
    "Clean V11 dictionary:"
)

print(
    OUTPUT_FILE
)

print()
print(
    "Rejected V11 dictionary:"
)

print(
    REJECTED_FILE
)

print()
print(
    "PostgreSQL was NOT modified."
)

print("=" * 70)