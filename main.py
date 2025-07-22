"""
Job Hunter Main Entry Point

Supports running FastAPI server or MCP server.
Default mode is MCP server.

Usage with uv:
- uv run job_hunter_main_clean.py           # Run MCP server (default)
- uv run job_hunter_main_clean.py fastapi   # Run FastAPI server only
- SERVER_MODE=fastapi uv run job_hunter_main_clean.py # Use environment variable

Usage with python:
- python job_hunter_main_clean.py           # Run MCP server (default)
- python job_hunter_main_clean.py fastapi   # Run FastAPI server only
"""

import sys
import os
from fastapi import FastAPI
from app.api.endpoints import jobs, applications, metadata, mcp_tools, resumes

# FastAPI app setup
app = FastAPI(
    title="Job Hunter API",
    description="Job hunting and tracking API with MCP integration",
    version="1.0.0"
)

# Register routes
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
app.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
app.include_router(mcp_tools.router, prefix="/mcp", tags=["mcp"])

@app.get("/")
def read_root():
    return {"message": "Job Hunter API - Ready to help you find your dream job!"}

def run_fastapi():
    """Run FastAPI server"""
    import uvicorn
    print("🚀 Starting FastAPI Server...")
    print("📍 API available at: http://localhost:8000")
    print("📚 Docs available at: http://localhost:8000/docs")
    # Use string import for better uv compatibility
    uvicorn.run("job_hunter_main_clean:app", host="0.0.0.0", port=8000, reload=True)

def run_mcp():
    """Run MCP server"""
    from app.mcp.server import mcp_server
    print("🔧 Starting MCP Server...")
    print("📡 MCP protocol: stdio transport")
    mcp_server.run(transport='stdio')

def main():
    """Main entry point with simplified argument handling"""
    # Check command line arguments first
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        # Fall back to environment variable, default to "mcp"
        mode = os.environ.get("SERVER_MODE", "fastapi").lower()
    
    # Mode selection - simplified to just fastapi or mcp
    if mode == "mcp":
        run_mcp()
    elif mode == "fastapi":
        run_fastapi()  # Default mode
    else:
        print(f"❌ Unknown mode: {mode}")
        print("✅ Available modes: mcp (default), fastapi")
        print("\nExamples:")
        print("  uv run main.py              # Run fastapi server")
        print("  uv run main.py mcp          # Run MCP server")
        print("  SERVER_MODE=fastapi uv run main.py  # Use environment variable")
        sys.exit(1)

if __name__ == "__main__":
    main()
