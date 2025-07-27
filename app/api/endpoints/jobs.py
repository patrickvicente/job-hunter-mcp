from fastapi import APIRouter, Depends, HTTPException
from app.db.schemas import JobBase, JobCreate, JobUpdate, JobRead, ApplicationRead
from app.db.models import Job, Application, FitScore
from app.db.session import get_db
from app.core.text_processor import process_job_description, parse_salary, parse_posted_date
from app.mcp.tools.enrich_job import EnrichJobInput
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# New schema for Chrome extension integration
class JobDataFromExtension(BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    posted_date: Optional[str] = None
    method: Optional[str] = None
    url: str
    source: Optional[str] = None
    category: Optional[str] = None  # Job category from extension

class ApplicationDataFromExtension(BaseModel):
    status: str = "pending" 
    notes: Optional[str] = None

class JobApplicationImport(BaseModel):
    job: JobDataFromExtension
    application: ApplicationDataFromExtension

class JobImportResponse(BaseModel):
    """Response model for job import from extension."""
    job_id: int
    application_id: int
    job_title: str
    company: str
    message: str
    processed_data: Dict[str, Any]

class JobSearchParams(BaseModel):
    keywords: Optional[str] = None
    location: Optional[str] = None
    visa_sponsorship: Optional[bool] = None
    work_mode: Optional[str] = None
    work_type: Optional[str] = None  # Changed from job_type to work_type
    experience_level: Optional[str] = None
    limit: int = 50

class JobUrlCheckResponse(BaseModel):
    """Response model for job URL check endpoint."""
    exists: bool
    job: Optional[Dict[str, Any]] = None
    application: Optional[Dict[str, Any]] = None

@router.get("/", response_model=list[JobBase])
def list_jobs(db=Depends(get_db)):
    return db.query(Job).all()

@router.get("/check-url", response_model=JobUrlCheckResponse)
async def check_job_url(url: str, db=Depends(get_db)):
    """
    Check if a job URL already exists in the database.
    Returns job and application info if found, or null if not found.
    This endpoint is designed for Chrome extension integration.
    """
    try:
        # Decode URL if it's encoded
        import urllib.parse
        decoded_url = urllib.parse.unquote(url)
        
        # Check if job exists
        job = db.query(Job).filter(Job.url == decoded_url).first()
        
        if job:
            # Get the most recent application for this job
            application = db.query(Application).filter(
                Application.job_id == job.id
            ).order_by(Application.applied_at.desc()).first()
            
            return {
                "exists": True,
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "category": job.category,
                    "work_mode": job.work_mode,
                    "work_type": job.work_type,
                    "experience_level": job.experience_level,
                    "salary_min": job.salary_min,
                    "salary_max": job.salary_max,
                    "url": job.url,
                    "created_at": job.created_at.isoformat() if job.created_at else None
                },
                "application": {
                    "id": application.id if application else None,
                    "status": application.status if application else None,
                    "notes": application.notes if application else None,
                    "applied_at": application.applied_at.isoformat() if application and application.applied_at else None
                } if application else None
            }
        else:
            return {
                "exists": False,
                "job": None,
                "application": None
            }
            
    except Exception as e:
        logger.error(f"Error checking job URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking job URL: {str(e)}")

@router.get("/{job_id}", response_model=JobBase)
def get_job(job_id: int, db=Depends(get_db)):
    job =  db.query(Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JobBase, status_code=201)
def create_job(job: JobCreate, db=Depends(get_db)):
    job_data = job.model_dump()
    job_data['url'] = str(job_data['url'])  # Convert HttpUrl to string
    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.put("/{job_id}", response_model=JobBase)
def update_job(job_id: int, job: JobUpdate, db=Depends(get_db)):
    db_job = db.query(Job).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in job.model_dump(exclude_unset=True).items():
        setattr(db_job, field, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db=Depends(get_db)):
    """
    Delete a job and all associated applications and fit scores.
    This will cascade delete all related data.
    """
    db_job = db.query(Job).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Log what will be deleted for debugging
    application_count = db.query(Application).filter(Application.job_id == job_id).count()
    fit_score_count = db.query(FitScore).filter(FitScore.job_id == job_id).count()
    
    logger.info(f"Deleting job {job_id} with {application_count} applications and {fit_score_count} fit scores")
    
    # Delete the job (cascade will handle the rest)
    db.delete(db_job)
    db.commit()
    
    return {"message": f"Job and {application_count} applications deleted successfully"}

