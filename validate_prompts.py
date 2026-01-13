import yaml
import os

GOD_MODE_PATH = os.path.join("prompts", "god_mode_prompts.yaml")

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def validate_prompts():
    data = load_yaml(GOD_MODE_PATH)
    issues_found = False

    for section in ["sales", "support", "success"]:
        prompts = data.get(section, [])
        for entry in prompts:
            eid = entry.get("id", "UNKNOWN")
            problems = []

            if not entry.get("persona"):
                problems.append("missing 'persona'")

            if "pain_point_tags" not in entry:
                problems.append("missing 'pain_point_tags'")
            elif not entry["pain_point_tags"]:
                problems.append("empty 'pain_point_tags'")

            if not isinstance(entry.get("prompts", {}), dict):
                problems.append("missing or invalid 'prompts'")
            else:
                if not entry["prompts"].get("safe"):
                    problems.append("missing 'prompts.safe'")
                if not entry["prompts"].get("direct"):
                    problems.append("missing 'prompts.direct'")

            if problems:
                issues_found = True
                print(f"[⚠️] {eid} ({section}): {', '.join(problems)}")

    if not issues_found:
        print("✅ All prompts are valid.")

if __name__ == "__main__":
    validate_prompts()
