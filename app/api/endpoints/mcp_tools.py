from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.mcp.tools.enrich_job import enrich_job_data

router = APIRouter()

class EnrichJobRequest(BaseModel):
    job_data: dict
    context: str

@router.post("/mcp/enrich_job")
def enrich_job_endpoint(request: EnrichJobRequest):
    try:
        result = enrich_job_data(request.job_data, request.context)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))