"""
LexIQ Labs – Pain Point Matcher (v2)

Role:
- Provide a SECONDARY signal to guide God Mode selection
- Never block response generation
- Never dictate wording
- Operates deterministically
"""

from typing import Dict, List, Optional, Tuple
import re


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def score_match(text: str, tags: List[str]) -> int:
    """
    Simple frequency-based scoring.
    We keep this lightweight on purpose.
    """
    score = 0
    for tag in tags:
        if tag in text:
            score += 1
    return score


def match_pain_point(
    *,
    customer_message: str,
    pain_points: List[Dict],
    min_score: int = 2
) -> Dict:
    """
    Attempts to find a relevant pain point.

    Returns:
    {
        "matched": bool,
        "pain_point": Dict | None,
        "confidence": float,
        "reason": str
    }
    """

    text = normalize(customer_message)

    best_match: Optional[Tuple[Dict, int]] = None

    for pain_point in pain_points:
        tags = pain_point.get("pain_point_tags", [])
        score = score_match(text, tags)

        if score >= min_score:
            if not best_match or score > best_match[1]:
                best_match = (pain_point, score)

    # No meaningful match
    if not best_match:
        return {
            "matched": False,
            "pain_point": None,
            "confidence": 0.0,
            "reason": "No strong lexical overlap with known pain points."
        }

    pain_point, score = best_match
    confidence = min(score / (len(pain_point.get("pain_point_tags", [])) or 1), 1.0)

    return {
        "matched": True,
        "pain_point": pain_point,
        "confidence": round(confidence, 2),
        "reason": f"Matched on {score} keyword signals."
    }


def select_god_mode_prompt(
    *,
    persona: str,
    god_mode_prompts: List[Dict],
    pain_point_match: Dict
) -> Dict:
    """
    Selects the most appropriate God Mode prompt.

    Priority:
    1. Persona match
    2. Pain point tag overlap (if available)
    3. Wildcard fallback
    """

    candidates = [
        p for p in god_mode_prompts
        if p.get("persona") == persona
    ]

    # If pain point matched, try to align tags
    if pain_point_match.get("matched"):
        pain_tags = set(pain_point_match["pain_point"].get("pain_point_tags", []))

        scored = []
        for prompt in candidates:
            prompt_tags = set(prompt.get("pain_point_tags", []))
            overlap = len(pain_tags & prompt_tags)
            scored.append((prompt, overlap))

        scored.sort(key=lambda x: x[1], reverse=True)

        if scored and scored[0][1] > 0:
            return scored[0][0]

    # Fallback: wildcard prompt
    for prompt in candidates:
        if "_wildcard" in prompt.get("pain_point_tags", []):
            return prompt

    # Absolute fallback: first persona prompt
    return candidates[0] if candidates else {}
