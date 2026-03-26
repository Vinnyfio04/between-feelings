from typing import List, Optional

from model.llm_client import generate_text
from model.db.prompts import (
    SYSTEM_PROMPT,
    CHAT_PROMPT,
    PATTERN_GENERATION_PROMPT,
    CLARIFYING_QUESTIONS_PROMPT,
)
from model.emotion_log import EmotionLog


def _clean_text(value: Optional[str]) -> str:
    """
    Returns a safe, stripped string for prompt formatting.
    """
    if value is None:
        return ""
    return str(value).strip()


def _format_follow_up_qa(follow_up_qa: Optional[str]) -> str:
    """
    Formats follow-up Q/A text safely for the prompt.
    """
    cleaned = _clean_text(follow_up_qa)
    return cleaned if cleaned else "None"


def _format_log(log: EmotionLog) -> str:
    """
    Converts one EmotionLog DTO into a stable plain-text format for the LLM.
    """
    lines = [
        f"Log ID: {log.log_id}",
        f"User ID: {log.user_id}",
        f"Date: {_clean_text(log.log_date)}",
        f"Emotion Label: {_clean_text(log.label)}",
        f"Intensity: {log.intensity}",
        f"Description: {_clean_text(log.situation_description)}",
        f"Trigger: {_clean_text(log.perceived_trigger)}",
        f"Sleep Quality: {_clean_text(log.sleep_quality)}",
        f"Follow-Up Q&A: {_format_follow_up_qa(log.follow_up_qa)}",
    ]

    return "\n".join(lines)


def _format_logs(logs: List[EmotionLog]) -> str:
    """
    Converts a list of EmotionLog DTOs into prompt-ready text.
    """
    if not logs:
        return "No emotional logs were provided."

    formatted_logs = []
    for index, log in enumerate(logs, start=1):
        formatted_logs.append(f"LOG {index}\n{_format_log(log)}")

    return "\n\n---\n\n".join(formatted_logs)


def _build_prompt(
    system_prompt: str,
    task_prompt: str,
    logs_text: str,
    user_input: Optional[str] = None
) -> str:
    """
    Concatenates the prompt in the required order:
    system prompt + relevant prompt + relevant log(s) + optional user input
    """
    parts = [
        system_prompt.strip(),
        "",
        task_prompt.strip(),
        "",
        "LOG DATA:",
        logs_text.strip(),
    ]

    if user_input and user_input.strip():
        parts.extend([
            "",
            "USER INPUT:",
            user_input.strip(),
        ])

    return "\n".join(parts)


# takes the user chat input, sends to the llm, returns string response
def generate_chat_text(chat_input: str, logs: List[EmotionLog]) -> str:
    if not chat_input or not chat_input.strip():
        raise ValueError("chat_input cannot be empty.")

    prompt = _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=CHAT_PROMPT,
        logs_text=_format_logs(logs),
        user_input=chat_input,
    )

    return generate_text(prompt)


# takes user pattern request, sends to llm, returns string response
def generate_patterns_summary(logs: List[EmotionLog]) -> str:
    if not logs:
        raise ValueError("At least one log is required to generate a pattern summary.")

    prompt = _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=PATTERN_GENERATION_PROMPT,
        logs_text=_format_logs(logs),
    )

    return generate_text(prompt)


# takes one newly created emotion log, sends to llm, returns string response
def generate_followup_questions(log: EmotionLog) -> str:
    prompt = _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=CLARIFYING_QUESTIONS_PROMPT,
        logs_text=_format_log(log),
    )

    return generate_text(prompt)