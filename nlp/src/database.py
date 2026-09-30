from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ============================================================
# POSTGRESQL DATABASE CONFIGURATION
# ============================================================

DB_USER = "postgres"
DB_PASSWORD = "Postgres@5100"
DB_HOST = "127.0.0.1"
DB_PORT = "5100"
DB_NAME = "ai_skill_gaps"

# Encode special characters in password
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)

# PostgreSQL connection URL
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{ENCODED_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

def get_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )