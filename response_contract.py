"""
LexIQ Labs – Response Contract

Purpose:
- Define and enforce the mandatory response structure
- Act as the canonical schema between Blender and Gemini Refiner
- Ensure psychological safety, clarity, and consistency
"""

from typing import Dict, List
from datetime import datetime


def build_response_contract(
    *,
    customer_message: str,
    empathy_summary: str,
    clarifications: Dict[str, str],
    user_intent: str,
    persona: str,
    god_mode_prompt: Dict,
    voice_profile: Dict | None = None,
) -> Dict:
    return {
        "meta": {
            "generated_at": datetime.utcnow().isoformat(),
            "persona": persona,
            "god_mode_id": god_mode_prompt.get("id"),
            "fingerprint_id": god_mode_prompt.get("fingerprint_id"),
        },
        "input_context": {
            "customer_message": customer_message,
            "empathy_summary": empathy_summary,
            "clarifications": clarifications or {},
            "user_intent": user_intent,
        },
        "response_structure": mandatory_structure(),
        "psychology_constraints": {
            "principles": extract_psychology_principles(god_mode_prompt)
        },
        "voice_constraints": voice_profile or {},
        "generation_rules": {
            "must_follow_structure": True,
            "must_respect_user_intent": True,
            "must_respect_psychology": True,
            "no_policy_invention": True,
            "no_unverified_promises": True,
            "no_emotional_manipulation": True,
        },
    }


def mandatory_structure() -> List[Dict[str, str]]:
    return [
        {
            "section": "reconfirmation",
            "instruction": (
                "Subtly restate the customer’s issue or goal using their language. "
                "Do not sound like a summary or repeat verbatim."
            ),
        },
        {
            "section": "acknowledgement",
            "instruction": (
                "Acknowledge the customer’s concern or frustration without exaggeration. "
                "Avoid defensiveness or over-apologizing."
            ),
        },
        {
            "section": "solution_or_next_steps",
            "instruction": (
                "Clearly outline the response, position, or next step. "
                "Be specific and realistic. Do not overpromise."
            ),
        },
        {
            "section": "assurance",
            "instruction": (
                "Close with reassurance, ownership, or partnership. "
                "Reduce uncertainty about what happens next."
            ),
        },
    ]


def extract_psychology_principles(god_mode_prompt: Dict) -> List[str]:
    principles: List[str] = []

    if "psychology_used" in god_mode_prompt:
        principles.append(
            f"Apply psychological framing based on: {god_mode_prompt['psychology_used']}"
        )

    if "inspired_by" in god_mode_prompt:
        principles.append(
            f"Maintain stance inspired by: {god_mode_prompt['inspired_by']}"
        )

    prompts = god_mode_prompt.get("prompts", {})

    if "safe" in prompts:
        principles.append(
            "Prioritize emotional safety: validate concerns, avoid pressure or escalation."
        )

    if "direct" in prompts:
        principles.append(
            "Maintain clarity and firmness when appropriate; avoid unnecessary hedging."
        )

    principles.extend(
        [
            "Do not blame the customer.",
            "Do not sound defensive.",
            "Do not transfer ownership unnecessarily.",
            "Prioritize clarity over persuasion.",
        ]
    )

    return principles
