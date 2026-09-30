import pandas as pd

SKILL_INPUT_PATH = "data/processed/normalized_job_skills.csv"
DOMAIN_INPUT_PATH = "data/processed/job_domains.csv"

TOP_SKILLS_OUTPUT = "data/processed/skill_demand.csv"
DOMAIN_SKILLS_OUTPUT = "data/processed/domain_skill_demand.csv"

print("=" * 70)
print("AI SKILL GAP INTELLIGENCE PLATFORM")
print("STEP 7 - SKILL DEMAND ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

skills_df = pd.read_csv(SKILL_INPUT_PATH)
domains_df = pd.read_csv(DOMAIN_INPUT_PATH)

print("\nInput datasets loaded successfully.")

print(f"Job-skill records: {len(skills_df):,}")
print(f"Domain records: {len(domains_df):,}")

# --------------------------------------------------
# CHECK REQUIRED COLUMNS
# --------------------------------------------------

required_skill_columns = [
    "jobId",
    "normalized_skill"
]

required_domain_columns = [
    "jobId",
    "domain"
]

for column in required_skill_columns:

    if column not in skills_df.columns:
        raise ValueError(
            f"Missing column in normalized skill dataset: {column}"
        )

for column in required_domain_columns:

    if column not in domains_df.columns:
        raise ValueError(
            f"Missing column in domain dataset: {column}"
        )

# --------------------------------------------------
# REMOVE INVALID VALUES
# --------------------------------------------------

skills_df = skills_df.dropna(
    subset=["jobId", "normalized_skill"]
)

domains_df = domains_df.dropna(
    subset=["jobId", "domain"]
)

skills_df["normalized_skill"] = (
    skills_df["normalized_skill"]
    .astype(str)
    .str.strip()
)

domains_df["domain"] = (
    domains_df["domain"]
    .astype(str)
    .str.strip()
)

skills_df = skills_df[
    skills_df["normalized_skill"] != ""
]

domains_df = domains_df[
    domains_df["domain"] != ""
]

# --------------------------------------------------
# REMOVE DUPLICATE JOB-SKILL RELATIONSHIPS
# --------------------------------------------------

skills_df = skills_df.drop_duplicates(
    subset=["jobId", "normalized_skill"]
)

print(
    f"\nUnique job-skill relationships: "
    f"{len(skills_df):,}"
)

# --------------------------------------------------
# OVERALL SKILL DEMAND
# --------------------------------------------------

print("\n" + "=" * 70)
print("OVERALL SKILL DEMAND")
print("=" * 70)

skill_demand = (
    skills_df
    .groupby("normalized_skill")
    .agg(
        job_count=("jobId", "nunique")
    )
    .reset_index()
)

total_jobs = skills_df["jobId"].nunique()

skill_demand["demand_percentage"] = (
    skill_demand["job_count"] / total_jobs * 100
).round(2)

skill_demand = skill_demand.sort_values(
    "job_count",
    ascending=False
)

skill_demand = skill_demand.reset_index(
    drop=True
)

skill_demand.insert(
    0,
    "rank",
    range(1, len(skill_demand) + 1)
)

# Save overall skill demand

skill_demand.to_csv(
    TOP_SKILLS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nTop 30 demanded skills:")

print(
    skill_demand
    .head(30)
    .to_string(index=False)
)

# --------------------------------------------------
# DOMAIN + SKILL MERGE
# --------------------------------------------------

print("\n" + "=" * 70)
print("DOMAIN-SPECIFIC SKILL DEMAND")
print("=" * 70)

job_skill_domain = skills_df.merge(
    domains_df[
        [
            "jobId",
            "domain"
        ]
    ],
    on="jobId",
    how="left"
)

# Remove jobs without domain

job_skill_domain = job_skill_domain.dropna(
    subset=["domain"]
)

# --------------------------------------------------
# DOMAIN SKILL COUNTS
# --------------------------------------------------

domain_skill_demand = (
    job_skill_domain
    .groupby(
        [
            "domain",
            "normalized_skill"
        ]
    )
    .agg(
        job_count=("jobId", "nunique")
    )
    .reset_index()
)

# --------------------------------------------------
# NUMBER OF JOBS PER DOMAIN
# --------------------------------------------------

domain_job_counts = (
    domains_df
    .groupby("domain")
    .agg(
        total_jobs=("jobId", "nunique")
    )
    .reset_index()
)

domain_skill_demand = domain_skill_demand.merge(
    domain_job_counts,
    on="domain",
    how="left"
)

domain_skill_demand["demand_percentage"] = (
    domain_skill_demand["job_count"]
    /
    domain_skill_demand["total_jobs"]
    * 100
).round(2)

# --------------------------------------------------
# RANK SKILLS WITHIN EACH DOMAIN
# --------------------------------------------------

domain_skill_demand = (
    domain_skill_demand
    .sort_values(
        [
            "domain",
            "job_count"
        ],
        ascending=[
            True,
            False
        ]
    )
)

domain_skill_demand["rank"] = (
    domain_skill_demand
    .groupby("domain")
    .cumcount()
    + 1
)

domain_skill_demand = domain_skill_demand[
    [
        "domain",
        "rank",
        "normalized_skill",
        "job_count",
        "total_jobs",
        "demand_percentage"
    ]
]

domain_skill_demand.to_csv(
    DOMAIN_SKILLS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# DISPLAY TOP SKILLS BY DOMAIN
# --------------------------------------------------

domains = (
    domain_skill_demand["domain"]
    .dropna()
    .unique()
)

for domain in domains:

    print("\n" + "-" * 70)

    print(
        f"Top skills for: {domain}"
    )

    print("-" * 70)

    domain_result = domain_skill_demand[
        domain_skill_demand["domain"] == domain
    ]

    print(
        domain_result
        .head(10)
        .to_string(index=False)
    )

# --------------------------------------------------
# DOMAIN SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("DOMAIN SUMMARY")
print("=" * 70)

domain_summary = (
    domains_df
    .groupby("domain")
    .agg(
        job_count=("jobId", "nunique")
    )
    .reset_index()
    .sort_values(
        "job_count",
        ascending=False
    )
)

domain_summary["percentage"] = (
    domain_summary["job_count"]
    /
    domain_summary["job_count"].sum()
    * 100
).round(2)

print(
    domain_summary.to_string(index=False)
)

# --------------------------------------------------
# FINAL RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("STEP 7 COMPLETED")
print("=" * 70)

print(
    f"Unique skills analyzed: "
    f"{skill_demand['normalized_skill'].nunique():,}"
)

print(
    f"Domains analyzed: "
    f"{domain_summary['domain'].nunique():,}"
)

print("\nFiles created:")

print(
    TOP_SKILLS_OUTPUT
)

print(
    DOMAIN_SKILLS_OUTPUT
)

print("\nSkill demand analysis completed successfully.")

print("=" * 70)