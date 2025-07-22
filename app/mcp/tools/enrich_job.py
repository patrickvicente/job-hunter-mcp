"""
MCP Tool: Enrich Job Data

This tool provides job data enrichment functionality using AI.
Can work in two modes:
- backend: Direct AI enrichment (returns enriched data)
- llm: Returns prompt for LLM client to do enrichment agentically
"""

from typing import Dict, Any
from app.mcp.schemas.enrich_job import EnrichJobInput, EnrichJobOutput
from ...core.ai_client import enrich_job_data

class EnrichJobTool:
    """
    Class-based MCP tool for job enrichment.
    
    This approach provides better organization, metadata management,
    and makes it easier to test and maintain.
    """
    
    @staticmethod
    def metadata() -> Dict[str, Any]:
        """Tool metadata for MCP registration"""
        return {
            "name": "enrich_job",
            "description": "Enrich job data using AI (backend) or return a prompt for LLM client (agentic)",
            "inputSchema": EnrichJobInput.model_json_schema(),
            "outputSchema": EnrichJobOutput.model_json_schema()
        }
    
    @staticmethod
    async def execute(input: EnrichJobInput) -> EnrichJobOutput:
        """
        Execute job enrichment tool.
        
        Args:
            input: EnrichJobInput schema with job details
            
        Returns:
            EnrichJobOutput with enriched data or LLM prompt
        """
        job_data = input.model_dump(exclude={"context"})
        context = input.context or {}
        mode = context.get("mode", "backend")  # default to backend

        if mode == "llm":
            # Return a prompt for the LLM client to do the enrichment
            prompt = await EnrichJobTool._generate_llm_prompt(input)
            return EnrichJobOutput(
                enriched_data={}, 
                context={**context, "llm_prompt": prompt, "enrichment_mode": "llm"}
            )
        else:
            # Backend enrichment
            enriched = await enrich_job_data(job_data, context) if callable(getattr(enrich_job_data, "__await__", None)) else enrich_job_data(job_data, context)
            for key, value in enriched.items():
                if not job_data.get(key):
                    job_data[key] = value
            return EnrichJobOutput(
                enriched_data=job_data, 
                context={**context, "enrichment_mode": "backend"}
            )
    
    @staticmethod
    async def _generate_llm_prompt(input: EnrichJobInput) -> str:
        """Generate prompt for LLM client enrichment"""
        job_data = input.model_dump(exclude={"context"})
        context = input.context or {}
        
        all_fields = [
            "title", "description", "company", "location", "job_category", "url",
            "work_mode", "job_type", "experience_level", "salary_min", "salary_max",
            "currency", "visa_sponsorship", "source", "tech_stack"
        ]
        
        missing_fields = [field for field in all_fields if not job_data.get(field)]
        
        prompt = (
            "You are an AI assistant helping to structure job postings for a job tracking app.\n"
            f"User context: {context}\n"
            "Given the following job posting, infer or extract ONLY the following missing fields:\n"
            f"{', '.join(missing_fields) if missing_fields else 'None (all fields present)'}\n"
            "Also, always provide a structured summary with the following sections:\n"
            "About the job\nJob Responsibilities\nRequirements\nPreferred Qualifications\n"
            "\nKnown job data:\n"
        )
        
        for field in all_fields:
            prompt += f"{field}: {job_data.get(field, '')}\n"
            
        prompt += (
            "\nRespond ONLY in valid JSON with keys for the missing fields you filled, "
            "and a 'summary' key (dict with keys: about, responsibilities, requirements, preferred_qualifications)."
        )
        
        return prompt

# Function wrappers for FastMCP compatibility
async def enrich_job(input: EnrichJobInput) -> EnrichJobOutput:
    """FastMCP tool wrapper"""
    return await EnrichJobTool.execute(input)

async def enrich_job_prompt(input: EnrichJobInput) -> str:
    """FastMCP prompt wrapper"""
    return await EnrichJobTool._generate_llm_prompt(input)
