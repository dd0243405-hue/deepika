import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# Load .env automatically
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_client():

    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    if not api_key:

        raise RuntimeError(
            "Gemini API key is missing. "
            "Set GEMINI_API_KEY in your .env file."
        )

    return genai.Client(
        api_key=api_key
    )


# ---------------------------------------------------------
# Generate normal text
# ---------------------------------------------------------

def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1200
) -> str:

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction
    )

    response = get_client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )

    text = response.text

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# ---------------------------------------------------------
# Generate structured JSON
# ---------------------------------------------------------

def generate_json(
    prompt: str,
    schema
):

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=1800,
        response_mime_type="application/json",
        response_schema=schema
    )

    response = get_client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty JSON response."
        )

    return response.text