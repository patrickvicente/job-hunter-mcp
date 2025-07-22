from fastapi import APIRouter

from app.db.schemas import JobCreate

router = APIRouter()

@router.get("/")
def list_jobs():
    return []

@router.post("/")
def create_job(job: JobCreate):
    return job
    