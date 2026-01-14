"""
LexIQ Labs – Voice Profile

Purpose:
- Capture and apply a user’s writing style as stable constraints
- One-time analysis, reusable across sessions
- Behavioural style, not linguistic imitation
"""

from typing import Dict, List, Optional
import os
import json
import requests

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def create_voice_profile(
    *,
    writing_samples: List[str],
    timeout: int = 20,
) -> Optional[Dict]:
    """
    Analyze user writing samples and extract voice constraints.
    Returns a dict describing stable style traits.
    """
    if not writing_samples:
        return None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = build_analysis_prompt(writing_samples)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
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

        raw = (
            data["candidates"][0]["content"]["parts"][0]["text"]
            if data.get("candidates")
            else ""
        )

        return parse_voice_profile(raw)

    except Exception:
        return None


def build_analysis_prompt(samples: List[str]) -> str:
    joined = "\n\n---\n\n".join(samples)

    return f"""
You are analyzing writing style.

TASK:
Extract stable writing style traits from the samples below.
Summarize them as constraints, not examples.

RULES:
- Do NOT rewrite or improve the text
- Do NOT invent traits not supported by the samples
- Do NOT quote sentences from the samples
- Keep traits behavioural and high-level
- Use clear, neutral language

Return the result strictly as JSON with keys such as:
tone, formality, sentence_length, directness, apology_tendency,
warmth, closing_style

WRITING SAMPLES:
\"\"\"{joined}\"\"\"
""".strip()


def parse_voice_profile(text: str) -> Optional[Dict]:
    """
    Attempt to extract JSON from Gemini output safely.
    """
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return None
        return json.loads(text[start : end + 1])
    except Exception:
        return None


def apply_voice_constraints(
    *,
    response_contract: Dict,
    voice_profile: Optional[Dict],
) -> Dict:
    """
    Inject voice constraints into an existing response contract.
    """
    if not voice_profile:
        return response_contract

    response_contract["voice_constraints"] = voice_profile
    return response_contract

