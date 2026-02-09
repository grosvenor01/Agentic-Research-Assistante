from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }