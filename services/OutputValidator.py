from main.agent import Agent
from main.schemas import *
import json
import re
def make_json_serializable(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [make_json_serializable(o) for o in obj]
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    return obj

def run_validate(agent_name:str , agent : Agent, output_schema , input_message: str , config = None):
    messages = [{"role": "user", "content": input_message}]
    response = agent.invoke({"messages": messages} , config = config)
    with open(f"logs/{agent_name}_output.json", "w", encoding="utf-8") as f:
        json.dump(make_json_serializable(response), f, ensure_ascii=False, indent=4)
    
    try : 
        response = re.sub(r"^\s*//.*$", "", response["messages"][-1].content, flags=re.MULTILINE) # remove comments in case
        response = json.loads(response)

    except json.JSONDecodeError as e:
        print(f"\n⚠ JSON PARSE ERROR in the : {agent_name}")
        print("Error:", e)
        print("Raw content:")
        print(response)
        raise
        

    try:
        validated_output = output_schema.model_validate(response)
        return validated_output
    
    except Exception as e:
        print(f"Validation error: {e}")
        return None