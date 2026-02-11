from main.config import Settings
from main.model import get_llm
from main.agent import Agent
from main.schemas import PlannerOutputSchema , SynthesisOutputSchema
from main.tools import PlanningTools , SynthesisTools , EvaluationTools , CitationTools
from services.prompts import planning_system_prompt , synthesis_system_prompt , evaluation_system_prompt , citation_system_prompt
from services.OutputValidator import run_validate
from scripts.ResearchPapersIngests.extractPDF import save_Qdrant
from scripts.ResearchPapersIngests.document_downloader import download_pdfs
import asyncio
"""
# Import All Settings 
settings = Settings()

palnner = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0.3),
    tools = PlanningTools, 
    system_prompt=planning_system_prompt
).build_graph()

synthesis = Agent(
    llm= get_llm(model_name = "gpt-4.1-nano",api_key=settings.openai_api_key , temperature=0.3),
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

user_message = "What are the latest advancements in natural language processing?"
"""
"""messages = [
    {"role": "user", "content": user_message}
]

response = run_validate(palnner , output_schema=PlannerOutputSchema , messages=messages) """
"""
plan = {
  "plan": [
    {
      "step": "Search in the web for relevant information on the latest advancements in natural language processing",
      "resources": ["Google Scholar", "arXiv", "AI research news websites"]
    },
    {
      "step": "Search and extract information from recent research papers and articles published in the last year related to NLP advancements",
      "resources": ["arXiv", "IEEE Xplore", "ACL Anthology"]
    },
    {
      "step": "Summarize the information and extract key insights on recent trends, breakthroughs, and emerging technologies in NLP",
      "resources": []
    },
    {
      "step": "Generate a comprehensive answer to the user's research question based on the gathered information",
      "resources": []
    }
  ]
}
messages = [
    {"role": "user", "content": f"user question : {user_message} \n  plan : {plan}"}
]

response = run_validate(synthesis , output_schema=SynthesisOutputSchema , messages=messages) 
print(response.answer)"""


