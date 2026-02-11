import json
from pathlib import Path

def track_usage(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_input_tokens = 0
    total_output_tokens = 0

    for msg in data.get("messages", []):
        usage = msg.get("usage_metadata") or {}
        
        total_input_tokens += usage.get("input_tokens", 0)
        total_output_tokens += usage.get("output_tokens", 0)

    return {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
    }