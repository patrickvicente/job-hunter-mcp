from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FitScoringInput(BaseModel):
    """
    Input schema for the fit_scoring MCP tool.
    Compares a candidate's profile to a job and returns a fit score.
    """
    job_id: int  # The ID of the job to score against
    candidate_skills: List[str]  # List of candidate's skills
    candidate_experience: Optional[int] = 0  # Years of experience
    candidate_location: Optional[str] = None  # Candidate's location
    willing_to_relocate: Optional[bool] = False  # Relocation flexibility
    preferred_type: Optional[str] = None  # e.g., "full-time", "contract"
    context: Optional[Dict[str, Any]] = None  # Optional context for session/user preferences

class FitScoringOutput(BaseModel):
    """
    Output schema for the fit_scoring MCP tool.
    Returns the fit score and a breakdown of the scoring.
    """
    fit_score: int  # The overall fit score (0-100)
    breakdown: Dict[str, int]  # Score breakdown by criterion
    explanation: str  # Human-readable explanation of the score
    context: Optional[Dict[str, Any]] = None  # Updated context after execution