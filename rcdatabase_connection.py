[1mdiff --git a/ml/src/database_connection.py b/ml/src/database_connection.py[m
[1mnew file mode 100644[m
[1mindex 0000000..7b6b940[m
[1m--- /dev/null[m
[1m+++ b/ml/src/database_connection.py[m
[36m@@ -0,0 +1,61 @@[m
[32m+[m[32mfrom sqlalchemy import create_engine, text[m
[32m+[m[32mimport pandas as pd[m
[32m+[m[32mfrom urllib.parse import quote_plus[m
[32m+[m
[32m+[m[32mDB_USER = "postgres"[m
[32m+[m[32mDB_PASSWORD = "Postgres@5100"[m
[32m+[m[32mDB_HOST = "localhost"[m
[32m+[m[32mDB_PORT = "5100"[m
[32m+[m[32mDB_NAME = "ai_skill_gaps"[m
[32m+[m
[32m+[m[32mencoded_password = quote_plus(DB_PASSWORD)[m
[32m+[m
[32m+[m[32mDATABASE_URL = ([m
[32m+[m[32m    f"postgresql+psycopg2://{DB_USER}:{encoded_password}"[m
[32m+[m[32m    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mengine = create_engine(DATABASE_URL)[m
[32m+[m
[32m+[m
[32m+[m[32mdef test_connection():[m
[32m+[m[32m    with engine.connect() as connection:[m
[32m+[m[32m        result = connection.execute(text("SELECT 1"))[m
[32m+[m[32m        print("PostgreSQL connection successful!")[m
[32m+[m[32m        print("Test result:", result.scalar())[m
[32m+[m
[32m+[m
[32m+[m[32mdef load_ml_job_skills():[m
[32m+[m[32m    query = """[m
[32m+[m[32m        SELECT[m
[32m+[m[32m            job_id,[m
[32m+[m[32m            job_title,[m
[32m+[m[32m            skill_id,[m
[32m+[m[32m            skill_name[m
[32m+[m[32m        FROM ml_job_skills[m
[32m+[m[32m    """[m
[32m+[m
[32m+[m[32m    return pd.read_sql(query, engine)[m
[32m+[m
[32m+[m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m
[32m+[m[32m    print("=" * 60)[m
[32m+[m[32m    print("TESTING POSTGRESQL CONNECTION")[m
[32m+[m[32m    print("=" * 60)[m
[32m+[m
[32m+[m[32m    test_connection()[m
[32m+[m
[32m+[m[32m    print()[m
[32m+[m[32m    print("=" * 60)[m
[32m+[m[32m    print("LOADING NLP JOB-SKILL DATA")[m
[32m+[m[32m    print("=" * 60)[m
[32m+[m
[32m+[m[32m    df = load_ml_job_skills()[m
[32m+[m
[32m+[m[32m    print("Rows:", len(df))[m
[32m+[m[32m    print("Columns:", list(df.columns))[m
[32m+[m
[32m+[m[32m    print()[m
[32m+[m[32m    print("First 10 rows:")[m
[32m+[m[32m    print(df.head(10).to_string(index=False))[m
\ No newline at end of file[m
