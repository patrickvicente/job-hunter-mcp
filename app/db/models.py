from sqlalchemy import ARRAY, JSON, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    company = Column(String)
    location = Column(String)
    work_mode = Column(String) # 'remote', 'hybrid', 'onsite'
    work_type = Column(String) # 'full-time', 'part-time', 'contract', 'internship'
    experience_level = Column(String) # 'entry', 'junior', 'mid', 'senior', 'lead'
    category = Column(String) # 'software-engineer', 'data-scientist', 'product-manager', 'designer', 'marketing', 'sales', 'finance', 'hr', 'legal', 'other'
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String, nullable=True, default="AUD")
    visa_sponsorship = Column(Boolean, default=False)
    url = Column(String)
    source = Column(String) # 'seek', 'linkedin', 'jora', 'remotely', 'other'
    tech_stack = Column(ARRAY(String), nullable=True) # 'python', 'javascript', 'java', 'aws', 'sql'
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    posted_date = Column(DateTime, nullable=True)
    method = Column(String, default="manual") # 'automation', 'manual'
    applications = relationship("Application", back_populates="job")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    job_category = Column(String, nullable=True)
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    parsed_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    applications = relationship("Application", back_populates="resume")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, default="pending") # 'pending', 'applied', 'interview', 'offer', 'rejected', 'withdrawn', 'archived'
    applied_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    # Note: category is now in Job model, not Application

    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")

class FitScore(Base):
    __tablename__ = "fit_scores"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"))
    score = Column(Integer) # 0-100
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    

