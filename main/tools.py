from services.synthesis_func import google_search , scrape_resources , scholarly_search
from langchain.tools import tool
import asyncio
from typing import List
from main.agent import Agent
from main.schemas import *
from services.OutputValidator import run_validate
from services.plan_parser import parse_plan
from langgraph.runtime import get_config
# Syntyhesis tools
@tool
def google_search_tool(query: str, max_results=2):
    """This function performs a Google search for the given query and returns the top results and resources ."""
    return asyncio.run(google_search(query, max_results))

@tool
def scrape_resources_tool(urls: List[str]):
    """This function takes a list of URLs and scrapes the content from each URL asynchronously."""
    return asyncio.run(scrape_resources(urls))

@tool
def scholarly_search_tool(query: str, max_results=2):
    """This Tool performs a semantic search for avaialble academic search papers in the knwoledge base related to the query and returns the top results."""
    return asyncio.run(scholarly_search(query, max_results))

@tool
def call_planner(query : str):
    """This tool return a strict plan to follow to generate the needed report about the user query research topic"""
    agent = get_config()["configurable"]["planner"]
    planner_response = run_validate(agent_name="planner", agent=agent, output_schema=PlannerOutputSchema , input_message=query)
    return parse_plan(planner_response.plan)

@tool
def call_synthesis(plan : str):
    """This tool returns A json format output that contains the answer to the user's research question based on the execution of the plan after searching from different resources"""
    agent = get_config()["configurable"]["synthesis"]
    synthesis_response = run_validate(agent_name="synthesis", agent=agent, output_schema=SynthesisOutputSchema , input_message=plan) 
    return {
        "answer":synthesis_response.answer,
        "refs" : synthesis_response.references
    }

@tool
def call_evaluator(answer : str):
    """This tool generate the detailled evaluation about the generated answer"""
    agent = get_config()["configurable"]["evaluator"]
    evaluator_response = run_validate(agent_name="evaluator", agent=agent, output_schema=EvaluationOutputSchema , input_message=answer)
    return evaluator_response



SupervisorTools = [call_planner , call_synthesis , call_evaluator]
SynthesisTools = [ scholarly_search_tool , google_search_tool , scrape_resources_tool]
PlanningTools = []
EvaluationTools = []
