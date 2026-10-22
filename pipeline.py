"""
pipeline.py — Orchestrates the four agents.

Flow:
  User input → Researcher → Summarizer → Quiz Generator ⇄ Evaluator → Output

The Evaluator can send the quiz back for regeneration up to MAX_RETRIES times.
"""

import time
from dataclasses import dataclass, field
from agents import researcher, summarizer, quiz_generator, evaluator

MAX_RETRIES = 2


@dataclass
class PipelineResult:
    """Everything the pipeline produces in a single run."""

    topic: str
    mode: str                          # "topic" or "text"
    facts: str = ""
    notes: str = ""
    quiz: list[dict] = field(default_factory=list)
    review: dict = field(default_factory=dict)
    attempts: int = 0
    elapsed_seconds: float = 0.0
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "mode": self.mode,
            "facts": self.facts,
            "notes": self.notes,
            "quiz": self.quiz,
            "review": self.review,
            "attempts": self.attempts,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "error": self.error,
        }


def run_pipeline(
    topic: str,
    *,
    source_text: str | None = None,
    max_retries: int = MAX_RETRIES,
    num_questions: int = 5,
) -> PipelineResult:
    """Run the full study-buddy 4-agent pipeline."""
    mode = "text" if source_text else "topic"
    result = PipelineResult(topic=topic, mode=mode)
    start = time.time()

    try:
        # ── Agent 1: Researcher ─────────────────────────────────
        result.facts = researcher(topic, source_text=source_text)

        # ── Agent 2: Summarizer ─────────────────────────────────
        result.notes = summarizer(result.facts, topic=topic)

        # ── Agent 3 & 4: Quiz Generator ⇄ Evaluator ─────────────
        feedback = None
        for attempt in range(1, max_retries + 2):
            result.attempts = attempt

            result.quiz = quiz_generator(
                result.notes,
                num_questions=num_questions,
                feedback=feedback,
            )

            result.review = evaluator(result.notes, result.quiz)

            if result.review.get("passed", False):
                break

            # Send problems back to Quiz Generator for retry
            problems = result.review.get("problems", [])
            feedback = "\n".join(f"- {p}" for p in problems) if problems else None

    except Exception as exc:
        result.error = str(exc)

    result.elapsed_seconds = time.time() - start
    return result
