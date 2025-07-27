from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class NotionExportConfig(BaseModel):
    """Configuration for Notion export"""
    notion_token: str  # Notion integration token
    database_id: str   # Target Notion database ID
    page_size: int = 50  # Number of jobs to export per batch
    update_existing: bool = True  # Whether to update existing entries

class NotionJobFilter(BaseModel):
    """Filters for selecting jobs to export"""
    source: Optional[str] = None  # Filter by job source
    company: Optional[str] = None  # Filter by company
    location: Optional[str] = None  # Filter by location
    date_from: Optional[str] = None  # Export jobs from this date
    date_to: Optional[str] = None    # Export jobs to this date
    status: Optional[str] = None     # Filter by application status
    limit: int = 100  # Maximum number of jobs to export

class ExportToNotionInput(BaseModel):
    """
    Input schema for the export_to_notion MCP tool.
    
    This tool exports job data from the database to a Notion database.
    Supports filtering and batch export with progress tracking.
    """
    config: NotionExportConfig
    filters: Optional[NotionJobFilter] = None
    context: Optional[Dict[str, Any]] = None

class ExportToNotionOutput(BaseModel):
    """
    Output schema for the export_to_notion MCP tool.
    
    Returns export results and any errors encountered.
    """
    total_jobs: int
    exported: int
    updated: int
    failed: int
    notion_pages_created: List[str]  # List of Notion page IDs
    errors: List[Dict[str, Any]]
    export_summary: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None 