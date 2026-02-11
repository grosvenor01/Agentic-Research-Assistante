from main.agent import Agent
from main.schemas import *
import json

def run_validate(agent : Agent, output_schema , messages):
    response = agent.invoke({"messages": messages})
    response = json.loads(response["messages"][-1].content)

    try:
        validated_output = output_schema.model_validate(response)
        return validated_output
    
    except Exception as e:
        print(f"Validation error: {e}")
        return None