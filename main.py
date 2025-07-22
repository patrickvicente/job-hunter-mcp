from fastapi import FastAPI
from app.api.endpoints import jobs, applications, metadata, mcp_tools
from app.mcp.server import mcp
from app.mcp.tools.enrich_job import enrich_job

app = FastAPI()

# register routes
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
app.include_router(mcp_tools.router, prefix="/mcp", tags=["mcp"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

def main():
    print("Hello from job-hunter-mcp-server!")


if __name__ == "__main__":
    mcp.run()
