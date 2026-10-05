from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from app.backend.database import get_connection
from app.backend.nlp_service import nlp_service


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
# REQUEST MODELS
# ============================================================

class SkillGapRequest(BaseModel):
    skills: List[str]


class ResumeRequest(BaseModel):
    resume_text: str


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_skill(skill):

    if skill is None:
        return ""

    return " ".join(
        str(skill).strip().lower().split()
    )


def clean_skill_list(skill_text):

    if not skill_text:
        return []

    skills = []

    for skill in str(skill_text).split(","):

        skill = skill.strip()

        if skill:
            skills.append(skill)

    return skills


def find_matching_skills(
    student_skills,
    required_skills
):

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

            matching.append(
                required_skill
            )

        else:

            missing.append(
                required_skill
            )

    return matching, missing


# ============================================================
# HOME
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
def analyze_skill_gap(
    request: SkillGapRequest
):

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
        # STEP 2: EXACT SKILL SEARCH
        # ----------------------------------------------------

        normalized_student_skills = [
            normalize_skill(skill)
            for skill in student_skills
        ]


        query = """
            SELECT
                job_title,
                required_skills
            FROM skill_gap_analysis
            WHERE EXISTS (
                SELECT 1
                FROM regexp_split_to_table(
                    required_skills,
                    ','
                ) AS required_skill
                WHERE LOWER(TRIM(required_skill))
                      = ANY(%s)
            )
            LIMIT 20;
        """


        cursor = connection.cursor()

        cursor.execute(
            query,
            (normalized_student_skills,)
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()


        # ----------------------------------------------------
        # STEP 3: CALCULATE SKILL GAP
        # ----------------------------------------------------

        skill_gaps = []

        for row in rows:

            job_title = row[0]

            required_skills_text = row[1]

            required_skills = clean_skill_list(
                required_skills_text
            )


            # ------------------------------------------------
            # MATCHING / MISSING
            # ------------------------------------------------

            matching_skills, missing_skills = (
                find_matching_skills(
                    student_skills,
                    required_skills
                )
            )


            # ------------------------------------------------
            # COUNTS
            # ------------------------------------------------

            total_required = len(
                required_skills
            )

            total_matching = len(
                matching_skills
            )

            total_missing = len(
                missing_skills
            )


            # ------------------------------------------------
            # GAP PERCENTAGE
            # ------------------------------------------------

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


            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            skill_gaps.append({

                "job_title":
                    job_title,

                "student_skills":
                    student_skills,

                "required_skills":
                    required_skills,

                "matching_skills":
                    matching_skills,

                "missing_skills":
                    missing_skills,

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
        # RETURN
        # ----------------------------------------------------

        return {

            "status":
                "success",

            "count":
                len(skill_gaps),

            "student_skills":
                student_skills,

            "skill_gaps":
                skill_gaps
        }


    except Exception as e:

        if connection:
            connection.close()

        return {

            "status":
                "error",

            "message":
                str(e)
        }


# ============================================================
# RESUME → NLP SKILL EXTRACTION
# ============================================================

@app.post("/resume/extract-skills")
def extract_resume_skills(
    request: ResumeRequest
):

    if not request.resume_text.strip():

        return {

            "status":
                "error",

            "message":
                "Resume text cannot be empty."
        }


    try:

        skills = nlp_service.extract_skills(
            request.resume_text
        )


        return {

            "status":
                "success",

            "skill_count":
                len(skills),

            "skills":
                skills
        }


    except Exception as e:

        return {

            "status":
                "error",

            "message":
                str(e)
        }


# ============================================================
# COMPLETE RESUME ANALYSIS
# NLP + DATABASE + SKILL GAP
# ============================================================

@app.post("/resume/analyze")
def analyze_resume(
    request: ResumeRequest
):

    # --------------------------------------------------------
    # CHECK RESUME
    # --------------------------------------------------------

    if not request.resume_text.strip():

        return {
            "status": "error",
            "message": "Resume text cannot be empty."
        }

    try:

        # ====================================================
        # STEP 1: NLP SKILL EXTRACTION
        # ====================================================

        extracted_skills = (
            nlp_service.extract_skills(
                request.resume_text
            )
        )

        # ====================================================
        # STEP 2: GET CANONICAL SKILL NAMES
        # ====================================================

        student_skills = []

        for skill in extracted_skills:

            skill_name = skill.get(
                "canonical_skill_name"
            )

            if skill_name:
                student_skills.append(skill_name)

        # ----------------------------------------------------
        # REMOVE DUPLICATES
        # ----------------------------------------------------

        unique_skills = []
        seen = set()

        for skill in student_skills:

            normalized = normalize_skill(skill)

            if normalized and normalized not in seen:

                seen.add(normalized)
                unique_skills.append(skill)

        student_skills = unique_skills

        # ====================================================
        # NO SKILLS FOUND
        # ====================================================

        if not student_skills:

            return {
                "status": "success",
                "message": "No technical skills were detected.",
                "student_skills": [],
                "skill_count": 0,
                "jobs_analyzed": 0,
                "jobs_returned": 0,
                "skill_gaps": []
            }

        # ====================================================
        # STEP 3: DATABASE CONNECTION
        # ====================================================

        connection = get_connection()

        if connection is None:

            return {
                "status": "error",
                "message": "Could not connect to database."
            }

        # ====================================================
        # STEP 4: GET ALL JOBS
        # ====================================================

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                job_title,
                required_skills
            FROM skill_gap_analysis
            WHERE required_skills IS NOT NULL;
        """)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        # ====================================================
        # STEP 5: NORMALIZE STUDENT SKILLS
        # ====================================================

        normalized_student_skills = {
            normalize_skill(skill)
            for skill in student_skills
            if normalize_skill(skill)
        }

        # ====================================================
        # STEP 6: CALCULATE SKILL GAPS
        # ====================================================

        skill_gaps = []

        for row in rows:

            job_title = row[0]
            required_skills_text = row[1]

            required_skills = clean_skill_list(
                required_skills_text
            )

            if not required_skills:
                continue

            # ------------------------------------------------
            # REMOVE DUPLICATE REQUIRED SKILLS
            # ------------------------------------------------

            unique_required_skills = []
            seen_required = set()

            for skill in required_skills:

                normalized = normalize_skill(skill)

                if normalized and normalized not in seen_required:

                    seen_required.add(normalized)
                    unique_required_skills.append(skill)

            required_skills = unique_required_skills

            # ------------------------------------------------
            # FIND MATCHING AND MISSING SKILLS
            # ------------------------------------------------

            matching_skills = []
            missing_skills = []

            for required_skill in required_skills:

                normalized_required = normalize_skill(
                    required_skill
                )

                if normalized_required in normalized_student_skills:

                    matching_skills.append(required_skill)

                else:

                    missing_skills.append(required_skill)

            # ------------------------------------------------
            # COUNTS
            # ------------------------------------------------

            total_required = len(required_skills)
            total_matching = len(matching_skills)
            total_missing = len(missing_skills)

            # ------------------------------------------------
            # MATCH PERCENTAGE
            # ------------------------------------------------

            if total_required > 0:

                match_percentage = round(
                    (
                        total_matching
                        / total_required
                    ) * 100,
                    2
                )

            else:

                match_percentage = 0.0

            # ------------------------------------------------
            # SKILL GAP PERCENTAGE
            # ------------------------------------------------

            if total_required > 0:

                skill_gap_percentage = round(
                    (
                        total_missing
                        / total_required
                    ) * 100,
                    2
                )

            else:

                skill_gap_percentage = 0.0

            skill_gaps.append({

                "job_title":
                    job_title,

                "required_skills":
                    required_skills,

                "matching_skills":
                    matching_skills,

                "missing_skills":
                    missing_skills,

                "total_required_skills":
                    total_required,

                "total_matching_skills":
                    total_matching,

                "total_missing_skills":
                    total_missing,

                "match_percentage":
                    match_percentage,

                "skill_gap_percentage":
                    skill_gap_percentage
            })

        # ====================================================
        # STEP 7: RANK JOBS
        # Highest match first
        # ====================================================

        skill_gaps.sort(
            key=lambda job: (
                job["match_percentage"],
                job["total_matching_skills"],
                -job["skill_gap_percentage"]
            ),
            reverse=True
        )

        # ====================================================
        # STEP 8: RETURN TOP 20 JOBS
        # ====================================================

        top_skill_gaps = skill_gaps[:20]

        # ====================================================
        # STEP 9: RETURN COMPLETE RESULT
        # ====================================================

        return {

            "status":
                "success",

            "student_skills":
                student_skills,

            "skill_count":
                len(student_skills),

            "jobs_analyzed":
                len(skill_gaps),

            "jobs_returned":
                len(top_skill_gaps),

            "skill_gaps":
                top_skill_gaps
        }

    except Exception as e:

        return {

            "status":
                "error",

            "message":
                str(e)
        }
