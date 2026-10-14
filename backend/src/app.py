from flask import Flask, jsonify, request
import json
import os
import sys
import uuid


# ------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


# ------------------------------------------------------------
# FLASK APP
# ------------------------------------------------------------

app = Flask(__name__)


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

ML_OUTPUT_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs",
    "final_student_analysis.json"
)

UPLOAD_FOLDER = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs",
    "uploaded_resumes"
)


# Create upload folder if it does not exist
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ------------------------------------------------------------
# HOME API
# ------------------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "AI Skill Gap Intelligence Platform API",
        "status": "running"
    })


# ------------------------------------------------------------
# EXISTING STUDENT ANALYSIS API
# ------------------------------------------------------------

@app.route("/api/student-analysis")
def student_analysis():

    if not os.path.exists(
        ML_OUTPUT_PATH
    ):

        return jsonify({
            "error": "ML output file not found"
        }), 404

    with open(
        ML_OUTPUT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return jsonify(data)


# ------------------------------------------------------------
# RESUME UPLOAD + ANALYSIS API
# ------------------------------------------------------------

@app.route(
    "/api/analyze-resume",
    methods=["POST"]
)
def analyze_resume():

    # --------------------------------------------------------
    # CHECK RESUME FILE
    # --------------------------------------------------------

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume file uploaded."
        }), 400

    resume_file = request.files["resume"]

    if resume_file.filename == "":

        return jsonify({
            "error": "No resume selected."
        }), 400


    # --------------------------------------------------------
    # TARGET ROLE
    # --------------------------------------------------------

    target_role = request.form.get(
        "target_role",
        ""
    ).strip()

    if not target_role:

        return jsonify({
            "error": "Target role is required."
        }), 400


    # --------------------------------------------------------
    # SAVE UPLOADED RESUME
    # --------------------------------------------------------

    original_filename = (
        resume_file.filename
    )

    file_extension = os.path.splitext(
        original_filename
    )[1].lower()

    if file_extension != ".txt":

        return jsonify({
            "error": "Currently only TXT resume files are supported."
        }), 400


    unique_filename = (
        str(uuid.uuid4())
        + ".txt"
    )

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    resume_file.save(
        resume_path
    )


    # --------------------------------------------------------
    # RUN COMPLETE ML PIPELINE
    # --------------------------------------------------------

    pipeline_path = os.path.join(
        PROJECT_ROOT,
        "ml",
        "src",
        "resume_analysis_pipeline.py"
    )

    try:

        import subprocess

        process = subprocess.run(
            [
                sys.executable,
                pipeline_path
            ],
            input=(
                resume_path
                + "\n"
                + target_role
                + "\n"
            ),
            text=True,
            capture_output=True,
            cwd=PROJECT_ROOT
        )


        # ----------------------------------------------------
        # CHECK PIPELINE STATUS
        # ----------------------------------------------------

        if process.returncode != 0:

            return jsonify({
                "error": "Resume analysis failed.",
                "details": process.stderr,
                "pipeline_output": process.stdout
            }), 500


        # ----------------------------------------------------
        # READ FINAL JSON
        # ----------------------------------------------------

        if not os.path.exists(
            ML_OUTPUT_PATH
        ):

            return jsonify({
                "error": "Final analysis JSON was not generated."
            }), 500


        with open(
            ML_OUTPUT_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            analysis = json.load(file)


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({
            "status": "success",
            "message": "Resume analyzed successfully.",
            "analysis": analysis
        })


    except Exception as error:

        return jsonify({
            "error": "Unexpected error during resume analysis.",
            "details": str(error)
        }), 500


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )