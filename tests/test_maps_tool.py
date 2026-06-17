import pytest
from tools.maps_tool import google_maps_search_url, google_maps_embed_iframe_url


class TestMapsTool:
    def test_search_url_basic(self):
        url = google_maps_search_url("Goa beaches")
        assert url.startswith("https://www.google.com/maps/search/?")
        assert "query=Goa+beaches" in url or "query=Goa%20beaches" in url

    def test_search_url_with_plus_encoding(self):
        url = google_maps_search_url("New Delhi")
        assert "New+Delhi" in url or "New%20Delhi" in url

    def test_embed_iframe_url(self):
        url = google_maps_embed_iframe_url(15.2993, 74.1240, zoom=9)
        assert url.startswith("https://www.google.com/maps?")
        assert "15.2993" in url
        assert "74.124" in url
        assert "z=9" in url
        assert "output=embed" in url

    def test_embed_iframe_default_zoom(self):
        url = google_maps_embed_iframe_url(26.9124, 75.7873)
        assert "z=12" in url

    def test_embed_iframe_custom_zoom(self):
        url = google_maps_embed_iframe_url(26.9124, 75.7873, zoom=7)
        assert "z=7" in url
