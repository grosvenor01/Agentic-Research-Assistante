from sklearn.preprocessing import normalize
import numpy as np
from openai import AsyncOpenAI

class TextEmbedding: 
    openai_client : AsyncOpenAI
    embed_model_name : str

    @staticmethod
    def __init__(openai_client , model_name):
        TextEmbedding.openai_client = openai_client
        TextEmbedding.embed_model_name = model_name

    @staticmethod
    async def generate_embeddings(text_chunks: list[str], batch_size: int = 8):
        batches = [
            text_chunks[i:i + batch_size]
            for i in range(0, len(text_chunks), batch_size)
        ]
        embeddings = []
        for batch in batches:
            response = await TextEmbedding.openai_client.embeddings.create(
                model=TextEmbedding.embed_model_name,
                input=batch,
            )
            embeddings.extend(
                [item.embedding for item in response.data]
            )
        return normalize(np.array(embeddings)).tolist()
