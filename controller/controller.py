import db_logging as db_log
import authentication as auth
import text_generation as tg

# Database logging
def save_log(log):
    return db_log.save_log(log)

def update_log(log_id, log):
    return db_log.update_log(log_id, log)

def get_logs(user_id):
    return db_log.get_logs(user_id)

def delete_log(user_id, log_id):
    return db_log.delete_log(user_id, log_id)

# Authentication
def user_exists(username, demo):
    return auth.user_exists(username, demo)

def verify_password(username, demo):
    return auth.verify_password(username, demo)

def create_user(username, password):
    return auth.create_user(username, password)

# Text Generation
def generate_chat_text(prompt, logs):
    return tg.generate_chat_text(prompt, logs)

def generate_patterns_summary():
    return tg.generate_patterns_summary()

def generate_followup_questions():
    return tg.generate_followup_questions()