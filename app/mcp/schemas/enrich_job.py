from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EnrichJobInput(BaseModel):
    """
    Input schema for the enrich_job MCP tool.
    Represents all the fields that can be provided to enrich a job posting using AI.
    Each field is optional except for title and description, which are required for meaningful enrichment.
    """
    title: str  # The job title (required)
    description: str  # The job description or posting text (required)
    company: Optional[str] = ""  # Name of the company offering the job
    location: Optional[str] = ""  # Location of the job (city, country, remote, etc.)
    job_category: Optional[str] = ""  # Category or industry of the job
    url: Optional[str] = ""  # URL to the job posting
    work_mode: Optional[str] = ""  # Work mode (e.g., remote, onsite, hybrid)
    job_type: Optional[str] = ""  # Type of job (e.g., full-time, contract)
    experience_level: Optional[str] = ""  # Required experience level (e.g., junior, senior)
    salary_min: Optional[int] = 0  # Minimum salary (if known)
    salary_max: Optional[int] = 0  # Maximum salary (if known)
    currency: Optional[str] = ""  # Currency for salary fields (e.g., USD, EUR)
    visa_sponsorship: Optional[bool] = False  # Whether the job offers visa sponsorship
    source: Optional[str] = ""  # Source of the job posting (e.g., LinkedIn, company site)
    tech_stack: Optional[List[str]] = []  # List of technologies or skills required
    context: Optional[Dict[str, Any]] = None  # Optional context for session or user preferences

class EnrichJobOutput(BaseModel):
    """
    Output schema for the enrich_job MCP tool.
    Contains the enriched job data and optionally the updated context after enrichment.
    """
    enriched_data: Dict[str, Any]  # The resulting enriched job data as a dictionary
    context: Optional[Dict[str, Any]] = None 
