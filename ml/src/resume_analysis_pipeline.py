import os
import subprocess
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_SRC = PROJECT_ROOT / "ml" / "src"
ML_OUTPUTS = PROJECT_ROOT / "ml" / "outputs"

FINAL_JSON = ML_OUTPUTS / "final_student_analysis.json"


# ============================================================
# RUN PIPELINE SCRIPT
# ============================================================

def run_script(script_name, input_text=None):
    script_path = ML_SRC / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Pipeline script not found: {script_path}"
        )

    print()
    print("=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input=input_text,
            text=True,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            check=False,
        )

        if result.stdout:
            print(result.stdout)

        if result.returncode != 0:
            if result.stderr:
                print("ERROR OUTPUT:")
                print(result.stderr)

            raise RuntimeError(
                f"{script_name} failed with exit code "
                f"{result.returncode}."
            )

        if result.stderr:
            print("SCRIPT MESSAGES:")
            print(result.stderr)

    except OSError as exc:
        raise RuntimeError(
            f"Could not execute {script_name}: {exc}"
        ) from exc


# ============================================================
# STEP 1: RESUME SKILL EXTRACTION
# ============================================================

def run_resume_skill_extractor(resume_path):
    run_script(
        "resume_skill_extractor.py",
        input_text=f"{resume_path}\n",
    )


# ============================================================
# STEP 2: RESUME JOB MATCHING
# ============================================================

def run_job_matching(target_role):
    run_script(
        "resume_job_matching.py",
        input_text=f"{target_role}\n",
    )


# ============================================================
# STEP 3: JOB RECOMMENDATIONS
# ============================================================

def run_job_recommendations():
    run_script("resume_job_recommendation.py")


# ============================================================
# STEP 4: SKILL GAP ANALYSIS
# ============================================================

def run_skill_gap_analysis():
    run_script("resume_skill_gap_analysis.py")


# ============================================================
# STEP 5: TARGET ROLE ANALYSIS
# ============================================================

def run_target_role_analysis(target_role):
    run_script(
        "resume_target_role_analysis.py",
        input_text=f"{target_role}\n",
    )


# ============================================================
# STEP 6: FINAL STUDENT ANALYSIS
# ============================================================

def run_final_analysis():
    run_script("final_student_analysis.py")


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def run_complete_analysis(resume_path, target_role):
    resume_path = str(Path(resume_path).resolve())
    target_role = (target_role or "").strip()

    if not os.path.isfile(resume_path):
        raise FileNotFoundError(
            f"Resume file not found: {resume_path}"
        )

    if not target_role:
        raise ValueError("Target role cannot be empty.")

    print()
    print("#" * 60)
    print("# AI SKILL GAP INTELLIGENCE PLATFORM")
    print("# COMPLETE RESUME ANALYSIS PIPELINE")
    print("#" * 60)

    print(f"\nResume: {resume_path}")
    print(f"Target role: {target_role}")

    # Remove the previous result before running the pipeline.
    # This prevents an old JSON from being mistaken for a new result.
    if FINAL_JSON.exists():
        FINAL_JSON.unlink()

    ML_OUTPUTS.mkdir(parents=True, exist_ok=True)

    # Step 1
    run_resume_skill_extractor(resume_path)

    # Step 2
    run_job_matching(target_role)

    # Step 3
    run_job_recommendations()

    # Step 4
    run_skill_gap_analysis()

    # Step 5
    run_target_role_analysis(target_role)

    # Step 6
    run_final_analysis()

    # Validate final output
    if not FINAL_JSON.exists():
        raise FileNotFoundError(
            "Final analysis JSON was not generated: "
            f"{FINAL_JSON}"
        )

    if FINAL_JSON.stat().st_size == 0:
        raise RuntimeError(
            "Final analysis JSON exists but is empty."
        )

    print()
    print("#" * 60)
    print("# COMPLETE ANALYSIS FINISHED")
    print("#" * 60)
    print(f"Final output: {FINAL_JSON}")


# ============================================================
# COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RESUME ANALYSIS PIPELINE")
    print("=" * 60)

    resume_path = input(
        "\nEnter resume TXT file path: "
    ).strip().strip('"')

    target_role = input(
        "Enter target role: "
    ).strip()

    try:
        run_complete_analysis(
            resume_path,
            target_role,
        )

    except Exception as error:
        print()
        print("=" * 60)
        print("PIPELINE ERROR")
        print("=" * 60)
        print(str(error))
        sys.exit(1)