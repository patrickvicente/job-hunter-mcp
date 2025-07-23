"""
MCP Tool: Fit Scoring

Calculates a classic fit score between a candidate and a job using rule-based logic.
"""

from typing import Dict, Any, Union, Optional
from app.core.ai_client import call_llm
from app.mcp.schemas.fit_scoring import FitScoringInput, FitScoringOutput
import json
import logging

logger = logging.getLogger(__name__)


class FitScoringTool:
    """
    MCP tool for LLM-based fit scoring between a job and a resume.
    Requires job_data and resume_data (to be provided by backend or agent).
    Supports both backend (calls LLM) and llm/agentic (returns prompt) workflows.
    """

    @staticmethod
    def metadata() -> Dict[str, Any]:
        return {
            "name": "fit_scoring",
            "description": "Uses an LLM to score the fit between a job and a resume. Returns a fit_score (0-100), explanation, and recommendation.",
            "inputSchema": FitScoringInput.model_json_schema(),
            "outputSchema": FitScoringOutput.model_json_schema()
        }

    @staticmethod
    async def execute(input: FitScoringInput) -> FitScoringOutput:
        context = input.context or {}
        mode = context.get("mode", "backend") # backend (DEFAULT) or agentic
        job_data = input.job_data
        resume_data = input.resume_data
        prompt = FitScoringTool._generate_llm_prompt(job_data, resume_data, mode=mode)

        if mode == "agentic":
            # Return the prompt for the agentic/LLM client to process
            return FitScoringOutput(
                fit_score=0,
                explanation="Prompt generated for agentic LLM client. Use the llm_prompt in context to get the score.",
                recommendation="",
                context={**context, "llm_prompt": prompt, "fit_scoring_mode": "agentic"}
            )
        else:
            # Backend/server mode: call the LLM and return the result
            try:
                llm_response = await call_llm(prompt)
                logger.warning(f"LLM raw response: {repr(llm_response)}")
                result = json.loads(llm_response)
                logger.warning(f"LLM parsed response: {repr(result)}")
                return FitScoringOutput(
                    fit_score=result["fit_score"],
                    explanation=result["explanation"],
                    recommendation=result["recommendation"],
                    context={**context, "llm_prompt": prompt, "fit_scoring_mode": "backend"}
                )
            except Exception as e:
                return FitScoringOutput(
                    fit_score=0,
                    explanation=(
                        "There was an error processing the fit score. "
                        "The AI did not return a valid response. "
                        "Please try again later or report to the developer."
                        f"(Technical details: {e})"
                    ),
                    recommendation="",
                    context={**context, "llm_prompt": prompt, "fit_scoring_mode": "backend"}
                )

    @staticmethod
    def _generate_llm_prompt(job_data: Union[Dict[str, Any], str], resume_data: Union[Dict[str, Any], str], mode: str ) -> str:
        prompt = (
            f"Mode: {mode or 'agentic'}\n"
            "You are an expert recruiter. Given the following job description and candidate resume, "
            "score the candidate's fit for the job on a scale of 0-100, and explain your reasoning.\n\n"
            "PREFERENCE: Make it concise and to the point.\n"
            "IMPORTANT: Respond ONLY in valid JSON with this format:\n"
            "{ \"fit_score\": <int>, \"explanation\": <string>, \"recommendation\": <string> }\n\n"
            "Do not include any text before or after the JSON. Do not use markdown. Output JSON only.\n\n"
            "Job:\n"
            f"{job_data}\n\n"
            "Resume:\n"
            f"{resume_data}\n"
        )
        return prompt

# FastMCP wrappers
async def fit_scoring(
    job_data: Union[Dict[str, Any], str],
    resume_data: Union[Dict[str, Any], str],
    mode: str = "backend",
    context: Optional[Dict[str, Any]] = None
) -> FitScoringOutput:
    """
    MCP FastMCP wrapper for fit scoring between a job and a resume.

    - In 'backend' mode (default), the server calls the LLM and returns a fit score, explanation, and recommendation.
    - In 'agentic' mode, the server returns a prompt for the client/agent to process with their own LLM.

    Args:
        job_data (dict or str): Job description or structured job data.
        resume_data (dict or str): Candidate resume or structured resume data.
        mode (str): 'backend' (default) for server-side LLM call, or 'agentic' for prompt-only mode.
        context (dict, optional): Additional context for session, user, or preferences. 'mode' will be set automatically.

    Returns:
        FitScoringOutput: Fit score result (backend) or prompt (agentic).
    """
    context = context or {}
    context["mode"] = mode
    input = FitScoringInput(job_data=job_data, resume_data=resume_data, context=context)
    return await FitScoringTool.execute(input)

async def fit_scoring_prompt(
    job_data: Union[Dict[str, Any], str],
    resume_data: Union[Dict[str, Any], str],
    mode: str = "backend",
) -> str:
    """
    Generate an LLM prompt for agentic fit scoring between a resume and a job description.

    This function returns the prompt string for agentic clients or LLMs to compute the fit score externally.
    The prompt instructs the LLM to respond ONLY in valid JSON with fit_score, explanation, and recommendation.

    Args:
        job_data (dict or str): Job description or structured job data.
        resume_data (dict or str): Candidate resume or structured resume data.
        mode (str): 'backend' or 'agentic' (for API symmetry; does not affect prompt content).

    Returns:
        str: The generated LLM prompt for fit scoring.
    """
    return FitScoringTool._generate_llm_prompt(job_data, resume_data, mode=mode)