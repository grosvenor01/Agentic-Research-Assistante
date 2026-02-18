import os
import uuid
import langextract as lx
from main.config import Settings
import asyncio 
import PyPDF2
from openai import AsyncOpenAI
from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance , VectorParams
from .text_embedding import TextEmbedding
import json ,asyncio
from langchain_openai import ChatOpenAI

async def read_pdf(pdf_path: str):
        def read_pdf_sync(path: str):
            text = ""
            with open(f"docs/{path}", "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        return await asyncio.to_thread(read_pdf_sync, pdf_path)

async def ExtractPDF(file_paths: list[str]):
    system_prompt = """
        You are a helpful research assistant that extracts and summarizes key information and contributions from research papers.
        Output format:
        {
            "title": "Title of the paper",
            "summary": "A concise summary of the paper's main contributions and findings"
        }
    """
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0,
        api_key=Settings().openai_api_key
    )

    texts = await asyncio.gather(
        *(read_pdf(path) for path in file_paths)
    )

    responses = await asyncio.gather(*(llm.ainvoke(
        [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Extract the key insights, methodologies, contributions and findings from the following research paper:\n\n{text}"
            }
        ]
    ) for text in texts
    ))

    return [json.loads(response.content) for response in responses]

async def save_Qdrant():
    # Create Qdrant client 
    client = AsyncQdrantClient(url=Settings().qdrant_url)
    try:
        await client.create_collection(collection_name="research_papers",vectors_config= VectorParams(size=1536 , distance=Distance.COSINE))
    except Exception as e:
        print(f"Collection already exists or error creating collection")
    
    # Sumarize files 
    files = await ExtractPDF(os.listdir("docs/"))
    print(files)
    
    # Embed files 
    file_texts = [file["title"] for file in files]
    embedder = TextEmbedding(openai_client=AsyncOpenAI(api_key=Settings().openai_api_key), model_name="text-embedding-3-small")
    embeddings = await embedder.generate_embeddings(file_texts)
    
    # Store in Qdrant 
    for file, embedding in zip(files, embeddings):
        await client.upsert(
            collection_name="research_papers",
            points=[
                {
                    "id": str(uuid.uuid4()),
                    "vector": embedding,
                    "payload": {"text": file["summary"] , "title": file["title"]}
                }
            ]
        )

if __name__ == "__main__":
    asyncio.run(save_Qdrant())

         
     


    