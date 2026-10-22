"""
llm.py — Single entry point for all LLM calls.

Powered by Groq. The API key is read securely from the .env file in the backend.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Please ensure it is present in your .env file."
    )

client = Groq(api_key=API_KEY)

# Primary fast 120B model on Groq with fallback
PRIMARY_MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "qwen/qwen3.8-27b"


def call_llm(role: str, task: str, *, temperature: float = 0.5) -> str:
    """Call the LLM with a system-level *role* and a user *task*.

    Parameters
    ----------
    role : str
        System prompt that sets agent persona and constraints.
    task : str
        User-facing prompt or agent input.
    temperature : float
        Sampling temperature (0 = deterministic, 1 = creative).

    Returns
    -------
    str
        The model's text response.
    """
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": task},
    ]

    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )
        return response.choices[0].message.content or ""
    except Exception:
        # Fallback to secondary model if primary encounters rate limit or availability issue
        response = client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )
        return response.choices[0].message.content or ""
