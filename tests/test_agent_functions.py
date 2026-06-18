import json
import pytest
from utils import compute_fallback_budget, DESTINATION_COORDS, lookup_coords


class TestFallbackBudgetSplit:
    def test_total_equals_budget(self):
        budget = 10000
        split = compute_fallback_budget(budget)
        total = sum(split.values())
        assert total == budget

    def test_large_budget(self):
        budget = 100000
        split = compute_fallback_budget(budget)
        assert sum(split.values()) == budget

    def test_small_budget(self):
        budget = 500
        split = compute_fallback_budget(budget)
        assert sum(split.values()) == budget

    def test_budget_categories_present(self):
        budget = 10000
        split = compute_fallback_budget(budget)
        for key in ["travel", "stay", "food", "activities", "buffer"]:
            assert key in split

    def test_no_negative_values(self):
        budget = 100
        split = compute_fallback_budget(budget)
        for val in split.values():
            assert val >= 0


class TestDestinationCoords:
    def test_goa_coords(self):
        lat, lng = lookup_coords("Goa")
        assert lat == 15.2993
        assert lng == 74.1240

    def test_case_insensitive(self):
        lat, lng = lookup_coords("GOA")
        assert lat == 15.2993

    def test_jaipur_coords(self):
        lat, lng = lookup_coords("Jaipur")
        assert lat == 26.9124

    def test_new_delhi_coords(self):
        lat, lng = lookup_coords("New Delhi")
        assert lat == 28.6139

    def test_fallback_coords(self):
        lat, lng = lookup_coords("Unknown City")
        assert lat == 23.0
        assert lng == 79.0

    def test_partial_match(self):
        lat, lng = lookup_coords("South Goa")
        assert lat == 15.2993

    def test_all_destinations_have_valid_coords(self):
        for dest_name in DESTINATION_COORDS:
            lat, lng = DESTINATION_COORDS[dest_name]
            assert -90 <= lat <= 90
            assert -180 <= lng <= 180
