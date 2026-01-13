# time_travel.py

import os
import requests
from typing import List, Dict, Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)

MAX_SIMULATED_WORDS = 40


def _call_gemini(prompt: str, timeout: int = 8) -> Optional[str]:
    """Internal helper to call Gemini safely."""
    if not GEMINI_API_KEY:
        return None

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=timeout
        )

        if response.status_code != 200:
            return None

        return (
            response.json()
            .get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

    except Exception:
        return None


# ─────────────────────────────────────────
# Public API

def simulate_customer_reaction(
    customer_message: str,
    reply_text: str
) -> Optional[str]:
    """
    Simulates a likely customer follow-up message
    after receiving the given reply.

    This is NOT a prediction, only a plausible reaction.
    """

    prompt = f"""
You are simulating a customer's likely NEXT reply.

CONTEXT:
Original customer message:
"{customer_message}"

Agent reply:
"{reply_text}"

RULES:
- Respond as the customer
- Keep under {MAX_SIMULATED_WORDS} words
- Do not invent new issues
- Reflect emotional direction only
- Do not explain your reasoning

Return ONLY the simulated customer reply.
"""

    return _call_gemini(prompt)


def score_emotional_direction(simulated_reply: str) -> Dict:
    """
    Lightweight emotional scoring without LLMs.
    Positive = calming / resolving
    Negative = escalating
    """

    if not simulated_reply:
        return {"score": 0, "direction": "neutral"}

    text = simulated_reply.lower()

    positive_markers = [
        "thanks", "okay", "understood", "makes sense",
        "appreciate", "sounds good", "fine", "got it"
    ]

    negative_markers = [
        "still", "not acceptable", "angry", "frustrated",
        "doesn't help", "unhappy", "issue remains", "why"
    ]

    score = 0

    for p in positive_markers:
        if p in text:
            score += 1

    for n in negative_markers:
        if n in text:
            score -= 1

    if score > 0:
        direction = "improving"
    elif score < 0:
        direction = "worsening"
    else:
        direction = "neutral"

    return {
        "score": score,
        "direction": direction
    }


def time_travel_preview(
    customer_message: str,
    reply_text: str
) -> Dict:
    """
    Full Time-Travel™ simulation.
    Returns the simulated reply and emotional direction.
    """

    simulated = simulate_customer_reaction(
        customer_message,
        reply_text
    )

    if not simulated:
        return {
            "simulated_reply": None,
            "direction": "unknown",
            "note": "Simulation unavailable"
        }

    sentiment = score_emotional_direction(simulated)

    return {
        "simulated_reply": simulated,
        "direction": sentiment["direction"],
        "score": sentiment["score"]
    }
