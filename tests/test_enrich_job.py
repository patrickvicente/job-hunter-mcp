import pytest
from unittest.mock import patch
from app.mcp.schemas.enrich_job import EnrichJobInput
from app.mcp.tools.enrich_job import enrich_job, enrich_job_prompt
import json

@pytest.mark.asyncio
async def test_enrich_job_backend():
    # Mock call_llm where it is imported in the enrich_job tool
    llm_response = json.dumps({"company": "TestCorp", "summary": {"about": "A test job."}})
    with patch("app.mcp.tools.enrich_job.call_llm", return_value=llm_response):
        input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.")
        result = await enrich_job(input)
        assert isinstance(result.enriched_data, dict)
        assert result.enriched_data["company"] == "TestCorp"
        assert "summary" in result.enriched_data
        assert result.context["enrichment_mode"] == "backend"
        assert "llm_prompt" in result.context

@pytest.mark.asyncio
async def test_enrich_job_agentic():
    input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.", context={"mode": "agentic"})
    result = await enrich_job(input)
    assert result.enriched_data == {}
    assert result.context["enrichment_mode"] == "agentic"
    assert "llm_prompt" in result.context
    # The prompt should mention missing fields
    assert "company" in result.context["llm_prompt"]

@pytest.mark.asyncio
async def test_enrich_job_prompt():
    input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.")
    prompt = await enrich_job_prompt(input)
    assert isinstance(prompt, str)
    assert "Software Engineer" in prompt
    assert "Develop and maintain web applications." in prompt 