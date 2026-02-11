from typing import List
import json
def plan_transforme(plan: List) -> str:
    str =""
    for index , i in enumerate(plan):
        str += f"Step {index+1} : {i['step']} \n"
    
    return str
    
def parse_plan(plan: List) -> str:
    print(type(plan))
    try:
        return plan_transforme(plan)
    
    except json.JSONDecodeError as e:
        print(f"Error parsing plan: {e}")
        return {}