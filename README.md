# Job Hunter MCP Server

A personal, open source platform to supercharge your job search, with a focus on visa sponsorship, AI-powered fit scoring, and workflow automation. Designed for self-hosting and full control.

---

## 🚀 Overview

**Job Hunter MCP** is a backend server and toolkit for job seekers, especially those seeking visa sponsorship (e.g., 482, PR pathways). It leverages AI, automation, and analytics to help you find, track, and apply for jobs more effectively. This project is designed for interoperability and composability, and is listed on [Pulse MCP Servers](https://www.pulsemcp.com/servers).

---

## 🏡 Hosting & Setup

- **Self-hosted:** Run locally or on your own VPS for privacy and control.
- **No authentication:** All endpoints are public for easy automation and integration.
- **Recommended stack:** FastAPI (backend), PostgreSQL (data), Streamlit (dashboard), n8n (automation).

---

## 🔧 Features

- **Visa Sponsorship Job Search:** Scrape and filter jobs by visa type, location, and keywords.
- **AI Fit Scoring:** Score your fit for each job using AI and custom logic.
- **Resume & Cover Letter Tailoring:** LLM-powered customization for each application.
- **Application Tracker:** Add, update, and view applications, statuses, and notes via Streamlit.
- **Follow-up Reminders:** Automated reminders for follow-ups and interviews (via n8n, email, or Telegram).
- **Analytics Dashboard:** Visualize your job search funnel, fit scores, and response times.
- **Export/Import:** Export your data to CSV, Notion, or Google Sheets.
- **Automation:** Use n8n to scrape jobs, send reminders, and sync data.
- **Open API:** All endpoints are public and documented (Swagger/OpenAPI).
- **Pulse MCP Metadata:** `/metadata` endpoint for easy discovery and integration.

---

## ⚡ Quickstart

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/job-hunter-mcp-server.git
   cd job-hunter-mcp-server
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
5. **Launch Streamlit dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
6. **(Optional) Start n8n for automation:**
   - See `/automation/` for workflow templates.

---

## 🌐 Public Endpoints & Usage Examples

All endpoints are public and require no authentication.

### `/metadata` — Server Info
```bash
curl http://localhost:8000/metadata
```

### `/jobs/search` — Search for Jobs
```bash
curl "http://localhost:8000/jobs/search?visa=482&location=Sydney"
```

### `/jobs/score` — Get Fit Score
```bash
curl -X POST http://localhost:8000/jobs/score -H "Content-Type: application/json" -d '{"resume": "...", "job_description": "..."}'
```

### `/resume/tailor` — Tailor Resume/Cover Letter
```bash
curl -X POST http://localhost:8000/resume/tailor -H "Content-Type: application/json" -d '{"resume": "...", "job_description": "..."}'
```

---

## 📊 Visualization & Tracking

- **Streamlit dashboard:** Track applications, statuses, and analytics in real time.
- **Jupyter notebooks:** For custom data analysis with Pandas.
- **Export:** Sync or export data to Notion or Google Sheets as needed.

---

## 🤖 Automation & Rules

- **n8n workflows:** Automate scraping, reminders, and data sync.
- **Rules engine:** Define custom rules for reminders, fit scoring, and notifications (see `/rules/` in MDC format).

---

## 📚 Documentation

- API documentation is auto-generated and available at `/docs` when the server is running.
- See `/rules/` for automation and scoring rules in MDC format.

---

## 🙏 Contributing

Contributions are welcome! Please open issues or pull requests.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🌍 Pulse MCP Listing

This project is listed on [Pulse MCP Servers](https://www.pulsemcp.com/servers) for easy discovery and integration with the wider MCP ecosystem.
