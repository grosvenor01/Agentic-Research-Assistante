from exa_py import Exa
from scholarly import scholarly
from main.config import Settings
from typing import List
import asyncio
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance , VectorParams
from scripts.ResearchPapersIngests.text_embedding import TextEmbedding
# Syntyhesis tools

def google_search(query: str, max_results=2):
    """This function performs a Google search for the given query and returns the top results ."""
    exa = Exa(api_key=Settings().exa_api_key)
    results = exa.search(
        query=query,
        type="auto",
        num_results=max_results,
        contents={"highlights":{"max_characters":2000}}
    )
    return results

async def scrape_single(exa, url: str):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, exa.scrape, [url])
    return result

async def scrape_resources(urls: List[str]):
    """This function takes a list of URLs and scrapes the content from each URL asynchronously."""
    exa = Exa(api_key=Settings().exa_api_key)
    tasks = [scrape_single(exa, url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def scholarly_search(query: str, max_results=2):
    """This Tool performs a semantic search for avaialble academic search papers related to the query and returns the top results."""
    client = AsyncQdrantClient(url=Settings().qdrant_url)
    search_results = await client.search(
        collection_name="research_papers",
        query_vector=TextEmbedding().embed_text(query),
        limit=max_results,
        with_payload=True
    )
    return search_results

PlanningTools = []
SynthesisTools = [google_search , scrape_resources , scholarly_search]
EvaluationTools = []
CitationTools = []