import ast
import json
from typing import Any, Dict, List, Optional

from model.llm_client import generate_text
import db_logging as log_repository
from emotion_log import EmotionLog
from prompt_generation import (
    build_chat_prompt,
    build_patterns_summary_prompt,
    build_followup_questions_prompt,
)


class NoLogsAvailableError(ValueError):
    """Raised when no logs are available for pattern summary generation."""


class InvalidLLMJsonError(ValueError):
    """Raised when the model output is malformed or schema-invalid JSON."""


class LLMResponseError(ValueError):
    """Raised when the model response is unusable for summary generation."""


class InvalidFollowupQuestionsError(ValueError):
    """Raised when follow-up questions output is malformed or invalid."""


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
) -> Dict[str, Any]:
    """Generate a pattern summary from explicit logs or logs loaded by user_id."""
    if logs is None:
        if user_id is None:
            raise ValueError("Either logs or user_id is required.")
        logs = log_repository.get_logs(user_id)

    if not logs:
        raise NoLogsAvailableError("At least one log is required to generate a pattern summary.")

    prompt = build_patterns_summary_prompt(logs=logs)

    try:
        raw_text = generate_text(prompt)
        # region agent log
        print(f"[DEBUG patterns raw_text] {raw_text}")
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "pre-fix",
                    "hypothesisId": "H1-H5",
                    "location": "controller/text_generation.py:62",
                    "message": "generate_text succeeded with raw patterns payload",
                    "data": {"raw_text": raw_text},
                    "timestamp": __import__("time").time_ns() // 1_000_000,
                }) + "\n")
        except Exception:
            pass
        # endregion
    except Exception as exc:
        # region agent log
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H7",
                    "location": "controller/text_generation.py:80",
                    "message": "generate_text raised exception",
                    "data": {"error_type": type(exc).__name__, "error": str(exc)},
                    "timestamp": __import__("time").time_ns() // 1_000_000,
                }) + "\n")
        except Exception:
            pass
        # endregion
        raise LLMResponseError(f"Pattern summary generation failed: {str(exc)}") from exc
    return _parse_and_validate_patterns_json(raw_text)


def generate_followup_questions(log: EmotionLog) -> List[str]:
    """Generate follow-up questions for a single emotion log."""
    prompt = build_followup_questions_prompt(log=log)

    raw_text = generate_text(prompt)
    return _parse_and_validate_followup_questions(raw_text)


def _parse_and_validate_followup_questions(raw_text: str) -> List[str]:
    if not raw_text or not raw_text.strip():
        raise InvalidFollowupQuestionsError("Follow-up questions response is empty.")

    candidate = raw_text.strip()
    if candidate.startswith("```"):
        first_newline = candidate.find("\n")
        if first_newline != -1:
            candidate = candidate[first_newline + 1 :]
        if candidate.endswith("```"):
            candidate = candidate[:-3]
        candidate = candidate.strip()

    try:
        parsed = ast.literal_eval(candidate)
    except (SyntaxError, ValueError) as exc:
        raise InvalidFollowupQuestionsError(
            "Follow-up questions response must be a Python list literal of strings."
        ) from exc

    if not isinstance(parsed, list):
        raise InvalidFollowupQuestionsError("Follow-up questions response must be a list.")

    if len(parsed) != 3:
        raise InvalidFollowupQuestionsError("Follow-up questions response must contain exactly 3 items.")

    cleaned_questions: List[str] = []
    for item in parsed:
        if not isinstance(item, str):
            raise InvalidFollowupQuestionsError("Each follow-up question must be a string.")
        cleaned_item = item.strip()
        if not cleaned_item:
            raise InvalidFollowupQuestionsError("Follow-up questions must be non-empty strings.")
        cleaned_questions.append(cleaned_item)

    return cleaned_questions


def _parse_and_validate_patterns_json(raw_text: str) -> Dict[str, Any]:
    if not raw_text or not raw_text.strip():
        raise InvalidLLMJsonError("Patterns response is empty.")

    candidate = raw_text.strip()
    if candidate.startswith("```"):
        first_newline = candidate.find("\n")
        if first_newline != -1:
            candidate = candidate[first_newline + 1 :]
        if candidate.endswith("```"):
            candidate = candidate[:-3]
        candidate = candidate.strip()
        # region agent log
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H3",
                    "location": "controller/text_generation.py:89",
                    "message": "stripped markdown fences from patterns response",
                    "data": {"had_fence": True, "starts_with_brace": candidate.startswith("{")},
                    "timestamp": __import__("time").time_ns() // 1_000_000,
                }) + "\n")
        except Exception:
            pass
        # endregion

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise InvalidLLMJsonError("Patterns response is not valid JSON.") from exc

    if not isinstance(data, dict):
        raise InvalidLLMJsonError("Patterns response must be a JSON object at the top level.")

    required_fields = {
        "hero_summary": str,
        "short_summary": str,
        "quick_insights": list,
        "detailed_summary": str,
    }

    missing_fields = [key for key in required_fields if key not in data]
    if missing_fields:
        raise InvalidLLMJsonError(
            f"Patterns response is missing required field(s): {', '.join(missing_fields)}."
        )

    for field_name, expected_type in required_fields.items():
        if not isinstance(data[field_name], expected_type):
            raise InvalidLLMJsonError(
                f"Patterns response field '{field_name}' must be of type {expected_type.__name__}."
            )

    quick_insights = data["quick_insights"]
    if any(not isinstance(item, str) for item in quick_insights):
        raise InvalidLLMJsonError(
            "Patterns response field 'quick_insights' must be a list of strings."
        )

    return data