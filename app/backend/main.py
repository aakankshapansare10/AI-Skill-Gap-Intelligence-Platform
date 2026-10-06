from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

from pathlib import Path
import json
import shutil
import tempfile
import sys


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Skill Gap Intelligence Platform",
    description="API for resume-based skill gap analysis and job recommendations",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PROJECT PATHS
# ============================================================

# main.py:
# project/app/backend/main.py
#
# parents[0] = backend
# parents[1] = app
# parents[2] = project root

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_SRC = PROJECT_ROOT / "ml" / "src"
ML_OUTPUTS = PROJECT_ROOT / "ml" / "outputs"

FINAL_JSON = ML_OUTPUTS / "final_student_analysis.json"


# ============================================================
# MAKE PROJECT AVAILABLE TO PYTHON
# ============================================================

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path):

    reader = PdfReader(str(pdf_path))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Skill Gap Intelligence Platform API is running!",
        "version": "1.0.0",
        "status": "online"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "api": "running"
    }


# ============================================================
# PROJECT STATUS
# ============================================================

@app.get("/status")
def status():

    return {
        "api": "running",
        "project_root": str(PROJECT_ROOT),
        "ml_source_exists": ML_SRC.exists(),
        "ml_outputs_exists": ML_OUTPUTS.exists(),
        "final_result_exists": FINAL_JSON.exists()
    }


# ============================================================
# ANALYZE RESUME
# ============================================================

@app.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    target_role: str = Form(...)
):

    # --------------------------------------------------------
    # CHECK TARGET ROLE
    # --------------------------------------------------------

    target_role = target_role.strip()

    if not target_role:

        raise HTTPException(
            status_code=400,
            detail="Target role cannot be empty."
        )


    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not resume.filename:

        raise HTTPException(
            status_code=400,
            detail="Resume file is required."
        )


    # --------------------------------------------------------
    # CHECK FILE TYPE
    # --------------------------------------------------------

    file_extension = Path(
        resume.filename
    ).suffix.lower()

    if file_extension not in [".pdf", ".txt"]:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT resume files are supported."
        )


    temp_pdf_path = None
    temp_resume_path = None


    try:

        # ====================================================
        # PDF RESUME
        # ====================================================

        if file_extension == ".pdf":

            # -----------------------------------------------
            # Save uploaded PDF temporarily
            # -----------------------------------------------

            with tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=".pdf",
                delete=False
            ) as temp_file:

                temp_pdf_path = Path(
                    temp_file.name
                )

                shutil.copyfileobj(
                    resume.file,
                    temp_file
                )


            # -----------------------------------------------
            # Extract PDF text
            # -----------------------------------------------

            extracted_text = extract_pdf_text(
                temp_pdf_path
            )


            # -----------------------------------------------
            # Check extracted text
            # -----------------------------------------------

            if not extracted_text.strip():

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Could not extract text from the PDF. "
                        "Please upload a text-based PDF."
                    )
                )


            # -----------------------------------------------
            # Create temporary TXT file
            # -----------------------------------------------

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".txt",
                delete=False,
                encoding="utf-8"
            ) as temp_txt:

                temp_resume_path = Path(
                    temp_txt.name
                )

                temp_txt.write(
                    extracted_text
                )


        # ====================================================
        # TXT RESUME
        # ====================================================

        else:

            with tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=".txt",
                delete=False
            ) as temp_file:

                temp_resume_path = Path(
                    temp_file.name
                )

                shutil.copyfileobj(
                    resume.file,
                    temp_file
                )


        # ====================================================
        # IMPORT MEMBER-3 ML PIPELINE
        # ====================================================

        from ml.src.resume_analysis_pipeline import (
            run_complete_analysis
        )


        # ====================================================
        # RUN COMPLETE ML PIPELINE
        # ====================================================

        run_complete_analysis(
            str(temp_resume_path),
            target_role
        )


        # ====================================================
        # CHECK FINAL JSON
        # ====================================================

        if not FINAL_JSON.exists():

            raise HTTPException(
                status_code=500,
                detail=(
                    "ML pipeline completed, "
                    "but final_student_analysis.json "
                    "was not generated."
                )
            )


        # ====================================================
        # LOAD FINAL JSON
        # ====================================================

        with open(
            FINAL_JSON,
            "r",
            encoding="utf-8"
        ) as file:

            analysis_result = json.load(file)


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return {

            "status":
                "success",

            "message":
                "Resume analysis completed successfully.",

            "filename":
                resume.filename,

            "target_role":
                target_role,

            "analysis":
                analysis_result
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Resume analysis failed: {str(error)}"
            )
        )


    finally:

        # ====================================================
        # DELETE TEMPORARY PDF
        # ====================================================

        if (
            temp_pdf_path is not None
            and temp_pdf_path.exists()
        ):

            try:

                temp_pdf_path.unlink()

            except Exception:

                pass


        # ====================================================
        # DELETE TEMPORARY TXT
        # ====================================================

        if (
            temp_resume_path is not None
            and temp_resume_path.exists()
        ):

            try:

                temp_resume_path.unlink()

            except Exception:

                pass


# ============================================================
# GET FINAL RESULT
# ============================================================

@app.get("/final-result")
def final_result():

    if not FINAL_JSON.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "No final analysis result found. "
                "Analyze a resume first."
            )
        )


    try:

        with open(
            FINAL_JSON,
            "r",
            encoding="utf-8"
        ) as file:

            analysis_result = json.load(file)


        return {

            "status":
                "success",

            "analysis":
                analysis_result
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not read final result: {str(error)}"
            )
        )


# ============================================================
# ML OUTPUT STATUS
# ============================================================

@app.get("/ml-status")
def ml_status():

    output_files = [

        "student_extracted_skills.csv",

        "resume_job_matching_results.csv",

        "resume_top_job_recommendations.csv",

        "resume_skill_gap_analysis.csv",

        "resume_target_role_analysis.csv",

        "final_student_analysis.csv",

        "final_student_analysis.json"
    ]


    files_status = {}


    for filename in output_files:

        file_path = (
            ML_OUTPUTS / filename
        )

        files_status[filename] = (
            file_path.exists()
        )


    return {

        "ml_outputs_directory":
            str(ML_OUTPUTS),

        "files":
            files_status
    }