from services.synthesis_func import google_search , scrape_resources , scholarly_search
from langchain.tools import tool
import asyncio
from typing import List

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

PlanningTools = []
SynthesisTools = [ scholarly_search_tool]
EvaluationTools = []