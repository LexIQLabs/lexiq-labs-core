# gemini_refiner.py

import os
import requests
import re
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)

# ─────────────────────────────────────────
# Hard safety checks

FORBIDDEN_PHRASES = [
    "we guarantee",
    "i promise",
    "refund",
    "compensation",
    "legal action",
    "policy states",
    "terms and conditions"
]

MAX_WORDS = 120


def _violates_constraints(text: str) -> bool:
    """Check if Gemini output violates hard constraints."""
    text_lc = text.lower()

    if len(text.split()) > MAX_WORDS:
        return True

    for phrase in FORBIDDEN_PHRASES:
        if phrase in text_lc:
            return True

    return False


# ─────────────────────────────────────────
# Gemini refiner

def refine_instruction(
    instruction_block: str,
    timeout: int = 8
) -> Optional[str]:
    """
    Uses Gemini ONLY to verbalize a structured instruction block
    into a polished, customer-facing reply.

    Returns:
    - refined text (str) if successful and safe
    - None if Gemini fails or violates constraints
    """

    if not GEMINI_API_KEY:
        print("[Gemini Refiner] Missing API key.")
        return None

    system_prompt = (
        "You are a language refiner.\n\n"
        "Rewrite the instruction below into a customer-facing reply.\n\n"
        "RULES:\n"
        "- Do NOT add new ideas\n"
        "- Do NOT change intent or tone\n"
        "- Do NOT add promises, policies, or guarantees\n"
        "- Do NOT exceed 120 words\n"
        "- Preserve emotional stance exactly\n\n"
        "Return ONLY the final reply.\n\n"
        "INSTRUCTION:\n"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": system_prompt + instruction_block
                    }
                ]
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
            print("[Gemini Refiner] API error:", response.text)
            return None

        result = (
            response.json()
            .get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not result:
            return None

        if _violates_constraints(result):
            print("[Gemini Refiner] Constraint violation detected.")
            return None

        return result

    except Exception as e:
        print("[Gemini Refiner] Exception:", str(e))
        return None

