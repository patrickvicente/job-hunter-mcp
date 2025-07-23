from pydantic import BaseModel
from typing import Optional, Dict, Any, Union

class FitScoringInput(BaseModel):
    """
    Input schema for the fit_scoring MCP tool.
    Requires job_data and resume_data (dict or string).
    """
    job_data: Union[Dict[str, Any], str]
    resume_data: Union[Dict[str, Any], str]
    context: Optional[Dict[str, Any]] = None

class FitScoringOutput(BaseModel):
    """
    Output schema for the fit_scoring MCP tool.
    Returns the fit score, explanation, and recommendation.
    """
    fit_score: int  # The overall fit score (0-100)
    explanation: str  # Human-readable explanation of the score
    recommendation: str  # Recommendation e.g. Update resume, add more skills, etc.
    context: Optional[Dict[str, Any]] = None  # Updated context after execution