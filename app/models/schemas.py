from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    target_role: str
    skills: list[str] = Field(default_factory=list)

class SkillGap(BaseModel):
    skill: str
    category: str
    importance: str
    reason: str

class AnalyzeResponse(BaseModel):
    role: str
    match_percentage: float
    matched_skills: list[str]
    skill_gaps: list[SkillGap]

class RoadmapRequest(BaseModel):
    target_role: str
    missing_skills: list[str]
    current_skills: list[str] = Field(default_factory=list)

class RoadmapResponse(BaseModel):
    roadmap: str

class SkillAnalyzeRequest(BaseModel):
    skill: str
    question: str | None = None
    
