import os
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

LAT_LON_MAP: Dict[str, tuple] = {
    "goa": (15.2993, 74.1240),
    "jaipur": (26.9124, 75.7873),
    "kerala": (10.8505, 76.2711),
    "manali": (32.2396, 77.1887),
    "ladakh": (34.1526, 77.5771),
    "agra": (27.1767, 78.0081),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "udaipur": (24.5854, 73.7125),
    "varanasi": (25.3176, 82.9739),
    "rishikesh": (30.0869, 78.2676),
    "mount abu": (24.5926, 72.7156),
}

PLACEHOLDER_CONDITIONS = [
    "Sunny", "Partly Cloudy", "Clear", "Light Rain",
    "Thunderstorms", "Cloudy", "Hot and Humid", "Mild",
]


def _lookup_lat_lon(destination: str) -> tuple:
    key = destination.strip().lower()
    if key in LAT_LON_MAP:
        return LAT_LON_MAP[key]
    for k, v in LAT_LON_MAP.items():
        if k in key or key in k:
            return v
    return (23.0, 79.0)


def get_weather_forecast(destination: str, days: int = 7) -> Dict[str, Any]:
    lat, lon = _lookup_lat_lon(destination)

    if API_KEY:
        try:
            import httpx
            from datetime import datetime, timedelta
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "cnt": min(days * 8, 40),
            }
            response = httpx.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return _parse_openweather_response(data, destination, days)
            logger.warning("OpenWeatherMap API returned status %d", response.status_code)
        except Exception as e:
            logger.warning("Failed to fetch weather from API: %s", e)

    return _generate_placeholder_forecast(destination, days)


def _parse_openweather_response(data: dict, city: str, days: int) -> dict:
    forecast = []
    seen_dates = set()
    for entry in data.get("list", []):
        dt_text = entry.get("dt_txt", "")
        day = dt_text.split(" ")[0] if dt_text else ""
        if day in seen_dates:
            continue
        seen_dates.add(day)
        if len(forecast) >= days:
            break
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]
        forecast.append({
            "day": len(forecast) + 1,
            "temp_min": round(main.get("temp_min", 25)),
            "temp_max": round(main.get("temp_max", 32)),
            "condition": weather.get("main", "Clear"),
            "rain_chance": round(entry.get("pop", 0) * 100),
            "humidity": main.get("humidity", 60),
        })
    return {"city": city, "country": "IN", "forecast": forecast}


def _generate_placeholder_forecast(destination: str, days: int) -> dict:
    import random
    rng = random.Random(hash(destination) % 2**32)
    forecast = []
    for i in range(min(days, 7)):
        forecast.append({
            "day": i + 1,
            "temp_min": rng.randint(18, 28),
            "temp_max": rng.randint(28, 38),
            "condition": rng.choice(PLACEHOLDER_CONDITIONS),
            "rain_chance": rng.randint(0, 60),
            "humidity": rng.randint(50, 90),
        })
    return {"city": destination, "country": "IN", "forecast": forecast}


def format_weather_context(weather_data: Dict[str, Any]) -> str:
    lines = [f"Weather forecast for {weather_data.get('city', 'destination')}:"]
    for f in weather_data.get("forecast", []):
        lines.append(
            f"  Day {f['day']}: {f['condition']}, {f['temp_min']}\u00b0C-{f['temp_max']}\u00b0C, "
            f"Rain: {f['rain_chance']}%, Humidity: {f['humidity']}%"
        )
    return "\n".join(lines)
