from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl

# --- Job Schemas --- #

class WorkMode(str, Enum):
    """Enumeration of possible work modes for a job."""
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"

class Source(str, Enum):
    """Enumeration of possible job sources."""
    seek = "seek"
    linkedin = "linkedin"
    jora = "jora"
    remoteok = "remoteok"
    cryptojobslist = "cryptojobslist"
    upwork = "upwork"
    angellist = "angellist"
    extension = "extension"  # Added for Chrome extension
    other = "other"

class JobType(str, Enum):
    """Enumeration of possible job types."""
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"
    internship = "internship"

class ExperienceLevel(str, Enum):
    """Enumeration of possible experience levels for a job."""
    entry = "entry"
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"

class ApplicationStatus(str, Enum):
    """Enumeration of possible application statuses."""
    pending = "pending"
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"

class JobBase(BaseModel):
    """Base schema for job attributes."""
    title: str
    description: str
    company: str
    location: str
    work_mode: Optional[WorkMode] = WorkMode.onsite
    work_type: Optional[JobType] = JobType.full_time 
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.entry
    category: str  
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = "AUD"
    visa_sponsorship: Optional[bool] = False
    url: HttpUrl
    source: Optional[Source] = Source.seek
    tech_stack: Optional[List[str]] = None

class JobCreate(JobBase):
    """Schema for creating a new job."""
    pass

class JobRead(JobBase):
    """Schema for reading a job, including nested applications."""
    id: int
    created_at: datetime
    applications: Optional[List['ApplicationRead']] = None

    class Config:
        from_attributes = True

class JobUpdate(JobBase):
    """
    Schema for updating a job.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional['WorkMode'] = None
    work_type: Optional['JobType'] = None
    experience_level: Optional['ExperienceLevel'] = None
    category: Optional[str] = None 
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = None
    visa_sponsorship: Optional[bool] = None
    url: Optional['HttpUrl'] = None
    source: Optional['Source'] = None
    tech_stack: Optional[List[str]] = None

    class Config:
        from_attributes = True

# --- Resume Schemas --- #

class ResumeBase(BaseModel):
    name: str
    job_category: Optional[str] = None
    file_url: str
    file_type: str
    parsed_data: Optional[Dict[str, Any]] = None

class ResumeCreate(ResumeBase):
    pass

class ResumeRead(ResumeBase):
    id: int
    created_at: datetime
    applications: Optional[List['ApplicationRead']] = None

    class Config:
        from_attributes = True

# --- Application Schemas --- #

class ApplicationBase(BaseModel):
    """Base schema for application attributes."""
    job_id: int
    resume_id: Optional[int] = None
    status: ApplicationStatus = ApplicationStatus.pending
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""
    pass

class ApplicationRead(BaseModel):
    """Schema for reading an application, including nested job and resume info."""
    id: int
    job_id: int
    resume_id: Optional[int] = None
    status: ApplicationStatus = ApplicationStatus.pending
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    applied_at: Optional[datetime] = None
    job: Optional['JobRead'] = None
    resume: Optional['ResumeRead'] = None

    class Config:
        from_attributes = True

class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    status: Optional[ApplicationStatus] = None
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    resume_id: Optional[int] = None

# --- Fit Score Schemas --- #

class FitScoreBase(BaseModel):
    """Base schema for fit score attributes."""
    job_id: int
    resume_id: int
    score: int # 0-100
    explanation: str

class FitScoreCreate(FitScoreBase):
    """Schema for creating a new fit score."""
    pass

class FitScoreRead(FitScoreBase):
    """Schema for reading a fit score."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# For forward references in nested schemas
defined = globals()
JobRead.model_rebuild()
ApplicationRead.model_rebuild()