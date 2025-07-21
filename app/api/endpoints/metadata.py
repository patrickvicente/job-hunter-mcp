from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/metadata")
def get_metadata():
    return {
        "app_name": "Job Hunter MCP Server",
        "app_version": "0.1.0",
        "app_description": "A server for the job-hunter-mcp package",
        "app_author": "Patrick Vicente",
        "app_author_email": "patrickvicente.au@gmail.com",
        "app_license": "MIT",
        "app_license_url": "https://opensource.org/licenses/MIT",
    }
