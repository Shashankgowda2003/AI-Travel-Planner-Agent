from typing import Dict, Tuple


DESTINATION_COORDS: Dict[str, Tuple[float, float]] = {
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


def lookup_coords(destination: str) -> Tuple[float, float]:
    key = destination.strip().lower()
    if key in DESTINATION_COORDS:
        return DESTINATION_COORDS[key]
    for k, v in DESTINATION_COORDS.items():
        if k in key or key in k:
            return v
    return (23.0, 79.0)


def compute_fallback_budget(budget: int) -> Dict[str, int]:
    travel = int(budget * 0.25)
    stay = int(budget * 0.35)
    food = int(budget * 0.2)
    activities = int(budget * 0.15)
    buffer = budget - (travel + stay + food + activities)
    return {
        "travel": travel,
        "stay": stay,
        "food": food,
        "activities": activities,
        "buffer": buffer,
    }
