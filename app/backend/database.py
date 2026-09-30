# ============================================================
# DATABASE CONNECTION
# AI Skill Gap Intelligence Platform
# ============================================================

import os
import psycopg2
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# ------------------------------------------------------------
# PostgreSQL configuration
# ------------------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


# ------------------------------------------------------------
# Get database connection
# ------------------------------------------------------------

def get_connection():

    try:

        connection = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        return connection

    except Exception as e:

        print("Database connection error:", e)

        return None