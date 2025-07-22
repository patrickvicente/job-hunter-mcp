from app.core.ai_client import enrich_job_data
from app.mcp.server import mcp

@mcp.tool()
def enrich_job(
    title: str,
    description: str,
    company: str = "",
    location: str = "",
    job_category: str = "",
    url: str = "",
    work_mode: str = "",
    job_type: str = "",
    experience_level: str = "",
    salary_min: int = 0,
    salary_max: int = 0,
    currency: str = "",
    visa_sponsorship: bool = False,
    source: str = "",
    tech_stack: list[str] = [],
    context: dict = None
) -> dict:
    """
    Enrich job data using AI.
    """
    job_data = {
        "title": title,
        "description": description,
        "company": company,
        "location": location,
        "job_category": job_category,
        "url": url,
        "work_mode": work_mode,
        "job_type": job_type,
        "experience_level": experience_level,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "currency": currency,
        "visa_sponsorship": visa_sponsorship,
        "source": source,
        "tech_stack": tech_stack,
    }
    enriched = enrich_job_data(job_data, context or {})
    for key, value in enriched.items():
        if not job_data.get(key):
            job_data[key] = value
            
    return job_data

