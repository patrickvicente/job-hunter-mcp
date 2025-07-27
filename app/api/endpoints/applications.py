from fastapi import APIRouter, Depends, HTTPException
from app.db.schemas import ApplicationBase, ApplicationCreate, ApplicationUpdate, ApplicationRead
from app.db.models import Application, FitScore
from app.db.session import get_db
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ApplicationStatusUpdate(BaseModel):
    """Schema for updating application status."""
    status: str
    notes: Optional[str] = None

class ApplicationUpdateResponse(BaseModel):
    """Simplified response schema for application updates to avoid circular references."""
    id: int
    job_id: int
    resume_id: Optional[int] = None
    status: str
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None

router = APIRouter()

@router.get("/", response_model=list[ApplicationRead])
def list_applications(db=Depends(get_db)):
    """List all applications with job and resume details."""
    applications = db.query(Application).all()
    return applications

@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db=Depends(get_db)):
    """Get a specific application by ID."""
    application = db.query(Application).get(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.post("/", response_model=ApplicationRead, status_code=201)
def create_application(application: ApplicationCreate, db=Depends(get_db)):
    """Create a new application."""
    db_application = Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.put("/{application_id}", response_model=ApplicationUpdateResponse)
def update_application(application_id: int, application: ApplicationUpdate, db=Depends(get_db)):
    """
    Update an application with smart applied_at handling.
    
    Smart applied_at logic:
    - Only set applied_at when status changes to 'applied' for the first time
    - Don't update applied_at if it's already set and status changes again
    - Don't update applied_at for other status changes
    """
    db_application = db.query(Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Get the update data
    update_data = application.model_dump(exclude_unset=True)
    
    # Smart applied_at handling
    if "status" in update_data:
        new_status = update_data["status"]
        old_status = db_application.status
        
        # Only set applied_at if:
        # 1. Status is changing to 'applied'
        # 2. applied_at is not already set (first time applying)
        if (new_status == "applied" and 
            old_status != "applied" and 
            db_application.applied_at is None):
            
            update_data["applied_at"] = datetime.now(timezone.utc)
            logger.info(f"Setting applied_at for application {application_id} - status changed to 'applied'")
        
        # If status is changing from 'applied' to something else, don't clear applied_at
        # This preserves the original application date
    
    # Apply all updates
    for field, value in update_data.items():
        setattr(db_application, field, value)
    
    db.commit()
    db.refresh(db_application)
    return db_application

@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db=Depends(get_db)):
    """
    Delete an application.
    This will also delete any associated fit scores.
    """
    db_application = db.query(Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Log what will be deleted for debugging
    fit_score_count = db.query(FitScore).filter(
        FitScore.job_id == db_application.job_id,
        FitScore.resume_id == db_application.resume_id
    ).count()
    
    logger.info(f"Deleting application {application_id} with {fit_score_count} fit scores")
    
    # Delete the application (cascade will handle fit scores)
    db.delete(db_application)
    db.commit()
    
    return {"message": f"Application and {fit_score_count} fit scores deleted successfully"}

@router.patch("/{application_id}/status", response_model=ApplicationUpdateResponse)
def update_application_status(application_id: int, status_update: ApplicationStatusUpdate, db=Depends(get_db)):
    """
    Update application status with smart applied_at handling.
    This is a simplified endpoint for status updates, commonly used by extensions.
    
    Args:
        application_id: ID of the application to update
        status: New status ('pending', 'applied', 'interview', 'offer', 'rejected')
        notes: Optional notes about the status change
    """
    db_application = db.query(Application).get(application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    old_status = db_application.status
    
    # Update status
    db_application.status = status_update.status
    
    # Smart applied_at handling
    if (status_update.status == "applied" and 
        old_status != "applied" and 
        db_application.applied_at is None):
        
        db_application.applied_at = datetime.now(timezone.utc)
        logger.info(f"Setting applied_at for application {application_id} - status changed to 'applied'")
    
    # Update notes if provided
    if status_update.notes is not None:
        db_application.notes = status_update.notes
    
    db.commit()
    db.refresh(db_application)
    return db_application
    
    