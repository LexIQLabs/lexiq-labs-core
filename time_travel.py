"""
LexIQ Labs – Time Travel Simulator

Purpose:
- Simulate a likely next customer response
- Forecast emotional direction after sending a drafted reply
- Assist reflection, not decision-making
- Optional, non-blocking, Gemini-assisted
"""

import os
import json
import requests
from typing import Dict, Optional

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def simulate_time_travel(
    *,
    customer_message: str,
    drafted_response: str,
    persona: str,
    timeout: int = 15,
) -> Optional[Dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = build_prompt(customer_message, drafted_response, persona)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.6,
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

        raw = (
            data["candidates"][0]["content"]["parts"][0]["text"]
            if data.get("candidates")
            else ""
        )

        return parse_simulation(raw)

    except Exception:
        return None


def build_prompt(customer_message: str, drafted_response: str, persona: str) -> str:
    return f"""
You are simulating a possible next customer reply.

CONTEXT:
Original customer message:
\"\"\"{customer_message}\"\"\"

Drafted response:
\"\"\"{drafted_response}\"\"\"

Persona: {persona}

TASK:
- Predict one plausible next customer reply
- Keep it realistic and concise
- Reflect emotional direction (improving, neutral, or worsening)

OUTPUT FORMAT (JSON ONLY):
{{
  "simulated_reply": "...",
  "emotional_direction": "improving | neutral | worsening"
}}

Do not explain your reasoning.
""".strip()


def parse_simulation(text: str) -> Optional[Dict]:
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return None
        return json.loads(text[start : end + 1])
    except Exception:
        return None

