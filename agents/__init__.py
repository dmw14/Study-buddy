"""agents package - one module per agent role."""

from .researcher import researcher
from .summarizer import summarizer
from .quiz_generator import quiz_generator
from .evaluator import evaluator

__all__ = ["researcher", "summarizer", "quiz_generator", "evaluator"]
