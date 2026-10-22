"""
Agent 2: Notes Summarizer

Job: Takes raw facts from the Researcher and produces well-structured,
exam-ready study notes (like the "note-taker friend" in a study group).
"""

from llm import call_llm

ROLE = (
    "You are an expert note-taker who creates clear, well-organized study notes. "
    "Use headings, sub-headings, and bullet points. "
    "Highlight key terms in bold using markdown syntax. "
    "Keep language simple, precise, and student-friendly."
)


def summarizer(facts: str, topic: str = "") -> str:
    """Convert raw facts into structured study notes."""
    heading = f" on **{topic}**" if topic else ""
    task = (
        f"Turn the following facts into well-structured study notes{heading}.\n\n"
        f"Requirements:\n"
        f"- Use clear markdown headings (#, ##, ###)\n"
        f"- Bold key terms and definitions (**term**)\n"
        f"- Organize into logical sections (Core Concepts, Key Mechanisms, Significance)\n"
        f"- Add a brief introduction and summary\n\n"
        f"Facts:\n{facts}"
    )
    return call_llm(ROLE, task, temperature=0.4)
