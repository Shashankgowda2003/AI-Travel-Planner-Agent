import pytest
from unittest.mock import patch, MagicMock


MOCK_WEATHER_RESPONSE = {
    "city": "Goa",
    "country": "IN",
    "forecast": [
        {"day": 1, "temp_min": 25, "temp_max": 32, "condition": "Partly Cloudy", "rain_chance": 10, "humidity": 70},
        {"day": 2, "temp_min": 26, "temp_max": 33, "condition": "Sunny", "rain_chance": 5, "humidity": 65},
        {"day": 3, "temp_min": 24, "temp_max": 30, "condition": "Thunderstorms", "rain_chance": 80, "humidity": 85},
        {"day": 4, "temp_min": 25, "temp_max": 31, "condition": "Rain", "rain_chance": 60, "humidity": 78},
    ],
}


class TestWeatherTool:
    def test_get_weather_forecast_returns_dict(self):
        from tools.weather_tool import get_weather_forecast
        result = get_weather_forecast("Goa", days=3)
        assert isinstance(result, dict)

    def test_get_weather_forecast_has_city(self):
        from tools.weather_tool import get_weather_forecast
        result = get_weather_forecast("Goa", days=3)
        assert "city" in result
        assert "Goa" in result.get("city", "")

    def test_get_weather_forecast_days_count(self):
        from tools.weather_tool import get_weather_forecast
        result = get_weather_forecast("Jaipur", days=4)
        assert "forecast" in result
        assert len(result["forecast"]) <= 4

    def test_get_weather_forecast_has_required_fields(self):
        from tools.weather_tool import get_weather_forecast
        result = get_weather_forecast("Goa", days=2)
        for day_data in result["forecast"]:
            for key in ["day", "temp_min", "temp_max", "condition", "rain_chance", "humidity"]:
                assert key in day_data

    def test_get_weather_forecast_no_api_key_returns_placeholder(self):
        from tools.weather_tool import get_weather_forecast
        result = get_weather_forecast("Mumbai", days=3)
        assert result is not None
        assert "forecast" in result

    def test_get_weather_forecast_different_destinations(self):
        from tools.weather_tool import get_weather_forecast
        r1 = get_weather_forecast("Goa", days=2)
        r2 = get_weather_forecast("Manali", days=2)
        assert r1["city"] != r2["city"]

    def test_weather_context_formatting(self):
        from tools.weather_tool import format_weather_context
        result = format_weather_context(MOCK_WEATHER_RESPONSE)
        assert isinstance(result, str)
        assert "Goa" in result
        assert "Thunderstorms" in result
