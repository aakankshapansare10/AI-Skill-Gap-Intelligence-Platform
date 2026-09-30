# ============================================================
# DATABASE CONNECTION
# AI Skill Gap Intelligence Platform
# ============================================================

import psycopg2


# ------------------------------------------------------------
# PostgreSQL configuration
# ------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "skill_gap_db",
    "user": "postgres",
    "password": "Antarahp@2005"
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