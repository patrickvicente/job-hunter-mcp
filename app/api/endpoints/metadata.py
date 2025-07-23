from fastapi import APIRouter
from app.mcp.server import mcp_server
import toml
import os

router = APIRouter()

# Utility to read version from pyproject.toml
PYPROJECT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "pyproject.toml")
def get_project_version():
    try:
        pyproject = toml.load(PYPROJECT_PATH)
        return pyproject["project"]["version"]
    except Exception:
        return "unknown"

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/")
def get_metadata():
    return {
        "app_name": "Job Hunter MCP Server",
        "app_version": get_project_version(),
        "app_description": "A server for the job-hunter-mcp package",
        "app_author": "Patrick Vicente",
        "app_author_email": "patrickvicente.au@gmail.com",
        "app_license": "MIT",
        "app_license_url": "https://opensource.org/licenses/MIT",
        # "app_mcp_tools": mcp_server.get_tools_metadata()
    }
