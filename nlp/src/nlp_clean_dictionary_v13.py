import os
import re
import pandas as pd


# ============================================================
# V13 FINAL NLP DICTIONARY CLEANER
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v12.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v13.csv"
)

REJECTED_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_rejected_v13.csv"
)


# ============================================================
# REQUIRED TECHNICAL SKILLS
# ============================================================

REQUIRED_TECHNICAL_SKILLS = [
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


# ============================================================
# LEGITIMATE DOMAIN SKILLS
# ============================================================

PROTECTED_SKILLS = {
    x.lower()
    for x in REQUIRED_TECHNICAL_SKILLS
}

PROTECTED_SKILLS.update({
    "typescript",
    "natural language processing",
    "accounting",
    "programming",
    "security",
    "automation",
    "analytics",
    "business development",
    "customer service",
    "cross-functional",
    "strategy",
    "research",
    "database",
    "sales",
    "marketing",
    "sap",
    "agile",
    "testing",
    "frameworks",
    "design",
    "digital",
    "health",
    "learning",
    "voice",
})


# ============================================================
# CLEAR NON-SKILL TERMS
# ============================================================

GENERIC_TERMS = {
    "naukri",
    "travel",
    "part",
    "resolve",
    "review",
    "dynamic",
    "assistant",
    "execution",
    "platform",
    "policies",
    "tasks",
    "local",
    "large",
    "core",
    "focus",
    "microsoft",
    "bangalore",
    "leads",
    "sales manager",
    "sales executive",
    "bank",
    "accounts",
    "certifications",
    "designing",
    "strategic",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(text):
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def key(text):
    return normalize(text).lower()


def is_sentence(text):

    if len(text) > 150:
        return True

    if len(text.split()) >= 15:
        return True

    return False


def is_numeric_noise(text):

    value = text.lower().strip()

    patterns = [
        r"^\d+\s*lpa$",
        r"^\d+\+\s*age$",
        r"^\d+th\s+pass$",
        r"^\d+th$",
        r"^\d+\s+class$",
        r"^\d+\s+to\s+\d+$",
        r"^\d+\s*-\s*\d+\s*bucket$",
        r"^\d+\s+end-to-end",
        r"^\d+\s+production",
        r"^\d+\s+talent",
        r"^\d+\+\s*yrs",
        r"^\d+\+\s*years",
    ]

    for pattern in patterns:

        if re.search(pattern, value):
            return True

    return False


# ============================================================
# LOAD V12
# ============================================================

print("=" * 70)
print("V13 FINAL NLP DICTIONARY CLEANING")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(
    f"\nOriginal dictionary rows: {len(df):,}"
)


# ============================================================
# PROCESS
# ============================================================

accepted = []
rejected = []

seen = set()

for _, row in df.iterrows():

    original = str(
        row["skill_name"]
    ).strip()

    if not original:

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "empty_skill"
        })

        continue

    skill = normalize(original)
    skill_key = key(skill)


    # --------------------------------------------------------
    # REQUIRED TECHNICAL SKILLS
    # --------------------------------------------------------

    if skill_key in PROTECTED_SKILLS:

        accepted.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "canonical_skill_name": skill
        })

        seen.add(skill_key)

        continue


    # --------------------------------------------------------
    # DUPLICATE
    # --------------------------------------------------------

    if skill_key in seen:

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "duplicate_canonical_skill"
        })

        continue


    # --------------------------------------------------------
    # ONE CHARACTER NOISE
    # --------------------------------------------------------

    if len(skill_key) == 1 and skill_key.isalpha():

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "invalid_short_skill"
        })

        continue


    # --------------------------------------------------------
    # NUMERIC NOISE
    # --------------------------------------------------------

    if is_numeric_noise(skill):

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "numeric_or_list_noise"
        })

        continue


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    if is_sentence(skill):

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "description_phrase"
        })

        continue


    # --------------------------------------------------------
    # GENERIC TERMS
    # --------------------------------------------------------

    if skill_key in GENERIC_TERMS:

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "generic"
        })

        continue


    # --------------------------------------------------------
    # LOCATIONS
    # --------------------------------------------------------

    if skill_key in {
        "bangalore",
        "mumbai",
        "delhi",
        "pune",
        "hyderabad",
        "chennai",
        "kolkata",
        "noida",
        "gurgaon",
    }:

        rejected.append({
            "skill_id": row["skill_id"],
            "skill_name": original,
            "reason": "location"
        })

        continue


    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    accepted.append({
        "skill_id": row["skill_id"],
        "skill_name": original,
        "canonical_skill_name": skill
    })

    seen.add(skill_key)


# ============================================================
# ADD MISSING REQUIRED TECHNICAL SKILLS
# ============================================================

existing_technical = {
    key(x)
    for x in accepted
    for _ in [0]
    if False
}

existing_technical = {
    key(row["canonical_skill_name"])
    for row in accepted
}

next_skill_id = 1000000

for technical_skill in REQUIRED_TECHNICAL_SKILLS:

    technical_key = key(technical_skill)

    if technical_key not in existing_technical:

        accepted.append({
            "skill_id": next_skill_id,
            "skill_name": technical_skill,
            "canonical_skill_name": technical_skill
        })

        existing_technical.add(
            technical_key
        )

        next_skill_id += 1

        print(
            f"Added missing technical skill: "
            f"{technical_skill}"
        )


# ============================================================
# DATAFRAMES
# ============================================================

clean_df = pd.DataFrame(
    accepted
)

rejected_df = pd.DataFrame(
    rejected
)


# ============================================================
# SAVE
# ============================================================

clean_df.to_csv(
    OUTPUT_FILE,
    index=False
)

rejected_df.to_csv(
    REJECTED_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 70)
print("V13 FINAL CLEANING COMPLETED")
print("=" * 70)

print(
    f"Original: {len(df):,}"
)

print(
    f"Accepted: {len(clean_df):,}"
)

print(
    f"Rejected: {len(rejected_df):,}"
)


# ============================================================
# TECHNICAL CHECK
# ============================================================

print("\nTechnical skill check:")

for skill in REQUIRED_TECHNICAL_SKILLS:

    found = (
        clean_df[
            "canonical_skill_name"
        ]
        .astype(str)
        .str.lower()
        .eq(skill.lower())
        .any()
    )

    print(
        f"{skill}: "
        f"{'PRESENT' if found else 'MISSING'}"
    )


# ============================================================
# SUSPICIOUS TERM CHECK
# ============================================================

print("\nV13 suspicious term check:")

check_terms = [
    "VOICE",
    "Digital",
    "Execution",
    "Assistant",
    "Test",
    "Learning",
    "platform",
    "Naukri",
    "Frameworks",
    "Travel",
    "Part",
    "Health",
    "Programming",
    "Dynamic",
    "Review",
    "Resolve",
    "BANK",
    "ACCOUNTING",
    "ACCOUNTS",
]

for term in check_terms:

    found = (
        clean_df[
            "canonical_skill_name"
        ]
        .astype(str)
        .str.lower()
        .eq(term.lower())
        .any()
    )

    print(
        f"{term}: "
        f"{'PRESENT' if found else 'REMOVED'}"
    )


# ============================================================
# OUTPUT
# ============================================================

print("\nOutput files:")
print(OUTPUT_FILE)
print(REJECTED_FILE)

print(
    "\nPostgreSQL was NOT modified."
)

print("=" * 70)