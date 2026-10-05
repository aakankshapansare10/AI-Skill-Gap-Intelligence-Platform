import pandas as pd
import re
from collections import Counter

# ============================================================
# PATHS
# ============================================================

INPUT_FILE = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform\data\processed\skills.csv"

OUTPUT_CLEAN = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform\data\processed\skills_dictionary_clean_v7.csv"

OUTPUT_REJECTED = r"E:\ty\pbl\AI_skill_gaps_intelligence_platform\data\processed\skills_dictionary_rejected_v7.csv"


# ============================================================
# EXPLICITLY ALLOWED SHORT / TECHNICAL SKILLS
# ============================================================

ALLOWED_SHORT_SKILLS = {
    "2D", "3D", "4G", "5G",
    "A+", "A/P", "A/R",
    "API", "ATS", "AWS",
    "BI",
    "C#", "C+", "C++", "C&B", "C&I",
    "CAD", "CAE", "CAM", "CPU", "CRM", "CSS", "CV",
    "DB2", "DNS",
    "EC2", "EDA", "ELT", "ERP", "ES6", "ETL",
    "F#", "F&A", "F&B", "F&D", "F&F", "F&O",
    "GA4", "GPU",
    "HCM", "HL7", "HR",
    "I&C", "I/O", "IAM", "IOS",
    "KPI",
    "L&D",
    "M&A", "M.e", "Mac",
    "n8n",
    "O&M",
    "P&L", "P&c", "PCB", "PHP", "PLC",
    "QA",
    "R&D", "RAM", "RF", "ROI",
    "S&G", "S&P", "SAP", "SAS", "SDK", "SEM", "SEO", "SQL", "SSH", "SSL",
    "T&D", "T&E", "TCP",
    "UI", "UDP", "UX",
    "VBA", "VM", "VPN",
    "X++", "XML"
}


# ============================================================
# GENERIC / NON-SKILL WORDS FOUND IN V6
# ============================================================

GENERIC_TERMS = {
    "strong",
    "good",
    "high",
    "maintain",
    "maintaining",
    "hiring",
    "problem",
    "problems",
    "cross",
    "selling",
    "sell",
    "year",
    "years",
    "written",
    "complex",
    "join",
    "targets",
    "target",
    "equivalent",
    "delivery",
    "international",
    "skills",
    "skill",
    "experienced",
    "experience",
    "prior",
    "required",
    "requirement",
    "requirements",
    "ability",
    "knowledge",
    "candidate",
    "candidates",
    "role",
    "roles",
    "work",
    "working",
    "people",
    "team",
    "teams",
    "management",
    "manager",
    "support",
    "communication",
    "sales",
    "customer",
    "customers",
    "client",
    "clients",
    "business",
    "technical",
    "technology",
    "software",
    "application",
    "applications",
    "development",
    "develop",
    "developing",
    "planning",
    "documentation",
    "education",
    "qualification",
    "qualifications",
    "responsibility",
    "responsibilities",
    "professional",
    "organization",
    "organization",
    "organization's",
    "excellent",
    "best",
    "prior",
    "life",
    "area",
    "direct",
    "large",
    "make",
    "resolve",
    "resolution",
    "improvement",
    "plans",
    "plan",
    "benefits",
    "concepts",
    "staff",
    "site",
    "power",
    "advantage",
    "processing",
    "coordination",
    "relationship",
    "relationship manager",
    "account",
    "records",
    "report",
    "voice",
    "post",
    "home",
    "generation",
    "lead",
    "leads",
    "organization",
    "strategic",
    "strategy",
    "engagement",
    "manufacturing",
    "solution",
    "solutions",
    "control",
    "production",
    "test",
    "testing",
    "frameworks",
    "framework",
    "programming",
    "designing",
    "design",
    "digital",
    "enterprise",
    "methodologies",
    "methodology",
    "large",
    "area",
    "field",
    "industry",
    "service",
    "services"
}


# ============================================================
# DESCRIPTION / SENTENCE DETECTION
# ============================================================

