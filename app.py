from main.config import Settings
from main.model import get_llm
from main.agent import Agent
from main.schemas import EvaluationOutputSchema, PlannerOutputSchema , SynthesisOutputSchema , SupervisorSchema
from main.tools import PlanningTools , SynthesisTools , EvaluationTools , SupervisorTools
from services.prompts import planning_system_prompt , synthesis_system_prompt , evaluation_system_prompt , supervisor_system_prompt
from services.OutputValidator import run_validate
from services.plan_parser import parse_plan
from services.usage_tracker import track_usage
import os
import time

import json
# Import All Settings 
settings = Settings()

supervisor = Agent(llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0),
    tools = SupervisorTools, 
    system_prompt=supervisor_system_prompt
).build_graph()

planner = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0.3),
    tools = PlanningTools, 
    system_prompt=planning_system_prompt
).build_graph()

synthesis = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0),
    tools = SynthesisTools,
    system_prompt=synthesis_system_prompt
).build_graph()

evaluator = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0.3),
    tools = EvaluationTools, 
    system_prompt=evaluation_system_prompt
).build_graph()

user_message = """Compare the architectural differences between Gemini, GPT-4, and Mixtral-style Mixture-of-Experts models.
                Explain how their design choices affect reasoning ability, inference cost, and scalability.
                Include references to specific research papers.
            """
# current = time.time()
# response_planner = run_validate(agent_name="planner", agent=planner, output_schema=PlannerOutputSchema , input_message=user_message)
# planner_message = f"user question : {user_message} \n  plan : {parse_plan(response_planner.plan)}"

# synthesis_response = run_validate(agent_name="synthesis", agent=synthesis, output_schema=SynthesisOutputSchema , input_message=planner_message) 
# evaluator_message = f" User Message : {user_message} \n Answer : {synthesis_response.answer} \n References : {synthesis_response.references}"

# evaluator_response = run_validate(agent_name="evaluator", agent=evaluator, output_schema=EvaluationOutputSchema , input_message=evaluator_message)
# end = time.time()

# #Save Final Response in txt file
# with open("final_response.txt", "w", encoding="utf-8") as f:
#     f.write(f"User Message : {user_message} \n\n")
#     f.write(f"Answer : {synthesis_response.answer} \n\n")
#     f.write("References : \n")
#     for ref in synthesis_response.references:
#         f.write(f"- {ref['title']} : {ref['url']} \n")
    
#     f.write("\n\nEvaluation : \n")
#     for criterion, result in evaluator_response.evaluation.items():
#         f.write(f"{criterion.capitalize()} (Score: {result['score']}) : {result['explanation']} \n\n")

# # Latency and Usage Tracking
# input_tokens =0
# output_tokens=0
# for i in os.listdir("logs/"):
#     usage = track_usage(f"logs/{i}")
#     input_tokens += usage["input_tokens"]
#     output_tokens += usage["output_tokens"]

# print(f"Total Input Tokens: {input_tokens}")
# print(f"Total Output Tokens: {output_tokens}")
# print(f"Total Cost: ${input_tokens*0.1/1000000 + output_tokens*0.4/1000000}$")
# print(f"Latency: {end - current} seconds")


config = {
    "configurable" : {
        "planner" : planner,
        "synthesis" : synthesis,
        "evaluator" : evaluator
    }
}

messages =  [
    {"role" : "user" , "content" : user_message}
]

output = run_validate(agent_name="supervisor" , agent= supervisor , output_schema= SupervisorSchema, input_message=user_message , config=config)
with open("final_response2.txt" , "w" , encoding="utf8") as fil:
    fil.write(output.final_report)
    fil.write(str(output.final_evaluation))
    
