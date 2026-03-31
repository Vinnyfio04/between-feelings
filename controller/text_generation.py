from typing import List

from model.llm_client import generate_text
from emotion_log import EmotionLog
from prompt_generation import (
    build_chat_prompt,
    build_patterns_summary_prompt,
    build_followup_questions_prompt,
)


# takes the user chat input, sends to the llm, returns string response
def generate_chat_text(chat_input: str, logs: List[EmotionLog]) -> str:
    if not chat_input or not chat_input.strip():
        raise ValueError("chat_input cannot be empty.")

    prompt = build_chat_prompt(chat_input=chat_input, logs=logs)

    return generate_text(prompt)


# takes user pattern request, sends to llm, returns string response
def generate_patterns_summary(logs: List[EmotionLog]) -> str:
    if not logs:
        raise ValueError("At least one log is required to generate a pattern summary.")

    prompt = build_patterns_summary_prompt(logs=logs)

    return generate_text(prompt)


# takes one newly created emotion log, sends to llm, returns string response
def generate_followup_questions(log: EmotionLog) -> str:
    prompt = build_followup_questions_prompt(log=log)

    return generate_text(prompt)