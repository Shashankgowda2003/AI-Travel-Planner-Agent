import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    openai_api_key: str = Field(..., min_length=1)
    model_name: str = "gpt-4"
    temperature: float = 0.2
    chroma_persist_dir: str = "./chroma_db"
    origin_city: str = "Bangalore"
    google_maps_api_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    default_days: int = 3
    default_budget: int = 10000
    max_days: int = 14
    fallback_models: List[str] = [
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo",
    ]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    @field_validator("openai_api_key")
    @classmethod
    def api_key_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("OPENAI_API_KEY must not be empty")
        return v.strip()


settings = Settings()
