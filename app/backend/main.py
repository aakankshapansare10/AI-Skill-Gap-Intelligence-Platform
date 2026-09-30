from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from app.backend.database import get_connection


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Skill Gap Intelligence Platform",
    description="Backend API for the AI Skill Gap Intelligence Platform",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class SkillGapRequest(BaseModel):
    skills: List[str]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_skill(skill):
    """
    Normalize a skill for comparison.

    Example:
        ' Python ' -> 'python'
        'PYTHON'   -> 'python'
    """

    if skill is None:
        return ""

    return " ".join(
        str(skill).strip().lower().split()
    )


def clean_skill_list(skill_text):
    """
    Convert comma-separated skill text into a Python list.

    Example:
        'Python, SQL, Excel'
        ->
        ['Python', 'SQL', 'Excel']
    """

    if not skill_text:
        return []

    skills = []

    for skill in str(skill_text).split(","):

        skill = skill.strip()

        if skill:
            skills.append(skill)

    return skills


def find_matching_skills(student_skills, required_skills):
    """
    Compare student skills with job-required skills.
    """

    student_normalized = {
        normalize_skill(skill)
        for skill in student_skills
        if normalize_skill(skill)
    }

    matching = []
    missing = []

    for required_skill in required_skills:

        normalized_required = normalize_skill(
            required_skill
        )

        if normalized_required in student_normalized:

            matching.append(required_skill)

        else:

            missing.append(required_skill)

    return matching, missing


# ============================================================
# HOME ROUTE
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Skill Gap Intelligence Platform API is running",
        "status": "success"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# DATABASE TEST
# ============================================================

@app.get("/database-test")
def database_test():

    connection = get_connection()

    if connection is None:

        return {
            "status": "error",
            "message": "Could not connect to database"
        }

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_database();"
        )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            "status": "success",
            "database": result[0]
        }

    except Exception as e:

        if connection:
            connection.close()

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# GET JOBS
# ============================================================

@app.get("/jobs")
def get_jobs():

    connection = get_connection()

    if connection is None:

        return {
            "status": "error",
            "message": "Could not connect to database"
        }

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            LIMIT 20;
        """)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        cursor.close()
        connection.close()

        jobs = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "status": "success",
            "count": len(jobs),
            "jobs": jobs
        }

    except Exception as e:

        if connection:
            connection.close()

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# GET SKILLS
# ============================================================

@app.get("/skills")
def get_skills():

    connection = get_connection()

    if connection is None:

        return {
            "status": "error",
            "message": "Could not connect to database"
        }

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM skills
            LIMIT 50;
        """)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        cursor.close()
        connection.close()

        skills = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "status": "success",
            "count": len(skills),
            "skills": skills
        }

    except Exception as e:

        if connection:
            connection.close()

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# GET EXISTING SKILL GAP ANALYSIS
# ============================================================

@app.get("/skill-gap")
def get_skill_gap():

    connection = get_connection()

    if connection is None:

        return {
            "status": "error",
            "message": "Could not connect to database"
        }

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                job_title,
                student_skills,
                required_skills,
                matching_skills,
                missing_skills,
                total_required_skills,
                total_matching_skills,
                total_missing_skills,
                skill_gap_percentage
            FROM skill_gap_analysis
            LIMIT 20;
        """)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        cursor.close()
        connection.close()

        skill_gaps = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "status": "success",
            "count": len(skill_gaps),
            "skill_gaps": skill_gaps
        }

    except Exception as e:

        if connection:
            connection.close()

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# DYNAMIC SKILL GAP ANALYSIS
# ============================================================

@app.post("/skill-gap/analyze")
def analyze_skill_gap(request: SkillGapRequest):

    connection = get_connection()

    if connection is None:

        return {
            "status": "error",
            "message": "Could not connect to database"
        }

    try:

        # ----------------------------------------------------
        # STEP 1: CLEAN STUDENT SKILLS
        # ----------------------------------------------------

        student_skills = [
            skill.strip()
            for skill in request.skills
            if skill and skill.strip()
        ]

        if not student_skills:

            connection.close()

            return {
                "status": "error",
                "message": "Please provide at least one skill."
            }


        # ----------------------------------------------------
        # STEP 2: CREATE SEARCH CONDITIONS
        # ----------------------------------------------------

        conditions = []

        query_params = []

        for skill in student_skills:

            conditions.append(
                "LOWER(required_skills) LIKE %s"
            )

            query_params.append(
                f"%{skill.lower()}%"
            )


        # ----------------------------------------------------
        # STEP 3: BUILD WHERE CLAUSE
        # ----------------------------------------------------

        where_clause = " OR ".join(
            conditions
        )


        # ----------------------------------------------------
        # STEP 4: FIND RELEVANT JOBS
        # ----------------------------------------------------

        query = f"""
            SELECT
                job_title,
                required_skills
            FROM skill_gap_analysis
            WHERE {where_clause}
            LIMIT 20;
        """


        cursor = connection.cursor()

        cursor.execute(
            query,
            query_params
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()


        # ----------------------------------------------------
        # STEP 5: CALCULATE SKILL GAP
        # ----------------------------------------------------

        skill_gaps = []

        for row in rows:

            job_title = row[0]

            required_skills_text = row[1]

            required_skills = clean_skill_list(
                required_skills_text
            )


            # ----------------------------------------------
            # MATCHING AND MISSING SKILLS
            # ----------------------------------------------

            matching_skills, missing_skills = (
                find_matching_skills(
                    student_skills,
                    required_skills
                )
            )


            # ----------------------------------------------
            # CALCULATE COUNTS
            # ----------------------------------------------

            total_required = len(
                required_skills
            )

            total_matching = len(
                matching_skills
            )

            total_missing = len(
                missing_skills
            )


            # ----------------------------------------------
            # CALCULATE SKILL GAP PERCENTAGE
            # ----------------------------------------------

            if total_required > 0:

                skill_gap_percentage = round(
                    (
                        total_missing
                        /
                        total_required
                    ) * 100,
                    2
                )

            else:

                skill_gap_percentage = 0.0


            # ----------------------------------------------
            # ADD RESULT
            # ----------------------------------------------

            skill_gaps.append({

                "job_title": job_title,

                "student_skills":
                    ", ".join(student_skills),

                "required_skills":
                    ", ".join(required_skills),

                "matching_skills":
                    ", ".join(matching_skills)
                    if matching_skills
                    else None,

                "missing_skills":
                    ", ".join(missing_skills)
                    if missing_skills
                    else None,

                "total_required_skills":
                    total_required,

                "total_matching_skills":
                    total_matching,

                "total_missing_skills":
                    total_missing,

                "skill_gap_percentage":
                    skill_gap_percentage
            })


        # ----------------------------------------------------
        # STEP 6: RETURN RESPONSE
        # ----------------------------------------------------

        return {

            "status": "success",

            "count": len(skill_gaps),

            "student_skills":
                student_skills,

            "skill_gaps":
                skill_gaps
        }


    except Exception as e:

        if connection:

            connection.close()

        return {

            "status": "error",

            "message": str(e)
        }