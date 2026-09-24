from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational text
in simple and easy-to-understand language.

Requirements:

1. Preserve the important facts.
2. Preserve definitions.
3. Preserve important relationships.
4. Preserve important conclusions.
5. Do not add information that is not present.
6. Make the summary useful for quick revision.

TEXT:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1000
    )