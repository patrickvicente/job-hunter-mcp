# Job Hunter MCP Server

A personal, open source platform to supercharge your job search, with a focus on visa sponsorship, AI-powered fit scoring, and workflow automation. Designed for self-hosting, full control, and now supporting both REST API and Model Context Protocol (MCP) tools for next-gen AI integration.

---

## 🚀 Overview

**Job Hunter MCP** is a backend server and toolkit for job seekers, especially those seeking visa sponsorship (e.g., 482, PR pathways). It leverages AI, automation, and analytics to help you find, track, and apply for jobs more effectively. This project is designed for interoperability and composability, and is listed on [Pulse MCP Servers](https://www.pulsemcp.com/servers).

---

## 🏗️ Architecture

- **Hybrid FastAPI + MCP:** Provides both traditional REST API endpoints and MCP tools for LLM/agent integration.
- **PostgreSQL:** Used for persistent data storage (jobs, applications, etc.).
- **job-data-extractor Chrome Extension:** Maintained as a separate component for 1-click job data capture.
- **Optional Integrations:** Streamlit dashboard and n8n automation workflows are supported but not required.

---

## 🔧 Features

- **Visa Sponsorship Job Search:** Scrape and filter jobs by visa type, location, and keywords (REST + MCP).
- **AI Fit Scoring:** Score your fit for each job using AI and custom logic (REST + MCP).
- **Resume & Cover Letter Tailoring:** LLM-powered customization for each application (REST + MCP).
- **Application Tracker:** Add, update, and view applications, statuses, and notes (REST + MCP).
- **Follow-up Reminders:** Automated reminders for follow-ups and interviews (optional, via n8n, email, or Telegram).
- **Analytics Dashboard:** Visualize your job search funnel, fit scores, and response times (optional, via Streamlit).
- **Export/Import:** Export your data to CSV, Notion, or Google Sheets.
- **Automation:** Use n8n to scrape jobs, send reminders, and sync data (optional).
- **Open API:** All endpoints are public and documented (Swagger/OpenAPI).
- **Pulse MCP Metadata:** `/metadata` endpoint for easy discovery and integration.

---

## ⚡ Quickstart

1. **Clone the repo:**
   ```bash
   git clone https://github.com/patrickvicente/job-hunter-mcp.git
   cd job-hunter-mcp
   ```
2. **Install dependencies:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Set up PostgreSQL:**
   - Start a local or remote PostgreSQL instance.
   - Set your `DATABASE_URL` environment variable.
4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
5. **(Optional) Launch Streamlit dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
6. **(Optional) Start n8n for automation:**
   - See `/automation/` for workflow templates.

---

## 🌐 Public Endpoints & Usage Examples

All endpoints are public and require no authentication.

### REST API Endpoints

- `/metadata` — Server Info
- `/jobs/search` — Search for Jobs
- `/jobs/score` — Get Fit Score
- `/resume/tailor` — Tailor Resume/Cover Letter
- `/applications` — Application tracking endpoints

### MCP Tools

- **Job Search Tool:** Search for jobs using keywords, location, and visa filters.
- **Job Enrichment Tool:** Extract and enrich job details from URLs or text.
- **Application Tracking Tool:** Track job applications, statuses, and notes.
- **Fit Scoring Tool:** Analyze how well a job matches your skills and preferences.

#### Example: Using MCP Tools with Claude Desktop or Cursor

1. Add the MCP server to your Claude Desktop or Cursor configuration.
2. Use natural language to invoke tools, e.g.:
   - "Find me Python developer jobs in Sydney that sponsor 482 visas."
   - "Enrich this job posting: [URL]"
   - "Track my application to Atlassian."
   - "How well do I fit this job?"

---

## 🧩 Chrome Extension: job-data-extractor

- The `job-data-extractor` Chrome extension is maintained as a separate component for 1-click job data capture from job boards.
- Data can be sent directly to the server or exported for later use.

---

## 📊 Visualization & Tracking (Optional)

- **Streamlit dashboard:** Track applications, statuses, and analytics in real time.
- **Jupyter notebooks:** For custom data analysis with Pandas.
- **Export:** Sync or export data to Notion or Google Sheets as needed.

---

## 🤖 Automation & Rules (Optional)

- **n8n workflows:** Automate scraping, reminders, and data sync.
- **Rules engine:** Define custom rules for reminders, fit scoring, and notifications (see `/rules/` in MDC format).

---

## 📚 Documentation

- API documentation is auto-generated and available at `/docs` when the server is running.
- See `/rules/` for automation and scoring rules in MDC format.
- MCP tool schemas and usage are documented in the repo and compatible with Claude Desktop, Cursor, and other LLM clients.

---

## 🙏 Contributing

Contributions are welcome! Please open issues or pull requests.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🌍 Pulse MCP Listing

This project is listed on [Pulse MCP Servers](https://www.pulsemcp.com/servers) for easy discovery and integration with the wider MCP ecosystem.

<details>
<summary><strong>Job Hunter MCP - Fit Scoring Tool (MCP-Compliant)</strong></summary>

## MCP Tool Compliance
This tool follows the [MCP Tool Implementation Rules](./app/mcp/rules/mcp_tool_flow.mdc):
- **Schema:** Pydantic input/output schemas in `app/mcp/schemas/fit_scoring.py` with docstrings and context support.
- **Tool:** Class-based implementation in `app/mcp/tools/fit_scoring.py` with static methods, backend and agentic mode support, and FastMCP wrappers.
- **Registration:** Registered in `app/mcp/server.py` and `app/mcp/metadata.py`.
- **Wrappers:** FastMCP wrappers for both tool and prompt.
- **Docstrings:** Comprehensive, agentic-friendly docstrings for all public functions.
- **Testing:** Easily testable in isolation; supports both backend and agentic flows.
- **Documentation:** This README and code docstrings document usage, parameters, and modes.

## Usage

### Backend Mode (default)
- The server calls the LLM and returns a fit score, explanation, and recommendation.
- Example:
  ```python
  result = await fit_scoring(job_data, resume_data)
  # or explicitly
  result = await fit_scoring(job_data, resume_data, mode="backend")
  print(result.fit_score, result.explanation, result.recommendation)
  ```

### Agentic Mode
- The server returns a prompt for the client/agent to process with their own LLM. No LLM call is made by the server.
- Example:
  ```python
  result = await fit_scoring(job_data, resume_data, mode="agentic")
  prompt = result.context["llm_prompt"]
  # Agent runs prompt through its own LLM and parses the result
  ```

### Prompt Utility
- The `fit_scoring_prompt` function generates the prompt string for agentic clients or LLMs.
- Example:
  ```python
  prompt = await fit_scoring_prompt(job_data, resume_data, mode="agentic")
  # Use this prompt with your own LLM
  ```

## Notes
- The tool is fully MCP-compliant and supports both backend and agentic workflows.
- The `mode` parameter determines the behavior; agentic clients must set `mode="agentic"`.
- See code docstrings for parameter details and further examples.

## Testing
- **Unit tests** are provided using `pytest` and `pytest-asyncio`, with mocks for LLM calls to ensure fast and reliable testing.
- You may optionally add integration tests for real LLM/API calls if desired.

</details>

<details>
<summary><strong>Job Hunter MCP - Enrich Job Tool (MCP-Compliant)</strong></summary>

## MCP Tool Compliance
This tool follows the [MCP Tool Implementation Rules](./app/mcp/rules/mcp_tool_flow.mdc):
- **Schema:** Pydantic input/output schemas in `app/mcp/schemas/enrich_job.py` with docstrings and context support.
- **Tool:** Class-based implementation in `app/mcp/tools/enrich_job.py` with static methods, backend and agentic mode support, and FastMCP wrappers.
- **Registration:** Registered in `app/mcp/server.py` and `app/mcp/metadata.py`.
- **Wrappers:** FastMCP wrappers for both tool and prompt.
- **Docstrings:** Comprehensive, agentic-friendly docstrings for all public functions.
- **Testing:** Easily testable in isolation; supports both backend and agentic flows.
- **Documentation:** This README and code docstrings document usage, parameters, and modes.

## Usage

### Backend Mode (default)
- The server calls the LLM using the centralized async `call_llm` function and returns enriched job data.
- Example:
  ```python
  from app.mcp.schemas.enrich_job import EnrichJobInput
  from app.mcp.tools.enrich_job import enrich_job
  
  input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.")
  result = await enrich_job(input)
  print(result.enriched_data)
  ```

### Agentic Mode
- The server returns a prompt for the client/agent to process with their own LLM. No LLM call is made by the server.
- Example:
  ```python
  from app.mcp.schemas.enrich_job import EnrichJobInput
  from app.mcp.tools.enrich_job import enrich_job
  
  input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.", context={"mode": "agentic"})
  result = await enrich_job(input)
  prompt = result.context["llm_prompt"]
  # Agent runs prompt through its own LLM and parses the result
  ```

### Prompt Utility
- The `enrich_job_prompt` function generates the prompt string for agentic clients or LLMs.
- Example:
  ```python
  from app.mcp.schemas.enrich_job import EnrichJobInput
  from app.mcp.tools.enrich_job import enrich_job_prompt
  
  input = EnrichJobInput(title="Software Engineer", description="Develop and maintain web applications.")
  prompt = await enrich_job_prompt(input)
  # Use this prompt with your own LLM
  ```

## Notes
- The tool is fully MCP-compliant and supports both backend and agentic workflows.
- All LLM calls are made through the async `call_llm` abstraction for consistency and testability.
- The `mode` parameter in the context determines the behavior; agentic clients must set `context={"mode": "agentic"}`.
- See code docstrings for parameter details and further examples.

## Testing
- **Unit tests** are provided using `pytest` and `pytest-asyncio`, with mocks for LLM calls to ensure fast and reliable testing.
- You may optionally add integration tests for real LLM/API calls if desired.

</details>

# 🧪 Testing

This project uses **unit tests** and supports optional **integration tests** for all MCP tools and core logic.

## Test Types
- **Unit Tests:**
  - Use `pytest` and `pytest-asyncio` for async test support.
  - LLM calls are mocked (using `unittest.mock.patch`) to ensure tests are fast, reliable, and do not require network/API keys.
  - Example: See `tests/test_enrich_job.py` for how the LLM is mocked and tool logic is tested in isolation.
- **Integration Tests (Optional):**
  - You can add tests that call real LLMs (OpenAI, etc.) to verify prompt quality and API integration.
  - These are best run manually or in a separate test suite, as they may be slow, flaky, or incur costs.

## Running Tests

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio
   ```
2. **Run all tests:**
   ```bash
   pytest -v
   ```
3. **Run a specific test file:**
   ```bash
   pytest tests/test_enrich_job.py
   ```
4. **(Optional) Run integration tests:**
   - Mark integration tests with `@pytest.mark.skip` or a custom marker, and run them manually when needed.

## Example: Mocking LLM Calls

```python
from unittest.mock import patch
import json

llm_response = json.dumps({"company": "TestCorp"})
with patch("app.mcp.tools.enrich_job.call_llm", return_value=llm_response):
    # ... run your test logic here ...
```

## Benefits
- **Fast:** No waiting for real LLMs or network calls.
- **Reliable:** Tests are deterministic and do not depend on external services.
- **Safe:** No API keys or costs required for unit tests.

See the `tests/` directory for more examples and patterns.
