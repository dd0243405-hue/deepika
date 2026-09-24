import json
from typing import TypedDict

from gemini_client import generate_json


# ---------------------------------------------------------
# Quiz structure
# ---------------------------------------------------------

class QuizQuestion(TypedDict):

    question: str
    options: list[str]
    correct_answer: str
    explanation: str


# ---------------------------------------------------------
# JSON schema
# ---------------------------------------------------------

QUIZ_SCHEMA = list[QuizQuestion]


# ---------------------------------------------------------
# Clean Markdown JSON blocks
# ---------------------------------------------------------

def clean_json_block(text: str) -> str:

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

def generate_quiz(
    text: str
) -> list[QuizQuestion]:

    prompt = f"""
Generate exactly 3 multiple-choice questions
from the educational material below.

Requirements:

1. Exactly 3 questions.
2. Each question must contain exactly 4 options.
3. There must be only one correct answer.
4. The correct_answer must exactly match one
   of the four options.
5. Include a short explanation for each answer.
6. Questions must be based only on the supplied
   educational material.
7. Make the distractors plausible.

EDUCATIONAL MATERIAL:

{text}
"""

    raw = generate_json(
        prompt,
        QUIZ_SCHEMA
    )

    cleaned = clean_json_block(
        raw
    )

    try:

        data = json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Gemini returned invalid quiz JSON: {exc}"
        )

    # -----------------------------------------------------
    # Validate top-level structure
    # -----------------------------------------------------

    if not isinstance(data, list):

        raise ValueError(
            "Quiz output must be a list."
        )

    if len(data) != 3:

        raise ValueError(
            "Quiz generation did not return exactly 3 questions."
        )

    # -----------------------------------------------------
    # Validate every question
    # -----------------------------------------------------

    for item in data:

        if not isinstance(item, dict):

            raise ValueError(
                "Invalid quiz question."
            )

        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        for field in required_fields:

            if field not in item:

                raise ValueError(
                    f"Missing quiz field: {field}"
                )

        options = item["options"]

        if not isinstance(options, list):

            raise ValueError(
                "Quiz options must be a list."
            )

        if len(options) != 4:

            raise ValueError(
                "Each quiz question must contain exactly 4 options."
            )

        if item["correct_answer"] not in options:

            raise ValueError(
                "Correct answer must exactly match one option."
            )

    return data