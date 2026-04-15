# Between Feelings
AI-powered emotion tracking app that identifies recurring behavioral patterns from structured logs.

## Project Overview
The purpose of Between Feelings is to help people recognize and regulate their emotions. The primary target users are university students under academic pressure and working professionals facing life stress. The operating model involves users logging into the system with their account and password to ensure user data privacy. Users then input their emotional experiences into the LLM system. The LLM analyzes and guides users to elicit deeper reflections, subsequently generating patterns and saving the data in a database for users to modify and access at any time.

## Implemented Features
- User authentication for secure login and access control
- Retrieval of structured emotional log data from the database
- Search functionality by keyword or emotional intensity

## Planned Features
- Log emotional experiences in a simple, structured format
- Receive AI-generated follow-up questions to clarify entries
- View pattern-based summaries of emotional triggers over time
- Chat with your data to explore trends and insights

## Installation
1. Download the code
   - Clone this repo (or download the ZIP) into a local folder.

2. Install Python dependencies
   - Install the dependencies from `requirements.txt`:

     python -m pip install --user -r requirements.txt

3. Run the backend (Flask API)
   - Start the server from the project root:
     python server.py

5. Run the frontend (static HTML)
   - Open the following HTML pages in `view/` in your browser
   - For example:
     - `view/authentication.html` (login -> calls `/authentication/verify_password/...`)
     - `view/logs.html` (renders logs by calling `/logs/<user_id>` and deletes via `DELETE /logs/<user_id>/<log_id>`)
          - NOTE: Test logs can be used to verify deletion. You can search "test" in the search bar to retrieve them.

## Tech Stack
- Neon (PostgreSQL hosted)
  - Neon is used for the database because it supports efficient PostgreSQL usage and works cleanly with API backends via a single connection string.
- Python
  - `flask` + `flask_cors`: REST API endpoints and CORS so the browser can call the API.
  - `psycopg`: PostgreSQL driver used for querying Neon through `DATABASE_URL`.
  - Built-in Python standard libraries used for core app features and testing (e.g., `unittest`, `dataclasses`, `os`, `sys`, `pathlib`).
- HTML/CSS/JavaScript
  - Static UI pages under `view/` with inline JavaScript that calls the Flask API.

## Project Structure
root/
├── server.py
├── controller/
│   ├── authentication.py
│   ├── controller.py
│   ├── db_logging.py
│   ├── emotion_log.py
│   └── text_generation.py
├── model/
│   ├── llm_client.py
│   └── db/
│       └── prompts.py
├── view/
│   ├── authentication.html
│   ├── chat.html
│   ├── home.html
│   ├── edit_log.html
│   ├── logs.html
│   ├── script.js
│   └── log_style.css
│
├── testharness.py
└── tester.py

## Commenting Guidelines
Use comments to explain intent and constraints, not to narrate obvious syntax.

### What to comment
- Explain non-obvious logic, especially validation branches, fallbacks, polling, retries, and error mapping.
- Document why a decision was made when a simpler-looking option exists.
- Capture business context for limits and rules (for example, hard caps, required fields, and compatibility constraints).
- Add technical debt notes when a shortcut is intentional and temporary.

### What not to comment
- Do not add comments that just restate the next line of code.
- Do not keep commented-out old implementations as history notes.
- Do not over-comment basic HTML structure or trivial assignments.

### Traceability format
- For requirement or bug traceability, include a short reference token in comments:
  - `product/instructor requirement context`
  - `BUG(HCDD-456): bug context and why this guard exists`
- For debt items, use:
  - `TODO(HCDD-789): short reason + intended follow-up`

### Per-file review checklist
- Each new comment answers at least one: intent, constraint, decision rationale, or traceability.
- Comments are placed near the exact branch/logic they justify.
- No duplicate comments that say the same thing in multiple places.
- Naming stays meaningful; comments should not compensate for unclear names when an easy rename is possible in a future pass.
