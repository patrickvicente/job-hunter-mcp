from datetime import datetime
from enum import Enum
from typing import List, Optional

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
    job_type: Optional[JobType] = JobType.full_time
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.entry
    job_category: str
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
        orm_mode = True

# --- Resume Schemas --- #

class ResumeBase(BaseModel):
    """Base schema for resume attributes."""
    name: str
    job_category: Optional[str] = None
    content: str

class ResumeCreate(ResumeBase):
    """Schema for creating a new resume."""
    pass

class ResumeRead(ResumeBase):
    """Schema for reading a resume."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

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
    resume_id: int
    status: ApplicationStatus = ApplicationStatus.pending
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    job: Optional['JobRead'] = None
    resume: Optional['ResumeRead'] = None

    class Config:
        orm_mode = True

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
        orm_mode = True

# For forward references in nested schemas
defined = globals()
JobRead.model_rebuild()
ApplicationRead.model_rebuild()