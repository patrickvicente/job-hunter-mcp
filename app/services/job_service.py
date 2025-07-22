from app.db.models import Job
from app.db.session import db

def create_job_with_enrichment(job_data: JobCreate):
    job = Job(**job_data.model_dump())
    return job