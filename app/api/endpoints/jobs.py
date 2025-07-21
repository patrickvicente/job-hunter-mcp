from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_jobs():
    return [{"id": 1, "title": "Software Engineer"}]