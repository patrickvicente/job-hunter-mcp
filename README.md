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
