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


def track_full_usage(logs_dir="logs"):
    agent_names = ["supervisor", "planner", "synthesis", "evaluator"]
    total_input_tokens = 0
    total_output_tokens = 0
    
    for agent_name in agent_names:
        json_path = Path(logs_dir) / f"{agent_name}_output.json"
        if json_path.exists():
            usage = track_usage(str(json_path))
            total_input_tokens += usage["input_tokens"]
            total_output_tokens += usage["output_tokens"]

    input_cost = (total_input_tokens * 0.1) / 1_000_000
    output_cost = (total_output_tokens * 0.4) / 1_000_000
    total_price = input_cost + output_cost
    
    return {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_price": round(total_price, 6),
    }