# blender.py

import random
import textwrap
from typing import Dict, Optional


def blend_prompt(
    pain_point: Dict,
    goal: Optional[str],
    god_mode_prompt: Dict,
    tone: str = "safe"
) -> Dict:
    """
    Blend pain point + goal with a God Mode prompt.

    EXPECTED god_mode_prompt SCHEMA:
    {
        id: str,
        persona: str,
        fingerprint_id: str,
        prompts: {
            safe: [str, ...],
            direct: [str, ...]
        }
    }
    """

    # ─────────────────────────────────────────
    # Safety checks

    prompts_block = god_mode_prompt.get("prompts", {})
    if not isinstance(prompts_block, dict):
        raise ValueError("Invalid God Mode prompt: missing 'prompts' dict")

    tone = tone.lower().strip()
    variants = prompts_block.get(tone)

    if not variants:
        # Hard fallback → SAFE
        variants = prompts_block.get("safe", [])
        tone = "safe"

    if not variants:
        raise ValueError(
            f"No usable prompt variants found for prompt ID {god_mode_prompt.get('id')}"
        )

    # ─────────────────────────────────────────
    # Select variant

    selected_prompt = random.choice(variants)

    # ─────────────────────────────────────────
    # Build metadata

    fingerprint_id = god_mode_prompt.get("fingerprint_id", "unknown")
    pain_text = pain_point.get("text", "a customer concern")
    goal_text = goal.strip() if goal else "respond appropriately"

    readable_intro = (
        f"🧠 Handling **{pain_text}**\n"
        f"🎯 Goal: {goal_text}\n"
        f"🎚 Tone: {tone.upper()}"
    )

    # ─────────────────────────────────────────
    # Final ChatGPT-ready prompt

    chatgpt_prompt = textwrap.dedent(f"""
        CONTEXT:
        The customer is experiencing the following issue:
        "{pain_text}"

        OBJECTIVE:
        {goal_text}

        INSTRUCTIONS:
        {selected_prompt}

        <!-- fingerprint_id: {fingerprint_id} -->
    """)

    return {
        "readable_intro": readable_intro.strip(),
        "chatgpt_prompt": chatgpt_prompt.strip(),
        "fingerprint_id": fingerprint_id,
        "tone_used": tone
    }