SENTENCE_WORDS = {
    "and", "or", "with", "for", "from", "into", "using",
    "have", "has", "had", "will", "can", "should",
    "must", "need", "needs", "required", "preferred",
    "responsible", "responsibilities", "knowledge",
    "experience", "ability", "excellent", "good", "strong"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(text):
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalized_key(text):
    text = normalize(text).lower()
    return text


def is_short_skill(skill):
    """
    Handle short skills carefully.
    Preserve known technical abbreviations.
    """
    if skill in ALLOWED_SHORT_SKILLS:
        return False

    if len(skill) <= 1:
        return True

    if len(skill) <= 3:

        # pure alphabetic short strings are rejected
        # unless explicitly allowed above
        if skill.isalpha():
            return True

        # short strings containing digits are rejected
        # unless explicitly allowed
        if any(ch.isdigit() for ch in skill):
            return True

    return False


def looks_like_sentence(skill):
    text = skill.strip()

    words = text.split()

    # Very long phrases are unlikely to be a clean skill
    if len(words) >= 12:
        return True

    # Multiple sentence-like separators
    if text.count(",") >= 2:
        return True

    if text.count(";") >= 1:
        return True

    if text.count(":") >= 2:
        return True

    # Sentence ending punctuation
    if text.endswith(".") and len(text) > 3:
        return True

    lower_words = {w.lower().strip(".,:;()[]") for w in words}

    # Multiple sentence words indicate description text
    sentence_hits = lower_words.intersection(SENTENCE_WORDS)

    if len(words) >= 5 and len(sentence_hits) >= 2:
        return True

    # Common description pattern
    if len(words) >= 6 and any(
        phrase in text.lower()
        for phrase in [
            "years of experience",
            "year of experience",
            "good communication",
            "strong communication",
            "responsible for",
            "ability to",
            "knowledge of",
            "experience in",
            "experience with",
            "should have",
            "must have",
            "will be",
            "looking for"
        ]
    ):
        return True

    return False


def looks_like_experience_or_qualification(skill):
    text = skill.lower().strip()

    patterns = [
        r"\b\d+\+?\s*years?\b",
        r"\b\d+\s*yrs?\b",
        r"\byears?\s+of\s+experience\b",
        r"\byear\s+experience\b",
        r"\b\d+\s*-\s*\d+\s*years?\b",
        r"\bgraduat(e|ion)\b",
        r"\bpost.?graduate\b",
        r"\bunder.?graduate\b",
        r"\bdegree\b",
        r"\bdiploma\b",
        r"\bqualification\b",
        r"\bpass.?out\b",
        r"\bfresher(s)?\b",
        r"\bexperience\b"
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def looks_like_noise(skill):
    text = skill.strip()

    # excessive special characters
    special_count = len(re.findall(r"[^A-Za-z0-9+#&./' -]", text))

    if len(text) > 0 and special_count / len(text) > 0.25:
        return True

    # hashtags / markdown-like fragments
    if text.startswith("#"):
        return True

    # URLs / email-like strings
    if "http://" in text.lower() or "https://" in text.lower():
        return True

    if "@" in text:
        return True

    return False


# ============================================================
# LOAD RAW SKILLS
# ============================================================

print("=" * 70)
print("NLP DICTIONARY CLEANING - V7")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal skills: {len(df):,}")


# ============================================================
# PROCESS
# ============================================================

accepted = []
rejected = []

seen_normalized = set()

reason_counter = Counter()

for _, row in df.iterrows():

    skill_id = int(row["skill_id"])
    raw_skill = row["skill_name"]

    if pd.isna(raw_skill):
        rejected.append({
            "skill_id": skill_id,
            "skill_name": raw_skill,
            "reason": "empty_skill"
        })
        reason_counter["empty_skill"] += 1
        continue

    skill = normalize(raw_skill)

    if not skill:
        rejected.append({
            "skill_id": skill_id,
            "skill_name": raw_skill,
            "reason": "empty_skill"
        })
        reason_counter["empty_skill"] += 1
        continue

    key = normalized_key(skill)

    # --------------------------------------------------------
    # Duplicate normalized skill
    # --------------------------------------------------------

    if key in seen_normalized:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "duplicate_normalized_skill"
        })

        reason_counter["duplicate_normalized_skill"] += 1
        continue

    seen_normalized.add(key)

    # --------------------------------------------------------
    # Explicit generic terms
    # --------------------------------------------------------

    if key in GENERIC_TERMS:

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "generic"
        })

        reason_counter["generic"] += 1
        continue

    # --------------------------------------------------------
    # Short skill
    # --------------------------------------------------------

    if is_short_skill(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "invalid_short_skill"
        })

        reason_counter["invalid_short_skill"] += 1
        continue

    # --------------------------------------------------------
    # Experience / qualification
    # --------------------------------------------------------

    if looks_like_experience_or_qualification(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "experience_or_qualification"
        })

        reason_counter["experience_or_qualification"] += 1
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

        reason_counter["sentence_or_description"] += 1
        continue

    # --------------------------------------------------------
    # Noise
    # --------------------------------------------------------

    if looks_like_noise(skill):

        rejected.append({
            "skill_id": skill_id,
            "skill_name": skill,
            "reason": "special_character_noise"
        })

        reason_counter["special_character_noise"] += 1
        continue

    # --------------------------------------------------------
    # Accept
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
    encoding="utf-8-sig"
)

rejected_df.to_csv(
    OUTPUT_REJECTED,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 70)
print("V7 RESULTS")
print("=" * 70)

print(f"\nOriginal skills: {len(df):,}")
print(f"Accepted skills : {len(clean_df):,}")
print(f"Rejected skills : {len(rejected_df):,}")

print("\nRejection reasons:")

for reason, count in reason_counter.most_common():
    print(f"  {reason}: {count:,}")


# ============================================================
# IMPORTANT TECHNICAL SKILL CHECK
# ============================================================

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
    "Git"
]

clean_lower = {
    normalized_key(x)
    for x in clean_df["skill_name"].tolist()
}

print("\n" + "=" * 70)
print("TECHNICAL DICTIONARY CHECK")
print("=" * 70)

for skill in technical_skills:

    if normalized_key(skill) in clean_lower:
        print(f"{skill:20} PRESENT")
    else:
        print(f"{skill:20} NOT IN CLEAN DICTIONARY")


# ============================================================
# CHECK SUSPICIOUS TERMS
# ============================================================

print("\n" + "=" * 70)
print("GENERIC TERM CHECK")
print("=" * 70)

for term in sorted(GENERIC_TERMS):

    if term in clean_lower:
        print("STILL PRESENT:", term)


# ============================================================
# SHORT SKILLS
# ============================================================

print("\n" + "=" * 70)
print("SHORT SKILLS <= 3 CHARACTERS")
print("=" * 70)

short_df = clean_df[
    clean_df["skill_name"].astype(str).str.len() <= 3
]

print(f"Remaining short skills: {len(short_df):,}")

if len(short_df) > 0:
    for skill in short_df["skill_name"].tolist():
        print(skill)


print("\n" + "=" * 70)
print("FILES CREATED")
print("=" * 70)

print(OUTPUT_CLEAN)
print(OUTPUT_REJECTED)

print("\nV7 dictionary cleaning completed.")
print("PostgreSQL was NOT modified.")
print("=" * 70)