# Job Hunter MCP Server

A personal, open source platform to supercharge your job search, with a focus on visa sponsorship, AI-powered fit scoring, and workflow automation. Designed for self-hosting, full control, and now supporting both REST API and Model Context Protocol (MCP) tools for next-gen AI integration.

---

## 🚀 Overview

**Job Hunter MCP** is a backend server and toolkit for job seekers, especially those seeking visa sponsorship (e.g., 482, PR pathways). It leverages AI, automation, and analytics to help you find, track, and apply for jobs more effectively. This project is designed for interoperability and composability, and is listed on [Pulse MCP Servers](https://www.pulsemcp.com/servers).

---

## 🏗️ Architecture

- **Hybrid FastAPI + MCP:** Provides both traditional REST API endpoints and MCP tools for LLM/agent integration.
- **PostgreSQL:** Used for persistent data storage (jobs, applications, etc.).
- **Chrome Extension Integration:** REST API endpoints for receiving job data from the Chrome extension.
- **AI-Powered Tools:** Job enrichment, fit scoring, and application tracking with MCP tools.
- **ETL Pipeline:** Automated job scraping from multiple sources (Seek, Jora, etc.).
- **Text Processing:** Advanced job description parsing and keyword extraction.
- **Optional Integrations:** Streamlit dashboard and n8n automation workflows are supported but not required.

---

## 🔧 Features

### Core Features
- **Visa Sponsorship Job Search:** Scrape and filter jobs by visa type, location, and keywords (REST + MCP).
- **AI Fit Scoring:** Score your fit for each job using AI and custom logic (REST + MCP).
- **Resume & Cover Letter Tailoring:** LLM-powered customization for each application (REST + MCP).
- **Application Tracker:** Add, update, and view applications, statuses, and notes (REST + MCP).
- **Follow-up Reminders:** Automated reminders for follow-ups and interviews (optional, via n8n, email, or Telegram).
- **Analytics Dashboard:** Visualize your job search funnel, fit scores, and response times (optional, via Streamlit).

### New Features (Latest Release)
- **Chrome Extension Integration:** One-click job import from job boards with smart duplicate detection.
- **ETL Pipeline:** Automated job scraping from Seek, Jora, and other sources with configurable filters.
- **Advanced Text Processing:** Intelligent job description parsing, section extraction, and keyword identification.
- **Smart Application Tracking:** Automatic `applied_at` timestamp management and status transitions.
- **Enhanced Database Schema:** Improved job categorization, work type classification, and metadata tracking.
- **Notion Export Tool:** Export job data to Notion databases with filtering and batch processing.

### Integration Features
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
4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```
5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
6. **(Optional) Launch Streamlit dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
7. **(Optional) Start n8n for automation:**
   - See `/automation/` for workflow templates.

---

## 🌐 Public Endpoints & Usage Examples

All endpoints are public and require no authentication.

### REST API Endpoints

#### Core Endpoints
- `/metadata` — Server Info
- `/jobs/` — Job CRUD operations
- `/jobs/search` — Search for Jobs with filters
- `/jobs/score` — Get Fit Score
- `/resume/tailor` — Tailor Resume/Cover Letter
- `/applications` — Application tracking endpoints

#### Chrome Extension Integration
- `/jobs/import-from-extension` — Import job data from Chrome extension
- `/jobs/check-url` — Check if job URL already exists (duplicate detection)

#### ETL & Automation
- `/jobs/fetch` — Trigger ETL job scraping (if configured)
- `/jobs/export` — Export jobs to various formats

### MCP Tools

- **Job Enrichment Tool:** Extract and enrich job details from URLs or text using AI.
- **Fit Scoring Tool:** Analyze how well a job matches your skills and preferences.
- **Application Tracking Tool:** Track job applications, statuses, and notes.
- **Export to Notion Tool:** Export job data to Notion databases with filtering.

**Note:** Job import is handled via REST API (`/jobs/import-from-extension`) for efficiency and cost-effectiveness.

#### Example: Using MCP Tools with Claude Desktop or Cursor

1. Add the MCP server to your Claude Desktop or Cursor configuration.
2. Use natural language to invoke tools, e.g.:
   - "Find me Python developer jobs in Sydney that sponsor 482 visas."
   - "Enrich this job posting: [URL]"
   - "Track my application to Atlassian."
   - "How well do I fit this job?"
   - "Export my recent applications to Notion."

---

## 🧩 Chrome Extension Integration

### Features
- **One-Click Import:** Capture job data directly from job boards with a single click.
- **Smart Duplicate Detection:** Automatically detects if a job URL already exists in your database.
- **Background Processing:** Job enrichment happens asynchronously without blocking the import.
- **Flexible Data Capture:** Supports various job board formats and data structures.

### Integration Flow
1. Chrome extension scrapes job data from the current page
2. Data is sent to `/jobs/import-from-extension` endpoint
3. Server processes and stores the job data
4. Application record is created automatically
5. AI enrichment runs in the background
6. Extension receives confirmation and processed data

### Endpoint Details
- **POST `/jobs/import-from-extension`:** Main import endpoint
- **GET `/jobs/check-url`:** Check for existing jobs by URL
- **PATCH `/applications/{id}/status`:** Update application status

---

## 🔄 ETL Pipeline

### Automated Job Scraping
The ETL pipeline automatically scrapes jobs from multiple sources:

- **Seek.com.au:** Primary Australian job board with API and web scraping
- **Jora.com:** Secondary job board with web scraping
- **Configurable Sources:** Easy to add new job sources via YAML configuration

### Features
- **Intelligent Filtering:** Filter by keywords, location, salary range, work type
- **Duplicate Prevention:** Skip jobs that already exist in the database
- **Rate Limiting:** Respectful scraping with configurable delays
- **Error Handling:** Robust error handling and logging
- **Batch Processing:** Process multiple jobs efficiently

### Configuration
Edit `app/etl/config.yaml` to customize:
- Job sources and their parameters
- Search filters and keywords
- Rate limiting and timeouts
- Data extraction selectors

### Usage
```bash
# Run ETL pipeline manually
python -m app.etl.fetch_jobs

# Or trigger via API
curl -X POST http://localhost:8000/jobs/fetch
```

---

## 📊 Enhanced Text Processing

### Job Description Analysis
The text processor provides intelligent analysis of job descriptions:

- **Section Extraction:** Automatically identifies and extracts common sections (About, Requirements, Responsibilities, Benefits)
- **Keyword Extraction:** Identifies technical skills, tools, and job-related keywords
- **Salary Parsing:** Extracts and normalizes salary information from various formats
- **Date Parsing:** Converts various date formats to ISO standard
- **Text Cleaning:** Normalizes and cleans job description text

### Usage
```python
from app.core.text_processor import process_job_description

# Process a job description
result = process_job_description(job_description_text)
print(result["keywords"])  # ['python', 'aws', 'sql', 'agile']
print(result["description_structured"]["requirements"])  # Requirements section
```

---

## 🗄️ Database Schema Updates

### Recent Changes
- **Enhanced Job Model:** Added `work_type`, `category`, `posted_date`, `method` fields
- **Improved Categorization:** Better job categorization and classification
- **Application Tracking:** Smart `applied_at` timestamp management
- **Metadata Tracking:** Added source tracking and import method information

### Migration
Run database migrations to apply schema changes:
```bash
alembic upgrade head
```

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

<details>
<summary><strong>Job Hunter MCP - Export to Notion Tool (MCP-Compliant)</strong></summary>

## MCP Tool Compliance
This tool follows the [MCP Tool Implementation Rules](./app/mcp/rules/mcp_tool_flow.mdc):
- **Schema:** Pydantic input/output schemas in `app/mcp/schemas/export_to_notion.py` with docstrings and context support.
- **Tool:** Class-based implementation in `app/mcp/tools/export_to_notion.py` with static methods, backend and agentic mode support, and FastMCP wrappers.
- **Registration:** Registered in `app/mcp/server.py` and `app/mcp/metadata.py`.
- **Wrappers:** FastMCP wrappers for both tool and prompt.
- **Docstrings:** Comprehensive, agentic-friendly docstrings for all public functions.
- **Testing:** Easily testable in isolation; supports both backend and agentic flows.
- **Documentation:** This README and code docstrings document usage, parameters, and modes.

## Usage

### Backend Mode (default)
- The server exports job data directly to Notion and returns export results.
- Example:
  ```python
  from app.mcp.schemas.export_to_notion import ExportToNotionInput, NotionExportConfig
  from app.mcp.tools.export_to_notion import export_to_notion
  
  config = NotionExportConfig(
      notion_token="your_token",
      database_id="your_database_id"
  )
  input = ExportToNotionInput(config=config)
  result = await export_to_notion(input)
  print(f"Exported {result.exported} jobs to Notion")
  ```

### Agentic Mode
- The server returns a prompt for the client/agent to process with their own LLM.
- Example:
  ```python
  input = ExportToNotionInput(config=config, context={"mode": "agentic"})
  result = await export_to_notion(input)
  prompt = result.context["llm_prompt"]
  # Agent runs prompt through its own LLM and parses the result
  ```

## Features
- **Batch Export:** Export jobs in configurable batches
- **Filtering:** Filter jobs by source, company, location, date range, status
- **Progress Tracking:** Track export progress and handle errors gracefully
- **Update Existing:** Option to update existing Notion pages or create new ones

## Notes
- The tool is fully MCP-compliant and supports both backend and agentic workflows.
- Requires Notion integration token and database ID for configuration.
- See code docstrings for parameter details and further examples.

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