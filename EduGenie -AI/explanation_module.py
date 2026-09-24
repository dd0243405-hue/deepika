import os

from gemini_client import generate_text


# ---------------------------------------------------------
# Gemini explanation
# ---------------------------------------------------------

def _gemini_explanation(concept: str) -> str:

    prompt = f"""
Explain the following concept to a beginner.

CONCEPT:
{concept}

Use this structure:

1. Simple definition
2. How it works
3. Small example
4. Key takeaway

Use simple, beginner-friendly language.

Do not make the explanation unnecessarily long.
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1000
    )


# ---------------------------------------------------------
# Local LaMini-Flan-T5 explanation
# ---------------------------------------------------------

def _local_explanation(concept: str) -> str:

    try:

        from transformers import pipeline

    except ImportError:

        raise RuntimeError(
            "Local explanation requires transformers and torch. "
            "Install them using: pip install transformers torch"
        )

    model_name = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    generator = pipeline(
        "text2text-generation",
        model=model_name
    )

    prompt = (
        "Explain this concept simply for a beginner. "
        "Give a definition, explain how it works, "
        "provide a small example, and finish with "
        "a key takeaway.\n\n"
        f"Concept: {concept}"
    )

    result = generator(
        prompt,
        max_new_tokens=350,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


# ---------------------------------------------------------
# Public function
# ---------------------------------------------------------

def explain_concept(concept: str) -> str:

    provider = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    ).lower()

    if provider == "local":

        return _local_explanation(
            concept
        )

    return _gemini_explanation(
        concept
    )