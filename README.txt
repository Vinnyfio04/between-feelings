# Between Feelings
AI-powered emotion tracking app that identifies recurring behavioral patterns from structured logs.

## Project Overview
The purpose of Between Feelings is to help people recognize and regulate their emotions. The primary target users are university students under academic pressure and working professionals facing life stress. The operating model involves users logging into the system with their account and password to ensure user data privacy. Users then input their emotional experiences into the LLM system. The LLM analyzes and guides users to elicit deeper reflections, subsequently generating patterns and saving the data in a database for users to modify and access at any time.

## Implemented Features
- User authentication (sign up, user existence check, login)
- Create emotional logs
- AI-generated follow-up questions before final log submission
- View/search/filter logs
- Edit and delete logs
- AI-generated pattern summaries
- Chat with log data

## Installation
1. Download the code
   - Clone this repo (or download the ZIP) into a local folder.

2. Install Python dependencies
   - Install the dependencies from `requirements.txt`:

     python -m pip install --user -r requirements.txt

3. Run the backend (Flask API)
   - Start the server from the project root:
     python server.py

4. Run the frontend (static HTML)
   - Open the following HTML pages in `view/` in your browser
   - For example:
     - `view/authentication.html` (login -> calls `/authentication/verify_password/...`)
     - `view/logs.html` (renders logs by calling `/logs/<user_id>` and deletes via `DELETE /logs/<user_id>/<log_id>`)
          - NOTE: Test logs can be used to verify deletion. You can search "test" in the search bar to retrieve them.

## Required Environment Variables
The application uses the following environment variables:
- DATABASE_URL
- GOOGLE_GENERATIVE_AI_API_KEY

These values are already configured in the submitted project environment.

## Access & External Resources

- The required API keys and database connection string are already included in the submitted project files.
- No additional configuration is required to run the application as submitted.

### Test User Credentials
- User 1  
  Username: Sarah  
  Password: Sarah  

- User 2  
  Username: Victor  
  Password: Victor  

### External Services Used
- Gemini API (Google Generative AI) for LLM-based text generation  
- Neon PostgreSQL database for persistent storage

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
├── README.txt
├── requirements.txt
├── server.py
├── controller/
│   ├── authentication.py
│   ├── controller.py
│   ├── database_connection.py
│   ├── db_logging.py
│   ├── emotion_log.py
│   ├── prompt_generation.py
│   └── text_generation.py
├── model/
│   ├── llm_client.py
│   └── db/
│       └── prompts.py
├── view/
│   ├── authentication.html
│   ├── chat.html
│   ├── edit_log.html
│   ├── logs.html
│   ├── logo.svg
│   ├── new_log.html
│   ├── patterns.html
│   ├── sign_up.html
│   └── style.css
└── test/
    ├── test_authentication.py
    ├── test_db_logging.py
    └── test_server.py

## Architecture / MVC Flow
`view/*.html` -> `server.py` routes -> `controller/*` -> model/db helpers + Gemini API + Neon PostgreSQL

## Smoke Test Checklist

1. Start the backend (`python server.py`)
2. Open `view/authentication.html`
3. Log in using provided test credentials
4. Create and submit a new emotional log
5. View and search logs on `view/logs.html`
6. Edit or delete an existing log
7. View pattern summaries on `view/patterns.html`
8. Use chat functionality on `view/chat.html`