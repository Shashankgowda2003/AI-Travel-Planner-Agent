# tools/maps_tool.py
import os
from urllib.parse import urlencode

def google_maps_search_url(query: str, api_key: str | None = None):
    """
    Build a Google Maps search URL (works without API key for user clicking).
    If API key is present, it can be used for embed URLs in the Streamlit iframe.
    """
    base = "https://www.google.com/maps/search/?"
    params = {"api": "1", "query": query}
    return base + urlencode(params)

def google_maps_embed_iframe_url(lat: float, lng: float, zoom: int = 12):
    """
    Returns a maps.google.com embed URL for an iframe. If GOOGLE_MAPS_API_KEY is present, you can
    use the JavaScript API for richer interactions; but a simple place embed works without it.
    """
    # Simple embed via maps.google.com
    return f"https://www.google.com/maps?q={lat},{lng}&z={zoom}&output=embed"
