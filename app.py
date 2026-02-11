from main.config import Settings
from main.model import get_llm
from main.agent import Agent
from main.schemas import PlannerOutputSchema , SynthesisOutputSchema
from main.tools import PlanningTools , SynthesisTools , EvaluationTools , CitationTools
from services.prompts import planning_system_prompt , synthesis_system_prompt , evaluation_system_prompt , citation_system_prompt
from services.OutputValidator import run_validate
from services.plan_parser import parse_plan

# Import All Settings 
settings = Settings()

palnner = Agent(
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

citation = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0.3),
    tools = CitationTools,
    system_prompt=citation_system_prompt
).build_graph()

user_message = "What are the latest advancements in natural language processing? from announced research papers and generale information"
response_planner = run_validate(agent_name="planner", agent=palnner, output_schema=PlannerOutputSchema , input_message=user_message)
planner_message = f"user question : {user_message} \n  plan : {parse_plan(response_planner.plan)}"
synthesis_response = run_validate(agent_name="synthesis", agent=synthesis, output_schema=SynthesisOutputSchema , input_message=planner_message) 
evaluator_response = run_validate(agent_name="evaluator", agent=evaluator, output_schema=None , input_message=f" User Message : {user_message} \n Answer : {synthesis_response.answer} \n References : {synthesis_response.references}")


