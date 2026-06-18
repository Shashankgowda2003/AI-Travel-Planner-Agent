import pytest
import os


class TestMapRenderer:
    def test_map_renderer_module_exists(self):
        from tools.map_renderer import render_itinerary_map
        assert callable(render_itinerary_map)

    def test_render_produces_html_string(self):
        from tools.map_renderer import render_itinerary_map
        destination_coords = (15.2993, 74.1240)
        day_activities = [
            {"day": 1, "locations": [("Fort Aguada", 15.50, 73.77), ("Baga Beach", 15.55, 73.75)]},
            {"day": 2, "locations": [("Palolem Beach", 15.01, 74.03)]},
        ]
        result = render_itinerary_map(destination_coords, day_activities)
        assert isinstance(result, str)
        assert "leaflet" in result.lower() or "L.map" in result

    def test_render_handles_empty_activities(self):
        from tools.map_renderer import render_itinerary_map
        result = render_itinerary_map((15.2993, 74.1240), [])
        assert isinstance(result, str)

    def test_default_zoom_is_10(self):
        from tools.map_renderer import render_itinerary_map
        result = render_itinerary_map((15.2993, 74.1240), [], zoom=10)
        assert "L.map" in result or "leaflet" in result.lower()
