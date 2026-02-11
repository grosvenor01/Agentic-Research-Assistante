from sklearn.preprocessing import normalize
import numpy as np
from openai import AsyncOpenAI

class TextEmbedding: 
    openai_client : AsyncOpenAI
    embed_model_name : str

    def __init__(self, openai_client , model_name):
        self.openai_client = openai_client
        self.embed_model_name = model_name

    async def generate_embeddings(self, text_chunks: list[str], batch_size: int = 8):
        batches = [
            text_chunks[i:i + batch_size]
            for i in range(0, len(text_chunks), batch_size)
        ]
        embeddings = []
        for batch in batches:
            response = await self.openai_client.embeddings.create(
                model=self.embed_model_name,
                input=batch,
            )
            embeddings.extend(
                [item.embedding for item in response.data]
            )
        return normalize(np.array(embeddings)).tolist()
