from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_job_data(job_data, context):
    prompt = (
        "You are an AI assistant helping to structure job postings for a job tracking app.\n"
        f"User context: {context}\n"
        "Given the following job posting, extract and complete the following fields if possible (infer if missing):\n"
        "- title\n"
        "- description\n"
        "- company\n"
        "- location\n"
        "- job_category\n"
        "- url\n"
        "- work_mode (remote, onsite, hybrid)\n"
        "- job_type (full-time, part-time, contract, internship)\n"
        "- experience_level (entry, junior, mid, senior, lead)\n"
        "- salary_min\n"
        "- salary_max\n"
        "- currency\n"
        "- visa_sponsorship (true/false)\n"
        "- source\n"
        "- tech_stack (as a list)\n"
        "\n"
        "Also, provide a structured summary with the following sections:\n"
        "About the job\n"
        "Job Responsibilities\n"
        "Requirements\n"
        "Preferred Qualifications\n"
        "\n"
        "Job posting:\n"
        f"Title: {job_data.get('title', '')}\n"
        f"Description: {job_data.get('description', '')}\n"
        f"Company: {job_data.get('company', '')}\n"
        f"Location: {job_data.get('location', '')}\n"
        f"Job Category: {job_data.get('job_category', '')}\n"
        f"URL: {job_data.get('url', '')}\n"
        "\n"
        "Respond ONLY in valid JSON with keys: title, description, company, location, job_category, url, work_mode, job_type, experience_level, salary_min, salary_max, currency, visa_sponsorship, source, tech_stack, summary.\n"
        "The summary should be a dict with keys: about, responsibilities, requirements, preferred_qualifications."
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