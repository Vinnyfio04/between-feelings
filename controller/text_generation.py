from typing import List, Optional

from model.llm_client import generate_text
import db_logging as log_repository
from emotion_log import EmotionLog
from prompt_generation import (
    build_chat_prompt,
    build_patterns_summary_prompt,
    build_followup_questions_prompt,
)


def generate_chat_text(
    chat_input: str,
    logs: Optional[List[EmotionLog]] = None,
    user_id: Optional[int] = None,
) -> str:
    """Generate chat text from explicit logs or logs loaded by user_id."""
    if not chat_input or not chat_input.strip():
        raise ValueError("chat_input cannot be empty.")

    if logs is None:
        if user_id is None:
            raise ValueError("Either logs or user_id is required.")
        logs = log_repository.get_logs(user_id)

    prompt = build_chat_prompt(chat_input=chat_input, logs=logs)

    return generate_text(prompt)


def generate_patterns_summary(
    logs: Optional[List[EmotionLog]] = None,
    user_id: Optional[int] = None,
) -> str:
    """Generate a pattern summary from explicit logs or logs loaded by user_id."""
    if logs is None:
        if user_id is None:
            raise ValueError("Either logs or user_id is required.")
        logs = log_repository.get_logs(user_id)

    if not logs:
        raise ValueError("At least one log is required to generate a pattern summary.")

    prompt = build_patterns_summary_prompt(logs=logs)

    return generate_text(prompt)


def generate_followup_questions(log: EmotionLog) -> str:
    """Generate follow-up questions for a single emotion log."""
    prompt = build_followup_questions_prompt(log=log)

    return generate_text(prompt)