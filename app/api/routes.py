from pathlib import Path
import os

from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, RoadmapRequest, RoadmapResponse, SkillAnalyzeRequest
from app.services.skill_matcher import analyze_role, available_roles
from app.services.rag_service import generate_roadmap, analyze_skill_with_gemini

router = APIRouter()
BASE = Path(__file__).resolve().parents[2]
KB = BASE / "data" / "knowledge_base"


def _slug(name: str) -> str:
    return Path(name).stem


def _skill_files():
    return sorted(KB.glob("*.md"), key=lambda p: p.stem.lower())


@router.get("/roles")
def roles():
    return {"roles": available_roles()}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        return analyze_role(request.target_role, request.skills)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/roadmap", response_model=RoadmapResponse)
def roadmap(request: RoadmapRequest):
    try:
        return {"roadmap": generate_roadmap(request.target_role, request.missing_skills, request.current_skills)}
    except Exception as e:
        print("ROADMAP ERROR:", repr(e))
        raise HTTPException(500, str(e))


@router.get("/skills")
def skills():
    return {
        "skills": [
            {"name": p.stem.replace("_", " ").title(), "slug": p.stem}
            for p in _skill_files()
        ]
    }


@router.get("/skills/{skill_name}")
def skill_details(skill_name: str):
    requested = skill_name.lower().replace(" ", "_")
    path = KB / f"{requested}.md"
    if not path.exists():
        matches = [p for p in _skill_files() if p.stem.lower() == requested]
        if not matches:
            raise HTTPException(404, "Skill not found")
        path = matches[0]
    return {
        "name": path.stem.replace("_", " ").title(),
        "slug": path.stem,
        "content": path.read_text(encoding="utf-8"),
    }


@router.post("/skill-analyze")
def skill_analyze(request: SkillAnalyzeRequest):
    try:
        return {"analysis": analyze_skill_with_gemini(request.skill, request.question)}
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        print("SKILL ANALYSIS ERROR:", repr(e))
        raise HTTPException(500, str(e))
