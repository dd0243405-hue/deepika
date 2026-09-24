from gemini_client import generate_text


SYSTEM = """
You are EduGenie, a helpful educational assistant.

Your job is to help students understand academic
and general educational questions.

Rules:

1. Answer accurately.
2. Use simple language.
3. Give the direct answer first.
4. Explain the reasoning when useful.
5. If a question is ambiguous, clearly mention the ambiguity.
6. Do not invent citations.
7. Do not invent facts.
8. Keep answers concise but useful.
"""


def answer_question(question: str) -> str:

    prompt = f"""
Answer the student's question.

QUESTION:
{question}

Give the direct answer first.

Then provide a short explanation when useful.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.2,
        max_output_tokens=900
    )