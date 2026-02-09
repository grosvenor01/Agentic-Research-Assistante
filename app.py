from main.config import Settings
from main.model import get_llm


settings = Settings()

client = get_llm(settings.openai_api_key, temperature=0.7)
response = client.invoke("what is the capital of algeria ? ")


