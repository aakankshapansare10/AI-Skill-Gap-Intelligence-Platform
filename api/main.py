from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="AI Skill Gap Intelligence Platform",
    description="API for AI-based skill gap analysis and job recommendations",
    version="1.0.0"
)

class SkillAnalysisRequest(BaseModel):
    student_skills: List[str]
    target_role: str

class SkillGapRequest(BaseModel):
    student_skills: List[str]
    required_skills: List[str]
    target_role: str

@app.get("/")
def home():
    return {
        "message": "AI Skill Gap Intelligence Platform API is running!",
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/dataset-status")
def dataset_status():
    return {
        "status": "success",
        "message": "Dataset endpoint is working"
    }

@app.post("/analyze")
def analyze_skills(request: SkillAnalysisRequest):
    skills = [
        skill.strip().lower()
        for skill in request.student_skills
    ]

    return {
        "target_role": request.target_role,
        "student_skills": skills,
        "total_skills": len(skills),
        "message": "Skill analysis successful"
    }

@app.post("/skill-gap")
def skill_gap(request: SkillGapRequest):

    student = {
        skill.strip().lower()
        for skill in request.student_skills
    }

    required = {
        skill.strip().lower()
        for skill in request.required_skills
    }

    matching = sorted(student & required)
    missing = sorted(required - student)

    total = len(required)

    match_percentage = (
        round((len(matching) / total) * 100, 2)
        if total > 0 else 0
    )

    return {
        "target_role": request.target_role,
        "matching_skills": matching,
        "missing_skills": missing,
        "matching_skill_count": len(matching),
        "missing_skill_count": len(missing),
        "match_percentage": match_percentage,
        "skill_gap_percentage": round(100 - match_percentage, 2)
    }

@app.post("/jobs")
def jobs(request: SkillAnalysisRequest):

    return {
        "target_role": request.target_role,
        "student_skills": request.student_skills,
        "message": "Job recommendation endpoint is working"
    }
