from fastapi import APIRouter, Depends, HTTPException
from app.db.schemas import JobBase, JobCreate, JobUpdate
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[JobBase])
def list_jobs(db=Depends(get_db)):
    return db.query(JobBase).all(), 200

@router.get("/{job_id}", response_model=JobBase)
def get_job(job_id: int, db=Depends(get_db)):
    job =  db.query(JobBase).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job, 200

@router.post("/", response_model=JobBase)
def create_job(job: JobCreate, db=Depends(get_db)):
    db_job = JobBase(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job, 201

@router.put("/{job_id}", response_model=JobBase)
def update_job(job_id: int, job: JobUpdate, db=Depends(get_db)):
    db_job = db.query(JobBase).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in job.model_dump(exclude_unset=True).items():
        setattr(db_job, field, value)
    db.commit()
    db.refresh(db_job)
    return db_job, 200

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db=Depends(get_db)):
    db_job = db.query(JobBase).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}, 204