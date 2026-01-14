"""
LexIQ Labs – Blender Engine

Purpose:
- Compose a RESPONSE CONTRACT (not final prose)
- Enforce psychological safety via God Mode
- Respect user intent and writing style
- Prepare a structured instruction block for optional Gemini refinement

This file MUST NOT generate final user-facing text.
"""

from typing import Dict, List, Optional
from datetime import datetime


def blend(
    *,
    customer_message: str,
    persona: str,
    empathy_summary: str,
    clarifications: Optional[Dict[str, str]],
    user_intent: str,
    god_mode_prompt: Dict,
    voice_profile: Optional[Dict] = None,
) -> Dict:
    """
    Create a structured response contract.

    Returns a dictionary that downstream systems (Gemini or fallback)
    can use to draft a psychologically correct, on-brand response.
    """

    contract = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat(),
            "persona": persona,
            "fingerprint_id": god_mode_prompt.get("fingerprint_id"),
        },

        "input_context": {
            "customer_message": customer_message,
            "empathy_summary": empathy_summary,
            "clarifications": clarifications or {},
            "user_intent": user_intent,
        },

        "response_structure": {
            "mandatory_sections": [
                {
                    "section": "reconfirmation",
                    "instruction": (
                        "Subtly reflect the customer’s situation or goal in their own terms. "
                        "Do not sound like a summary or repeat verbatim."
                    ),
                },
                {
                    "section": "acknowledgement",
                    "instruction": (
                        "Acknowledge the customer’s emotion or concern without exaggeration. "
                        "Do not invalidate or deflect responsibility."
                    ),
                },
                {
                    "section": "solution_or_next_steps",
                    "instruction": (
                        "Clearly outline the proposed action, position, or next step. "
                        "Be concrete and realistic. Do not overpromise."
                    ),
                },
                {
                    "section": "assurance",
                    "instruction": (
                        "End with reassurance, ownership, or partnership. "
                        "Reduce uncertainty about what happens next."
                    ),
                },
            ]
        },

        "psychology_constraints": {
            "god_mode_id": god_mode_prompt.get("id"),
            "principles": extract_god_mode_principles(god_mode_prompt),
        },

        "voice_constraints": voice_profile or {},

        "generation_rules": {
            "must_follow_structure": True,
            "must_respect_user_intent": True,
            "must_respect_psychology": True,
            "no_policy_invention": True,
            "no_emotional_manipulation": True,
            "no_unverified_promises": True,
        },
    }

    return contract


def extract_god_mode_principles(god_mode_prompt: Dict) -> List[str]:
    """
    Extract psychology principles from a God Mode prompt.

    We do NOT inject example sentences here.
    We extract intent, stance, and psychological rules.
    """

    principles = []

    # Psychology used (if present)
    if "psychology_used" in god_mode_prompt:
        principles.append(
            f"Apply psychological framing based on: {god_mode_prompt['psychology_used']}"
        )

    # Inspired by (optional metadata)
    if "inspired_by" in god_mode_prompt:
        principles.append(
            f"Maintain stance inspired by: {god_mode_prompt['inspired_by']}"
        )

    # Safe / Direct guidance (conceptual, not textual)
    prompts = god_mode_prompt.get("prompts", {})

    if "safe" in prompts:
        principles.append(
            "Maintain emotional safety: validate feelings, avoid pressure, avoid escalation."
        )

    if "direct" in prompts:
        principles.append(
            "Maintain clarity and firmness when appropriate: avoid hedging, move toward resolution."
        )

    # Universal guardrails
    principles.extend(
        [
            "Do not blame the customer.",
            "Do not sound defensive.",
            "Do not transfer ownership unnecessarily.",
            "Prioritize clarity over persuasion.",
        ]
    )

    return principles
