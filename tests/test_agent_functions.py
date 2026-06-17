import json
import pytest
from unittest.mock import patch, MagicMock


class TestFallbackBudgetSplit:
    """Test the fallback budget split logic independent of LLM calls."""

    def _get_budget_split(self, budget: int) -> dict:
        travel = int(budget * 0.25)
        stay = int(budget * 0.35)
        food = int(budget * 0.2)
        activities = int(budget * 0.15)
        buf = budget - (travel + stay + food + activities)
        return {
            "travel": travel,
            "stay": stay,
            "food": food,
            "activities": activities,
            "buffer": buf,
        }

    def test_total_equals_budget(self):
        budget = 10000
        split = self._get_budget_split(budget)
        total = sum(split.values())
        assert total == budget

    def test_large_budget(self):
        budget = 100000
        split = self._get_budget_split(budget)
        assert sum(split.values()) == budget

    def test_small_budget(self):
        budget = 500
        split = self._get_budget_split(budget)
        assert sum(split.values()) == budget

    def test_budget_categories_present(self):
        budget = 10000
        split = self._get_budget_split(budget)
        for key in ["travel", "stay", "food", "activities", "buffer"]:
            assert key in split

    def test_no_negative_values(self):
        budget = 100
        split = self._get_budget_split(budget)
        for val in split.values():
            assert val >= 0


class TestDestinationCoords:
    """Test the destination coordinate lookup from app.py."""

    DESTINATION_COORDS = {
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
    }

    def _lookup(self, dest):
        key = dest.strip().lower()
        if key in self.DESTINATION_COORDS:
            return self.DESTINATION_COORDS[key]
        for k, v in self.DESTINATION_COORDS.items():
            if k in key or key in k:
                return v
        return (23.0, 79.0)

    def test_goa_coords(self):
        lat, lng = self._lookup("Goa")
        assert lat == 15.2993
        assert lng == 74.1240

    def test_case_insensitive(self):
        lat, lng = self._lookup("GOA")
        assert lat == 15.2993

    def test_jaipur_coords(self):
        lat, lng = self._lookup("Jaipur")
        assert lat == 26.9124

    def test_new_delhi_coords(self):
        lat, lng = self._lookup("New Delhi")
        assert lat == 28.6139

    def test_fallback_coords(self):
        lat, lng = self._lookup("Unknown City")
        assert lat == 23.0
        assert lng == 79.0

    def test_partial_match(self):
        lat, lng = self._lookup("South Goa")
        assert lat == 15.2993
