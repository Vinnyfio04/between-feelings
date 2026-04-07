from typing import Any, Dict, List, Optional

import db_logging as db_log
import authentication as auth
import text_generation as tg
from emotion_log import EmotionLog

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
def user_exists(username):
    return auth.user_exists(username)

def verify_password(username, password):
    return auth.verify_password(username, password)

def create_user(username, password):
    return auth.create_user(username, password)

# Text Generation
def generate_chat_text(
    chat_input: str,
    logs: Optional[List[EmotionLog]] = None,
    user_id: Optional[int] = None,
) -> str:
    return tg.generate_chat_text(chat_input=chat_input, logs=logs, user_id=user_id)

def generate_patterns_summary(
    logs: Optional[List[EmotionLog]] = None,
    user_id: Optional[int] = None,
) -> Dict[str, Any]:
    return tg.generate_patterns_summary(logs=logs, user_id=user_id)

def generate_followup_questions(log: EmotionLog) -> str:
    return tg.generate_followup_questions(log)