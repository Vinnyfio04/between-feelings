# Between Feelings
## Project Overview
The main purpose of Between Feelings is to help people recognize and regulate their emotions. The primary target users are university students under academic pressure and working professionals facing life stress. The operating model involves users logging into the system with their account and password to ensure user data privacy. Users then input their emotional experiences into the LLM system. The LLM analyzes and guides users to elicit deeper reflections, subsequently generating patterns and saving the data in a database for users to modify and access at any time.

## Project Structure
root/
│
├── controller/
│   ├── authentication.py
│   ├── controller.py
│   ├── db_logging.py
│   ├── EmotionLog.py
│   ├── text_generation.py
│   └── unit_test.py
│
├── model/
│   ├── llm_client.py
│   └── db/
│       ├── logs.sql
│       ├── patterns.json
│       └── prompts.py
│
├── view/
│   ├── authentication.html
│   ├── home.html
│   ├── chat.html
│   ├── logs.html
│   ├── script.js
│   └── styles.css
│
├── testharness.py
│
└── readme.txt

## Functional Flows
### 1. Authentication
#### Methods Used:
- controller.user_exists(username, demo)
- controller.verify_password(username, demo)
- controller.create_user(username, password)

#### Test Inputs:
username = "demo"
demo = "demo"

#### Flows:
- user_exists returns True for matching input, False otherwise
- verify_password returns True for matching input, False otherwise
- create_user returns True
PASS if returned booleans match expected values.

### 2. Emotional Log Operations
#### Methods Used:
- controller.save_log(log)
- controller.update_log(log_id, log)
- db_logging.get_logs(user_id)
- db_logging.get_log(log_id)

#### Flow:
- Create an EmotionLog instance with sample data
- save_log returns True
- update_log returns True
- get_logs returns a list
- get_log returns an EmotionLog object
PASS if return types are correct and no errors occur.

### 3. Text Generation
####Methods Used:
- controller.generate_chat_text(prompt, logs)
- controller.generate_patterns_summary()
- controller.generate_followup_questions()

Flow:
- Each method is called with sample input
- Each returns a string ("response")
PASS if return type is string.

### 4. LLM Connectivity
#### Methods Used:
- llm_client.llm_connect(llm)
- llm_client.db_llm_connect(db, llm)
- llm_client.generate_text(prompt)
#### Flow:
- Connectivity methods return True
- generate_text returns a string
PASS if expected boolean and string values are returned.

## Team Contributions
Joshua Beers - Worked on llm_client.py, text_generation.py , and testharness.py
Vincenzo Fiorenza - Worked on authentication.py, db_logging.py, and provided feedback on llm_client.py and text_generation.py
Jacob Lee - Focused on the Project Detailed Design assignment; provided feedback and maintained a constant stream of communication to ensure alignment between class, activity, sequence diagrams and API stubs; helped develop the API stub unit tests and README.
Qingyun Yao - Focused on the Project Detailed Design assignment; provided feebdback and on API stubs; contributed to the README file.