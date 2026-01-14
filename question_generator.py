"""
LexIQ Labs – Contextual Question Generator

Purpose:
- Generate up to 2 situational clarification questions
- Questions are dynamic, context-specific, and optional
- Gemini is used ONLY to suggest questions
- LexIQ filters aggressively to preserve speed and relevance
"""

import os
import json
import requests
from typing import List

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)


def generate_questions(
    *,
    customer_message: str,
    persona: str,
    timeout: int = 12,
) -> List[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return []

    prompt = build_prompt(customer_message, persona)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "topP": 0.9,
            "maxOutputTokens": 256,
        },
    }

    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={api_key}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()

        raw_text = (
            data["candidates"][0]["content"]["parts"][0]["text"]
            if data.get("candidates")
            else ""
        )

        questions = extract_questions(raw_text)
        return filter_questions(questions)

    except Exception:
        return []


def build_prompt(customer_message: str, persona: str) -> str:
    return f"""
You are helping draft a professional response.

Given the customer message below, suggest up to TWO clarification questions
that would materially help draft a better response.

RULES:
- Ask only factual or constraint-related questions
- Do NOT ask about emotions
- Do NOT ask "why" questions
- Do NOT suggest solutions
- Do NOT exceed two questions
- Questions must be short and neutral

Persona: {persona}

Customer message:
\"\"\"{customer_message}\"\"\"

Return only the questions, each on a new line.
""".strip()


def extract_questions(text: str) -> List[str]:
    lines = [line.strip("-• \t") for line in text.splitlines()]
    return [line for line in lines if line.endswith("?")]


def filter_questions(questions: List[str]) -> List[str]:
    filtered = []

    for q in questions:
        q_lower = q.lower()

        if len(q.split()) > 20:
            continue
        if "why" in q_lower:
            continue
        if "feel" in q_lower or "emotion" in q_lower:
            continue

        filtered.append(q)

        if len(filtered) == 2:
            break

    return filtered
