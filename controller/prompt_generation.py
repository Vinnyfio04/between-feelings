from typing import List, Optional

from model.db.prompts import (
    SYSTEM_PROMPT,
    CHAT_PROMPT,
    PATTERN_GENERATION_PROMPT,
    CLARIFYING_QUESTIONS_PROMPT,
)
from emotion_log import EmotionLog

def _format_logs(logs: List[EmotionLog]) -> str:
    """
    Converts a list of EmotionLog DTOs into prompt-ready text.
    """
    if not logs:
        return "No emotional logs were provided."

    formatted_logs = []  # Add header first.
    formatted_logs.append("Log ID | User ID | Label | Situation Description | Log Date | Perceived Trigger | Intensity | Sleep Quality | Follow-up Q&A ||")

    for log in logs:
        formatted_logs.append(log.to_prompt_row())
    
    return "\n".join(formatted_logs)



def _build_prompt(system_prompt: str, task_prompt: str, logs_text: str, user_input: Optional[str] = None) -> str:
    """
    Concatenates the prompt in the required order:
    system prompt + relevant prompt + relevant log(s) + optional user input
    """
    # REF(HCDD-120): preserve section order across features so prompt behavior
    # and downstream parsing remain predictable during prompt tuning.
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


def build_chat_prompt(chat_input: str, logs: List[EmotionLog]) -> str:
    return _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=CHAT_PROMPT,
        logs_text=_format_logs(logs),
        user_input=chat_input,
    )


def build_patterns_summary_prompt(logs: List[EmotionLog]) -> str:
    return _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=PATTERN_GENERATION_PROMPT,
        logs_text=_format_logs(logs),
    )


def build_followup_questions_prompt(log: EmotionLog) -> str:
    return _build_prompt(
        system_prompt=SYSTEM_PROMPT,
        task_prompt=CLARIFYING_QUESTIONS_PROMPT,
        logs_text=log.to_prompt_row(),
    )
