"""
MCP Tool: Fit Scoring

Calculates a classic fit score between a candidate and a job using rule-based logic.
"""

from typing import Dict, Any
from app.mcp.schemas.fit_scoring import FitScoringInput, FitScoringOutput
from app.db.session import SessionLocal
from app.db.models import Job  # Your SQLAlchemy Job model

class FitScoringTool:
    """
    Class-based MCP tool for fit scoring.
    """

    @staticmethod
    def metadata() -> Dict[str, Any]:
        return {
            "name": "fit_scoring",
            "description": "Calculates a fit score between a candidate and a job using classic rule-based logic.",
            "inputSchema": FitScoringInput.model_json_schema(),
            "outputSchema": FitScoringOutput.model_json_schema()
        }

    @staticmethod
    async def execute(input: FitScoringInput) -> FitScoringOutput:
        data = input.model_dump(exclude={"context"})
        context = input.context or {}
        mode = context.get("mode", "backend")

        if mode == "llm":
            prompt = await FitScoringTool._generate_llm_prompt(input)
            return FitScoringOutput(
                fit_score=0,
                breakdown={},
                explanation="LLM prompt generated.",
                context={**context, "llm_prompt": prompt, "processing_mode": "llm"}
            )
        else:
            db = SessionLocal()
            job = db.query(Job).get(data["job_id"])
            if not job:
                db.close()
                return FitScoringOutput(
                    fit_score=0,
                    breakdown={},
                    explanation="Job not found.",
                    context=context
                )

            # --- Classic scoring logic ---
            score = 0
            breakdown = {}

            # Skills/Tech Stack (50%)
            required_skills = set(getattr(job, "tech_stack", []))
            candidate_skills = set(data.get("candidate_skills", []))
            skill_match = len(required_skills & candidate_skills) / max(1, len(required_skills))
            skill_score = int(skill_match * 50)
            score += skill_score
            breakdown["skills"] = skill_score

            # Experience (20%)
            required_exp = getattr(job, "years_experience", 0)
            candidate_exp = data.get("candidate_experience", 0)
            if candidate_exp >= required_exp:
                exp_score = 20
            elif candidate_exp >= required_exp * 0.75:
                exp_score = 10
            else:
                exp_score = 0
            score += exp_score
            breakdown["experience"] = exp_score

            # Location (10%)
            job_location = getattr(job, "location", "").lower()
            candidate_location = (data.get("candidate_location") or "").lower()
            if job_location == candidate_location:
                loc_score = 10
            elif job_location == "remote" or data.get("willing_to_relocate", False):
                loc_score = 5
            else:
                loc_score = 0
            score += loc_score
            breakdown["location"] = loc_score

            # Job Type (10%)
            job_type = getattr(job, "type", None)
            preferred_type = data.get("preferred_type")
            if job_type and preferred_type and job_type == preferred_type:
                type_score = 10
            else:
                type_score = 0
            score += type_score
            breakdown["job_type"] = type_score

            # Other (10%) - reserved for custom logic
            other_score = 0
            score += other_score
            breakdown["other"] = other_score

            db.close()

            explanation = (
                f"Skills: {breakdown['skills']}/50, "
                f"Experience: {breakdown['experience']}/20, "
                f"Location: {breakdown['location']}/10, "
                f"Job Type: {breakdown['job_type']}/10, "
                f"Other: {breakdown['other']}/10."
            )

            return FitScoringOutput(
                fit_score=min(int(score), 100),
                breakdown=breakdown,
                explanation=explanation,
                context={**context, "processing_mode": "backend"}
            )

    @staticmethod
    async def _generate_llm_prompt(input: FitScoringInput) -> str:
        data = input.model_dump(exclude={"context"})
        context = input.context or {}
        prompt = (
            "You are an AI assistant helping to score candidate fit for a job.\n"
            f"User context: {context}\n"
            "Given the following job and candidate data, return a fit score (0-100) and a breakdown:\n"
            f"Data: {data}\n"
            "\nRespond ONLY in valid JSON with the expected output format."
        )
        return prompt

# FastMCP wrappers
async def fit_scoring(input: FitScoringInput) -> FitScoringOutput:
    return await FitScoringTool.execute(input)

async def fit_scoring_prompt(input: FitScoringInput) -> str:
    return await FitScoringTool._generate_llm_prompt(input)