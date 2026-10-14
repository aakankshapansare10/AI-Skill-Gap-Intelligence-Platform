from flask import Flask, jsonify
import json
import os


app = Flask(__name__)


# ------------------------------------------------------------
# PATH TO FINAL ML OUTPUT
# ------------------------------------------------------------

ML_OUTPUT_PATH = (
    "ml/outputs/final_student_analysis.json"
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
# STUDENT ANALYSIS API
# ------------------------------------------------------------

@app.route("/api/student-analysis")
def student_analysis():

    if not os.path.exists(ML_OUTPUT_PATH):

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
# RUN SERVER
# ------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )