"""
Agent 4: Evaluator

Job: Reviews the generated quiz against the study notes.
Returns a structured verdict: score (1–10) and a list of problems.
If the score is below the threshold, the pipeline retries quiz generation.
"""

import json
import re
from llm import call_llm

ROLE = (
    "You are a strict academic reviewer. "
    "You check quizzes for factual accuracy against the notes, question clarity, and fairness. "
    "You MUST reply with ONLY valid JSON — no markdown fences, no extra text."
)

PASS_THRESHOLD = 7  # score >= this means the quiz passes


def _extract_json(text: str) -> dict:
    """Best-effort extraction of a JSON object from LLM output."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse evaluator JSON from LLM response: {text[:200]}")


def evaluator(notes: str, quiz: list[dict]) -> dict:
    """Score the quiz against the notes."""
    quiz_text = json.dumps(quiz, indent=2)

    task = (
        "Compare the quiz questions below against the study notes.\n"
        "Check for:\n"
        "  1. Factual accuracy — are answers directly backed by the notes?\n"
        "  2. Clarity — are questions unambiguous?\n"
        "  3. Coverage — do questions cover the main ideas from the notes?\n"
        "  4. Option quality — are incorrect options plausible distractors?\n\n"
        f"--- STUDY NOTES ---\n{notes}\n--- END NOTES ---\n\n"
        f"--- QUIZ ---\n{quiz_text}\n--- END QUIZ ---\n\n"
        'Reply ONLY with JSON: {"score": <1-10>, "problems": ["issue 1", ...]}\n'
        "If there are no problems, return an empty list for problems."
    )

    result = _extract_json(call_llm(ROLE, task, temperature=0.2))
    result.setdefault("score", 0)
    result.setdefault("problems", [])
    result["passed"] = result["score"] >= PASS_THRESHOLD

    return result
