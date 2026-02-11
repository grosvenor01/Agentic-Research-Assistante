from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    exa_api_key: str = Field(alias="EXA_API_KEY")
    qdrant_url: str = Field(alias="qdrant_url")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }