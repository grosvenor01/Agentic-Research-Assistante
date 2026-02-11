from exa_py import Exa
from main.config import Settings
from typing import List
import asyncio
from qdrant_client import AsyncQdrantClient
from scripts.ResearchPapersIngests.text_embedding import TextEmbedding
from openai import AsyncOpenAI

async def google_search(query: str, max_results=2):
    """This function performs a Google search for the given query and returns the top results ."""
    exa = Exa(api_key=Settings().exa_api_key)
    results = exa.search(
        query=query,
        type="auto",
        num_results=max_results,
        contents={"highlights":{"max_characters":2000}}
    )
    return results

async def scrape_resources(urls: List[str]):
    """This function takes a list of URLs and scrapes the content from each URL asynchronously. Should be used one time for multiple urls """
    exa = Exa(api_key=Settings().exa_api_key)
    results = exa.get_contents(urls, text=True)
    return results

def scholarly_outputparser(search_results):
    extracted_info = []
    for result in search_results:
        extracted_info.append({
            "title": result.payload.get("title", "No title available"),
            "summary": result.payload.get("text", "No summary available"),
        })
    return extracted_info

async def scholarly_search(query: str, max_results=2):
    """This Tool performs papers search in avaialble academic search papers related to the query and returns theire sumarry"""
    openai_client = AsyncOpenAI(api_key=Settings().openai_api_key)
    qdrant_client = AsyncQdrantClient(url=Settings().qdrant_url)
    embedding_client = TextEmbedding(openai_client=openai_client, model_name="text-embedding-3-small")
    text_embedding = await embedding_client.generate_embeddings([query])
    search_results = await qdrant_client.search(
        collection_name="research_papers",
        query_vector=text_embedding[0],
        limit=max_results,
    )
    return scholarly_outputparser(search_results)