# New endpoints for Chrome extension integration
@router.post("/import-from-extension", response_model=JobImportResponse, status_code=201)
async def import_job_from_extension(data: JobApplicationImport, db=Depends(get_db)):
    """
    Import job and application data from Chrome extension.
    This endpoint receives job data scraped by the extension and application details,
    then creates both job and application records atomically.
    """
    try:
        logger.info(f"Processing job import: {data.job.title} from {data.job.company}")
        
        # Check if job already exists (by URL)
        existing_job = db.query(Job).filter(Job.url == data.job.url).first()
        
        if existing_job:
            # Job exists, just create application
            application = Application(
                job_id=existing_job.id,
                status=data.application.status,
                notes=data.application.notes
            )
            db.add(application)
            db.commit()
            db.refresh(application)
            
            return JobImportResponse(
                job_id=existing_job.id,
                application_id=application.id,
                job_title=existing_job.title,
                company=existing_job.company,
                message="Job already existed, application created",
                processed_data={}
            )
        
        # Step 1: Self-process description immediately (fast, reliable)
        processed_description = process_job_description(data.job.description) if data.job.description else {}
        
        # Parse salary and date using text processor
        salary_data = parse_salary(data.job.salary) if data.job.salary else {"salary_min": None, "salary_max": None}
        posted_date = parse_posted_date(data.job.posted_date) if data.job.posted_date else None
        
        # Create new job with basic processed data
        job_create = JobCreate(
            title=data.job.title or data.job.role,
            description=processed_description.get("description_clean", data.job.description),
            company=data.job.company,
            location=data.job.location,
            url=data.job.url,
            source=data.job.source or "extension",
            method=data.job.method or "manual",
            category=data.job.category or "other", 
            salary_min=salary_data["salary_min"],
            salary_max=salary_data["salary_max"],
            posted_date=posted_date
        )
    
        # Convert Pydantic model to dict and handle HttpUrl conversion
        job_data = job_create.model_dump()
        job_data['url'] = str(job_data['url'])  # Convert HttpUrl to string
        
        # Convert enum values to strings for database storage
        if 'work_mode' in job_data and job_data['work_mode']:
            job_data['work_mode'] = job_data['work_mode'].value
        if 'work_type' in job_data and job_data['work_type']:
            job_data['work_type'] = job_data['work_type'].value
        if 'experience_level' in job_data and job_data['experience_level']:
            job_data['experience_level'] = job_data['experience_level'].value
        if 'source' in job_data and job_data['source']:
            job_data['source'] = job_data['source'].value
        
        logger.info(f"Creating job with data: {job_data}")
        
        db_job = Job(**job_data)
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        # Create application
        application = Application(
            job_id=db_job.id,
            status=data.application.status,
            notes=data.application.notes
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        
        # Step 2: Trigger AI enrichment in background (non-blocking, enhanced)
        # Use asyncio.create_task to run enrichment in background without affecting the response
        try:
            asyncio.create_task(ai_enrich_job_background(db_job.id, processed_description))
        except Exception as enrichment_error:
            # Log enrichment error but don't fail the main request
            logger.warning(f"Background enrichment failed for job {db_job.id}: {enrichment_error}")
            # Continue with the response - enrichment is optional
        
        return JobImportResponse(
            job_id=db_job.id,
            application_id=application.id,
            job_title=db_job.title,
            company=db_job.company,
            message="Job and application created successfully",
            processed_data={
                "keywords": processed_description.get("keywords", []),
                "sections": processed_description.get("description_structured", {}),
                "word_count": processed_description.get("word_count", 0)
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error in import_job_from_extension: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error creating job/application: {str(e)}")

@router.post("/search", response_model=List[JobBase])
async def search_jobs(params: JobSearchParams, db=Depends(get_db)):
    """
    Search jobs with filters.
    This endpoint allows searching jobs by various criteria.
    """
    query = db.query(Job)
    
    if params.keywords:
        # Simple keyword search in title and description
        query = query.filter(
            (Job.title.contains(params.keywords)) |
            (Job.description.contains(params.keywords))
        )
    
    if params.location:
        query = query.filter(Job.location.contains(params.location))
    
    if params.visa_sponsorship is not None:
        query = query.filter(Job.visa_sponsorship == params.visa_sponsorship)
    
    if params.work_mode:
        query = query.filter(Job.work_mode == params.work_mode)
    
    if params.work_type:  # Changed from job_type to work_type
        query = query.filter(Job.work_type == params.work_type)
    
    if params.experience_level:
        query = query.filter(Job.experience_level == params.experience_level)
    
    return query.limit(params.limit).all()

async def ai_enrich_job_background(job_id: int, processed_description: dict):
    """
    Background task to enrich job with AI processing.
    This function runs asynchronously and should not affect the main request.
    """
    try:
        # Get a fresh database session for this background task
        db = next(get_db())
        
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            
            if not job:
                logger.error(f"Job {job_id} not found for AI enrichment")
                return
            
            # Use existing enrich_job MCP tool
            from app.mcp.tools.enrich_job import EnrichJobTool
            
            enrich_input = EnrichJobInput(
                title=job.title,
                description=job.description,
                company=job.company,
                location=job.location,
                url=job.url,
                source=job.source,
                context={"mode": "backend"}
            )
            
            enrichment_result = await EnrichJobTool.execute(enrich_input)
            
            # Update job with AI insights if available
            if enrichment_result.enriched_data:
                enriched_data = enrichment_result.enriched_data
                
                # Always update with AI-provided data (it's more accurate)
                # Handle field name mappings from AI response
                if enriched_data.get("job_category"):
                    job.category = enriched_data["job_category"]
                elif enriched_data.get("category"):
                    job.category = enriched_data["category"]
                
                if enriched_data.get("job_type"):
                    job.work_type = enriched_data["job_type"]
                elif enriched_data.get("work_type"):
                    job.work_type = enriched_data["work_type"]
                
                # Handle work_mode (AI might return different formats)
                if enriched_data.get("work_mode"):
                    work_mode = enriched_data["work_mode"]
                    # Normalize work_mode values
                    if work_mode.lower() in ["full-time", "full time", "fulltime"]:
                        job.work_mode = "onsite"  # Default for full-time
                    elif work_mode.lower() in ["remote", "work from home", "wfh"]:
                        job.work_mode = "remote"
                    elif work_mode.lower() in ["hybrid", "partially remote"]:
                        job.work_mode = "hybrid"
                    else:
                        job.work_mode = work_mode.lower()
                
                # Handle experience_level (AI might return different formats)
                if enriched_data.get("experience_level"):
                    exp_level = enriched_data["experience_level"]
                    # Normalize experience level values
                    if "entry" in exp_level.lower() or "graduate" in exp_level.lower():
                        job.experience_level = "entry"
                    elif "junior" in exp_level.lower():
                        job.experience_level = "junior"
                    elif "mid" in exp_level.lower() or "intermediate" in exp_level.lower():
                        job.experience_level = "mid"
                    elif "senior" in exp_level.lower():
                        job.experience_level = "senior"
                    elif "lead" in exp_level.lower():
                        job.experience_level = "lead"
                    else:
                        job.experience_level = exp_level.lower()
                
                # Update salary information if AI provides it
                if enriched_data.get("salary_min") and enriched_data["salary_min"] > 0:
                    job.salary_min = enriched_data["salary_min"]
                
                if enriched_data.get("salary_max") and enriched_data["salary_max"] > 0:
                    job.salary_max = enriched_data["salary_max"]
                
                # Update currency if provided
                if enriched_data.get("currency"):
                    job.currency = enriched_data["currency"]
                
                # Update visa sponsorship information
                if enriched_data.get("visa_sponsorship") is not None:
                    job.visa_sponsorship = enriched_data["visa_sponsorship"]
                
                # Update tech stack if available
                if enriched_data.get("tech_stack"):
                    job.tech_stack = enriched_data["tech_stack"]
                
                # Update description with AI-enhanced version if available
                if enriched_data.get("summary"):
                    summary = enriched_data["summary"]
                    enhanced_description = job.description
                    
                    # Add AI summary to the description if it's not already there
                    if summary.get("about"):
                        enhanced_description += f"\n\nSummary:\n{summary['about']}"
                    
                    if summary.get("responsibilities"):
                        enhanced_description += f"\n\nKey Responsibilities:\n{summary['responsibilities']}"
                    
                    if summary.get("requirements"):
                        enhanced_description += f"\n\nRequirements:\n{summary['requirements']}"
                    
                    if summary.get("preferred_qualifications"):
                        enhanced_description += f"\n\nPreferred Qualifications:\n{summary['preferred_qualifications']}"
                    
                    job.description = enhanced_description
                
                # Log what was updated for debugging
                updated_fields = []
                if enriched_data.get("job_category") or enriched_data.get("category"):
                    updated_fields.append("category")
                if enriched_data.get("job_type") or enriched_data.get("work_type"):
                    updated_fields.append("work_type")
                if enriched_data.get("work_mode"):
                    updated_fields.append("work_mode")
                if enriched_data.get("experience_level"):
                    updated_fields.append("experience_level")
                if enriched_data.get("salary_min") or enriched_data.get("salary_max"):
                    updated_fields.append("salary")
                if enriched_data.get("tech_stack"):
                    updated_fields.append("tech_stack")
                if enriched_data.get("summary"):
                    updated_fields.append("description")
                
                db.commit()
                logger.info(f"Job {job_id} enriched with AI insights. Updated fields: {', '.join(updated_fields)}")
            else:
                logger.warning(f"No enrichment data returned for job {job_id}")
                
        except Exception as db_error:
            logger.error(f"Database error during enrichment for job {job_id}: {db_error}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error enriching job {job_id} with AI: {e}")
        