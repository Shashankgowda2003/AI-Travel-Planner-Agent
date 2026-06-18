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


TRAVEL_STYLES = [
    "luxury",
    "budget",
    "backpacker",
    "family",
    "couple",
    "solo",
    "adventure",
    "relaxation",
]

STYLE_PROMPTS = {
    "luxury": "Focus on 5-star hotels, fine dining, private tours, premium experiences, and exclusive access to attractions.",
    "budget": "Prioritize free attractions, public transport, budget stays, street food, and low-cost experiences.",
    "backpacker": "Recommend hostels, local buses, offbeat spots, street food, hiking trails, and budget-friendly adventures.",
    "family": "Suggest kid-friendly activities, safe areas, family restaurants, relaxed pace, parks, and interactive museums.",
    "couple": "Include romantic spots, candlelight dinners, scenic viewpoints, couple activities, and cozy cafes.",
    "solo": "Recommend safe solo activities, social hostels, group tours, self-guided walks, and local meetup spots.",
    "adventure": "Prioritize trekking, water sports, paragliding, biking, rock climbing, and extreme sports activities.",
    "relaxation": "Focus on spas, beaches, slow pace, wellness retreats, nature walks, and peaceful getaways.",
}

STYLE_BUDGET_WEIGHTS = {
    "luxury": {"stay": 0.50, "food": 0.20, "activities": 0.15, "travel": 0.15},
    "budget": {"stay": 0.25, "food": 0.15, "activities": 0.15, "travel": 0.45},
    "backpacker": {"stay": 0.15, "food": 0.20, "activities": 0.20, "travel": 0.45},
    "family": {"stay": 0.35, "food": 0.20, "activities": 0.25, "travel": 0.20},
    "couple": {"stay": 0.40, "food": 0.20, "activities": 0.20, "travel": 0.20},
    "solo": {"stay": 0.25, "food": 0.15, "activities": 0.25, "travel": 0.35},
    "adventure": {"stay": 0.20, "food": 0.15, "activities": 0.40, "travel": 0.25},
    "relaxation": {"stay": 0.40, "food": 0.15, "activities": 0.25, "travel": 0.20},
}

DIETARY_OPTIONS = [
    "No restriction",
    "Vegetarian",
    "Vegan",
    "Halal",
    "Gluten-free",
    "Jain",
]

ACCESSIBILITY_OPTIONS = [
    "None",
    "Wheelchair accessible",
    "Child-friendly",
    "Senior-friendly",
    "Low physical activity",
]
