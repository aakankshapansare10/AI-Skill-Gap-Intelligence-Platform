from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

import os

DB_USER = "postgres"
DB_PASSWORD = "Postgres@5100"
DB_HOST = "localhost"
DB_PORT = "5100"
DB_NAME = "ai_skill_gaps"
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("PostgreSQL connection successful!")
        print("Test result:", result.scalar())


def load_ml_job_skills():
    query = """
        SELECT
            job_id,
            job_title,
            skill_id,
            skill_name
        FROM ml_job_skills
    """

    return pd.read_sql(query, engine)


if __name__ == "__main__":

    print("=" * 60)
    print("TESTING POSTGRESQL CONNECTION")
    print("=" * 60)

    test_connection()

    print()
    print("=" * 60)
    print("LOADING NLP JOB-SKILL DATA")
    print("=" * 60)

    df = load_ml_job_skills()

    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    print()
    print("First 10 rows:")
    print(df.head(10).to_string(index=False))