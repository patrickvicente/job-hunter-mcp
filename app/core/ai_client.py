from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_job_data(job_data, context):
    """
    Enrich job data using OpenAI API.
    
    Args:
        job_data: Dictionary containing job information
        context: Additional context for enrichment
        
    Returns:
        Dictionary with enriched job data
    """
    # Define all possible fields
    all_fields = [
        "title", "description", "company", "location", "job_category", "url",
        "work_mode", "job_type", "experience_level", "salary_min", "salary_max",
        "currency", "visa_sponsorship", "source", "tech_stack"
    ]
    
    # Identify missing fields - only ask AI to fill what's actually missing
    missing_fields = [field for field in all_fields if not job_data.get(field)]
    
    # Build the prompt based on the enrich_job tool logic
    prompt = (
        "You are an AI assistant helping to structure job postings for a job tracking app.\n"
        f"User context: {context}\n"
        "Given the following job posting, infer or extract ONLY the following missing fields:\n"
        f"{', '.join(missing_fields) if missing_fields else 'None (all fields present)'}\n"
        "Also, always provide a structured summary with the following sections:\n"
        "About the job\nJob Responsibilities\nRequirements\nPreferred Qualifications\n"
        "\nKnown job data:\n"
    )
    
    # Add all known job data to the prompt
    for field in all_fields:
        prompt += f"{field}: {job_data.get(field, '')}\n"
            
    prompt += (
        "\nRespond ONLY in valid JSON with keys for the missing fields you filled, "
        "and a 'summary' key (dict with keys: about, responsibilities, requirements, preferred_qualifications)."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.2,
    )
    
    try:
        enriched = json.loads(response.choices[0].message.content)
    except Exception:
        enriched = {}
        
    return enriched