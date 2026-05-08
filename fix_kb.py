import json, os

kb_path = r"d:\Trae CN\github\nwacs\nwacs\core\v8\.deep_learning_kb\knowledge_base.json"
with open(kb_path, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed = 0
for k, v in data.items():
    examples = v.get("examples", [])
    if isinstance(examples, dict):
        v["examples"] = [examples]
        fixed += 1
    elif isinstance(examples, list):
        normalized = []
        for ex in examples:
            if isinstance(ex, dict):
                normalized.append(ex)
            elif isinstance(ex, str):
                normalized.append({"before": "", "after": ex})
        v["examples"] = normalized

print(f"Fixed {fixed} entries (dict -> list)")

with open(kb_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Knowledge base saved.")
