import os
import subprocess
import sys


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
# RESUME SKILL EXTRACTION
# ------------------------------------------------------------

def run_resume_skill_extractor(resume_path):

    print()
    print("=" * 60)
    print("STEP 1: EXTRACTING RESUME SKILLS")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "resume_skill_extractor.py"
        )
    ]

    process = subprocess.run(
        command,
        input=resume_path + "\n",
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Resume skill extraction failed."
        )


# ------------------------------------------------------------
# RESUME JOB MATCHING
# ------------------------------------------------------------

def run_job_matching():

    print()
    print("=" * 60)
    print("STEP 2: MATCHING RESUME WITH JOBS")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "resume_job_matching.py"
        )
    ]

    process = subprocess.run(
        command,
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Resume job matching failed."
        )


# ------------------------------------------------------------
# JOB RECOMMENDATIONS
# ------------------------------------------------------------

def run_job_recommendations():

    print()
    print("=" * 60)
    print("STEP 3: GENERATING JOB RECOMMENDATIONS")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "resume_job_recommendation.py"
        )
    ]

    process = subprocess.run(
        command,
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Job recommendation failed."
        )


# ------------------------------------------------------------
# SKILL GAP ANALYSIS
# ------------------------------------------------------------

def run_skill_gap_analysis():

    print()
    print("=" * 60)
    print("STEP 4: ANALYZING SKILL GAPS")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "resume_skill_gap_analysis.py"
        )
    ]

    process = subprocess.run(
        command,
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Skill gap analysis failed."
        )


# ------------------------------------------------------------
# TARGET ROLE ANALYSIS
# ------------------------------------------------------------

def run_target_role_analysis(target_role):

    print()
    print("=" * 60)
    print("STEP 5: ANALYZING TARGET ROLE")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "resume_target_role_analysis.py"
        )
    ]

    process = subprocess.run(
        command,
        input=target_role + "\n",
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Target role analysis failed."
        )


# ------------------------------------------------------------
# FINAL ANALYSIS
# ------------------------------------------------------------

def run_final_analysis():

    print()
    print("=" * 60)
    print("STEP 6: CREATING FINAL STUDENT ANALYSIS")
    print("=" * 60)

    command = [
        sys.executable,
        os.path.join(
            PROJECT_ROOT,
            "ml",
            "src",
            "final_student_analysis.py"
        )
    ]

    process = subprocess.run(
        command,
        text=True,
        cwd=PROJECT_ROOT
    )

    if process.returncode != 0:

        raise RuntimeError(
            "Final student analysis failed."
        )


# ------------------------------------------------------------
# COMPLETE PIPELINE
# ------------------------------------------------------------

def run_complete_analysis(
    resume_path,
    target_role
):

    if not os.path.exists(resume_path):

        raise FileNotFoundError(
            "Resume file not found: "
            + resume_path
        )

    print()
    print("#" * 60)
    print("# AI SKILL GAP INTELLIGENCE PLATFORM")
    print("# COMPLETE RESUME ANALYSIS PIPELINE")
    print("#" * 60)

    print()
    print("Resume:")
    print(resume_path)

    print()
    print("Target Role:")
    print(target_role)

    # Step 1
    run_resume_skill_extractor(
        resume_path
    )

    # Step 2
    run_job_matching()

    # Step 3
    run_job_recommendations()

    # Step 4
    run_skill_gap_analysis()

    # Step 5
    run_target_role_analysis(
        target_role
    )

    # Step 6
    run_final_analysis()

    print()
    print("#" * 60)
    print("# COMPLETE ANALYSIS FINISHED")
    print("#" * 60)

    output_file = os.path.join(
        PROJECT_ROOT,
        "ml",
        "outputs",
        "final_student_analysis.json"
    )

    if os.path.exists(output_file):

        print()
        print(
            "Final output:",
            output_file
        )

    else:

        print()
        print(
            "WARNING: Final JSON file was not found."
        )


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

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

    if not target_role:

        print()
        print(
            "ERROR: Target role cannot be empty."
        )

        sys.exit(1)

    try:

        run_complete_analysis(
            resume_path,
            target_role
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("PIPELINE ERROR")
        print("=" * 60)

        print(
            str(error)
        )

        sys.exit(1)