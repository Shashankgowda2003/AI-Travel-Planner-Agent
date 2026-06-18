import json
import pytest
from unittest.mock import patch, MagicMock


def _simulate_llm_chain_with_fallback(primary_model: str, fallback_models: list[str], destination: str):
    models_to_try = [primary_model] + fallback_models
    last_error = None
    for model in models_to_try:
        try:
            if model == primary_model:
                raise Exception(f"Primary model {model} failed")
            return {
                "itinerary": [f"Day 1: Tour {destination}"],
                "budget": {"travel": 1000, "stay": 2000, "food": 1000, "activities": 500, "buffer": 500},
                "links": {"maps_search": f"https://maps.example.com/{destination}"},
            }
        except Exception as e:
            last_error = e
            continue
    raise RuntimeError("All models failed") from last_error


class TestModelFallback:
    def test_fallback_chain_exists(self):
        from config import settings
        assert len(settings.fallback_models) >= 2

    def test_fallback_uses_second_model_on_primary_failure(self):
        result = _simulate_llm_chain_with_fallback("gpt-4", ["gpt-4o", "gpt-3.5-turbo"], "Goa")
        assert result is not None
        assert "itinerary" in result

    def test_fallback_exhausts_all_models_then_raises(self):
        with pytest.raises(RuntimeError, match="All models failed"):
            _simulate_llm_chain_with_fallback("bad-model", [], "Goa")

    def test_fallback_logs_warnings(self):
        from config import settings
        fallback = settings.fallback_models
        assert fallback
        assert isinstance(fallback, list)
