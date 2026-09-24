from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    prompt = f"""
Create a step-by-step learning path
for the following topic.

TOPIC:
{topic}

Structure your answer using:

1. Goal
2. Beginner foundations
3. Intermediate topics
4. Advanced topics
5. Suggested timeline
6. Practice and projects
7. Recommended resource types

Resource types can include:

- Videos
- Articles
- Books
- Documentation
- Practice exercises
- Projects

The learner should progress from basic
concepts to advanced concepts.

Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1600
    )