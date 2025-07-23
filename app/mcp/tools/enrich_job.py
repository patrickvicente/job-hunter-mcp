"""
MCP Tool: Enrich Job Data

Provides job data enrichment using AI. Supports both backend (direct enrichment) and agentic (prompt-only) modes.
"""

from typing import Dict, Any, Optional
from app.mcp.schemas.enrich_job import EnrichJobInput, EnrichJobOutput
from ...core.ai_client import call_llm
import logging
import json

logger = logging.getLogger(__name__)

class EnrichJobTool:
    """
    MCP tool for AI-based job enrichment.
    Supports both backend (calls AI) and agentic (returns prompt) workflows.
    """

    @staticmethod
    def metadata() -> Dict[str, Any]:
        return {
            "name": "enrich_job",
            "description": "Enrich job data using AI (backend) or return a prompt for agentic LLM client.",
            "inputSchema": EnrichJobInput.model_json_schema(),
            "outputSchema": EnrichJobOutput.model_json_schema()
        }

    @staticmethod
    async def execute(input: EnrichJobInput) -> EnrichJobOutput:
        context = input.context or {}
        mode = context.get("mode", "backend")  # 'backend' (default) or 'agentic'
        job_data = input.model_dump(exclude={"context"})
        prompt = EnrichJobTool._generate_llm_prompt(job_data, context)

        if mode == "agentic":
            # Return the prompt for the agentic/LLM client to process
            return EnrichJobOutput(
                enriched_data={},
                context={**context, "llm_prompt": prompt, "enrichment_mode": "agentic"}
            )
        else:
            # Backend/server mode: call the AI and return the result
            try:
                llm_response = await call_llm(prompt)
                logger.warning(f"LLM enrichment raw response: {repr(llm_response)}")
                enriched = json.loads(llm_response)
                # Merge enriched fields into job_data only if not already present
                for key, value in enriched.items():
                    if not job_data.get(key):
                        job_data[key] = value
                return EnrichJobOutput(
                    enriched_data=job_data,
                    context={**context, "llm_prompt": prompt, "enrichment_mode": "backend"}
                )
            except Exception as e:
                logger.error(f"Error during job enrichment: {e}")
                return EnrichJobOutput(
                    enriched_data=job_data,
                    context={**context, "llm_prompt": prompt, "enrichment_mode": "backend", "error": str(e)}
                )

    @staticmethod
    def _generate_llm_prompt(job_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
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

# FastMCP wrappers
async def enrich_job(input: EnrichJobInput) -> EnrichJobOutput:
    """
    FastMCP tool wrapper for job enrichment.
    - In 'backend' mode (default), the server calls the AI and returns enriched job data.
    - In 'agentic' mode, the server returns a prompt for the client/agent to process with their own LLM.
    """
    context = input.context or {}
    # Normalize mode: treat 'llm' as 'agentic' for backward compatibility
    if context.get("mode") == "llm":
        context["mode"] = "agentic"
    input.context = context
    return await EnrichJobTool.execute(input)

async def enrich_job_prompt(input: EnrichJobInput) -> str:
    """
    Generate an LLM prompt for agentic job enrichment.
    This function returns the prompt string for agentic clients or LLMs to enrich job data externally.
    """
    context = input.context or {}
    # Normalize mode: treat 'llm' as 'agentic' for backward compatibility
    if context.get("mode") == "llm":
        context["mode"] = "agentic"
    job_data = input.model_dump(exclude={"context"})
    return EnrichJobTool._generate_llm_prompt(job_data, context)
