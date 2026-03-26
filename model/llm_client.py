import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
_client = None


def has_api_key() -> bool:
    load_dotenv(override=True)
    return bool(os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY"))


def get_client():
    global _client

    if _client is not None:
        return _client

    load_dotenv(override=True)
    api_key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is missing.")

    _client = genai.Client(api_key=api_key)
    return _client


def llm_connect() -> bool:
    try:
        client = get_client()
        # Minimal connectivity test
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with the word OK."
        )
        return bool(response.text)
    except Exception:
        return False


def generate_text(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    text = getattr(response, "text", None)
    if not text:
        raise ValueError("LLM returned an empty response.")

    return text.strip()