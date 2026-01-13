import yaml
import os
from difflib import get_close_matches
from typing import Tuple, Optional, List, Dict

# ─────────────────────────────────────────
# FILE PATHS
PROMPT_DIR           = os.path.join("prompts")
PAIN_POINT_YAML      = os.path.join(PROMPT_DIR, "pain_points_library.yml")
GOD_MODE_YAML        = os.path.join(PROMPT_DIR, "god_mode_prompts.yaml")

# ─────────────────────────────────────────
# LOADERS

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_pain_points(path: str = PAIN_POINT_YAML) -> dict:
    """Flatten all persona-specific pain points into a single list."""
    raw = load_yaml(path)
    flat = {"pain_points": []}

    for section in ["sales", "support", "success"]:
        section_entries = raw.get("pain_points", {}).get(section, [])
        for entry in section_entries:
            if isinstance(entry, dict) and "id" in entry and "keywords" in entry:
                flat["pain_points"].append(entry)
            else:
                print(f"[WARN] Skipping malformed entry in {section}: {entry}")

    return flat

def load_god_mode(path: str = GOD_MODE_YAML) -> dict:
    """
    Flatten all persona prompts into a list under 'god_mode_prompts',
    accepting keys like 'Sales', ' sales ', etc.
    """
    raw = load_yaml(path)
    prompts: List[Dict] = []

    for key, section_entries in raw.items():
        key_norm = key.strip().lower()
        if key_norm not in {"sales", "support", "success"}:
            continue     # skip unknown sections

        if not isinstance(section_entries, list):
            print(f"[WARN] Section '{key}' is not a list, skipping")
            continue

        for prompt in section_entries:
            if isinstance(prompt, dict) and "persona" in prompt:
                prompts.append(prompt)
            else:
                print(f"[WARN] Skipping malformed prompt in section '{key}': {prompt}")

    print(f"[INFO] Loaded {len(prompts)} god‑mode prompts total")
    return {"god_mode_prompts": prompts}

# ─────────────────────────────────────────
# FUZZY MATCHER

def find_best_pain_point(
    user_input: str,
    pain_points_data: dict,
    cutoff: float = 0.6
) -> Tuple[Optional[str], Optional[str]]:
    """Fuzzy match user input to closest pain point keyword."""
    if not user_input.strip():
        return None, None

    all_keywords = []
    keyword_map = {}

    for entry in pain_points_data.get("pain_points", []):
        if not isinstance(entry, dict):
            continue

        pid = entry.get("id", "")
        for kw in entry.get("keywords", []):
            norm_kw = kw.strip().lower()
            all_keywords.append(norm_kw)
            keyword_map[norm_kw] = pid

    close = get_close_matches(user_input.strip().lower(), all_keywords, n=1, cutoff=cutoff)
    if close:
        kw = close[0]
        return keyword_map[kw], kw

    return None, None

# ─────────────────────────────────────────
# PROMPT MATCHING LOGIC

def match_prompts(
    persona: str,
    matched_id: Optional[str],
    matched_keyword: Optional[str],
    god_mode_list: List[Dict],
    fallback: bool = True
) -> List[Dict]:
    """
    Match prompts from the god_mode_list based on persona and pain_point_tags.
    """
    persona_lc = persona.strip().lower()
    kw = (matched_keyword or "").strip().lower()
    pid = (matched_id or "").strip().lower()

    matched = []

    for prompt in god_mode_list:
        if not isinstance(prompt, dict):
            continue
        if prompt.get("persona", "").strip().lower() != persona_lc:
            continue

        tags = prompt.get("pain_point_tags", [])
        if not tags:
            matched.append(prompt)  # wildcard fallback
            continue

        tag_set = set([t.strip().lower() for t in tags])

        print(f"[MATCH DEBUG] Checking Prompt: {prompt.get('id')}")
        print(f"[TAGS] {tag_set}")
        print(f"[TRYING TO MATCH] kw='{kw}', pid='{pid}'")

        if kw in tag_set or pid in tag_set:
            matched.append(prompt)

    if not matched and fallback:
        print("[FALLBACK] No direct match. Using wildcard fallback.")
        matched = [
            p for p in god_mode_list
            if isinstance(p, dict) and p.get("persona", "").strip().lower() == persona_lc
        ]

    return matched

# ─────────────────────────────────────────
# TEST HARNESS

if __name__ == "__main__":
    print("🔧 Running matcher test harness...")
    pain_data = load_pain_points()
    god_data = load_god_mode()
    god_prompts = god_data["god_mode_prompts"]

    # Try a sample query
    input_text = "Pricing too high"
    persona = "Sales"

    pid, kw = find_best_pain_point(input_text, pain_data)
    print(f"[MATCHED] ID: {pid} | Keyword: {kw}")

    results = match_prompts(persona, pid, kw, god_prompts)
    print(f"[RESULT] Found {len(results)} matched prompts.")
    for p in results:
        print("→", p.get("id"))
