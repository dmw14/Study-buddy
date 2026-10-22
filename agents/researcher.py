"""
Agent 1: Topic Researcher

Job: Gathers key facts about a topic (like the "researcher friend" in a study group).
- Topic mode: uses LLM's built-in knowledge to list facts.
- Text mode:  extracts the most important facts from user-provided text.
"""

from llm import call_llm

ROLE = (
    "You are a careful, accurate academic researcher. "
    "Your job is to identify and list the most important facts about a topic. "
    "Present each fact as a concise bullet point. "
    "Do NOT add opinions, filler, or preamble — only verifiable facts."
)


def researcher(topic: str, source_text: str | None = None) -> str:
    """Return 8–10 key facts as bullet points."""
    if source_text:
        task = (
            f"Topic: {topic}\n\n"
            f"Extract the 8–10 most important facts from the following text. "
            f"Present them as bullet points.\n\n"
            f"--- BEGIN TEXT ---\n{source_text}\n--- END TEXT ---"
        )
    else:
        task = (
            f"List 8–10 key facts about the following topic. "
            f"Be accurate and concise.\n\nTopic: {topic}"
        )

    return call_llm(ROLE, task, temperature=0.3)
