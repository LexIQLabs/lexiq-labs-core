"""
LexIQ Labs – Gemini Refiner

Purpose:
- Refine language ONLY
- Respect response contract, God Mode psychology, and voice profile
- Never decide strategy or structure
- Fail gracefully if Gemini is unavailable
"""

import os
import json
import requests
from typing import Dict, Optional

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def refine_response(
    *,
    response_contract: Dict,
    temperature: float = 0.4,
    timeout: int = 15,
) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = build_prompt(response_contract)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "topP": 0.9,
            "maxOutputTokens": 512,
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

        return (
            data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if data.get("candidates")
            else None
        )

    except Exception:
        return None


def build_prompt(contract: Dict) -> str:
    return f"""
You are refining a customer-facing response.

IMPORTANT RULES:
- Do NOT change strategy
- Do NOT invent policies, refunds, or promises
- Do NOT remove required structure
- Follow the constraints exactly

---

CONTEXT:
Customer message:
\"\"\"{contract['input_context']['customer_message']}\"\"\"

Empathy summary:
{contract['input_context']['empathy_summary']}

Clarifications:
{json.dumps(contract['input_context'].get('clarifications', {}), indent=2)}

User intent:
{contract['input_context']['user_intent']}

---

RESPONSE STRUCTURE (MANDATORY):
1. Subtle reconfirmation of the issue or goal
2. Acknowledgement of the customer’s concern
3. Clear solution or next steps
4. Assurance or ownership

---

PSYCHOLOGICAL CONSTRAINTS:
{chr(10).join('- ' + p for p in contract['psychology_constraints']['principles'])}

---

VOICE CONSTRAINTS:
{json.dumps(contract.get('voice_constraints', {}), indent=2)}

---

Write a single, natural response that satisfies all of the above.
Do not label sections.
Do not mention analysis.
""".strip()

