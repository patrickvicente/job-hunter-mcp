from fastapi import APIRouter, Depends, HTTPException
from app.db.models import Resume
from app.db.schemas import ResumeBase, ResumeCreate, ResumeRead
from app.db.session import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ResumeRead])
def list_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.post("/", response_model=ResumeRead, status_code=201)
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    db_resume = Resume(**resume.model_dump())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@router.put("/{resume_id}", response_model=ResumeRead)
def update_resume(resume_id: int, resume: ResumeBase, db: Session = Depends(get_db)):
    db_resume = db.query(Resume).get(resume_id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    for field, value in resume.model_dump(exclude_unset=True).items():
        setattr(db_resume, field, value)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}", status_code=204)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = db.query(Resume).get(resume_id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.delete(db_resume)
    db.commit()
    return {"message": "Resume deleted successfully"}
