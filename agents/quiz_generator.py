"""
Agent 3: Quiz Generator

Job: Generates a set of multiple-choice questions (MCQs) in JSON format
based on the study notes. On retries, it receives feedback from the
Evaluator and improves the questions accordingly.
"""

import json
import re
from llm import call_llm

ROLE = (
    "You are a quiz-writing expert. "
    "Create challenging but fair multiple-choice questions that test "
    "deep conceptual understanding, not just rote memorization. "
    "You MUST reply with ONLY a valid JSON array — no markdown code fences, "
    "no commentary, no conversational text."
)

JSON_SCHEMA_HINT = """
[
  {
    "question": "What is ...?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A",
    "explanation": "Brief explanation of why this is correct."
  }
]
""".strip()


def _extract_json(text: str) -> list:
    """Best-effort extraction of a JSON array from LLM output."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse quiz JSON from LLM response: {text[:200]}")


def quiz_generator(
    notes: str,
    *,
    num_questions: int = 5,
    feedback: str | None = None,
) -> list[dict]:
    """Generate MCQs from study notes."""
    task = (
        f"Based on the study notes below, generate exactly {num_questions} "
        f"multiple-choice questions.\n\n"
        f"Each question must have 4 options (A–D) and one correct answer.\n\n"
        f"Reply ONLY with a JSON array matching this schema:\n{JSON_SCHEMA_HINT}\n\n"
        f"--- STUDY NOTES ---\n{notes}\n--- END NOTES ---"
    )

    if feedback:
        task += (
            f"\n\n⚠️ A reviewer found these problems with your previous attempt. "
            f"Fix them strictly in this attempt:\n{feedback}"
        )

    raw = call_llm(ROLE, task, temperature=0.5)
    return _extract_json(raw)
