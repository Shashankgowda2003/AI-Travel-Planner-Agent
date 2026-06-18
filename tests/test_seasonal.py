import json
import os
import pytest


KB_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "india_destinations.json")


class TestSeasonalFestivalKnowledge:
    def test_all_entries_have_best_season(self):
        with open(KB_PATH, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            assert "best_season" in item, (
                f"Entry '{item.get('id')}' missing 'best_season' field"
            )

    def test_all_entries_have_festivals(self):
        with open(KB_PATH, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            assert "festivals" in item, (
                f"Entry '{item.get('id')}' missing 'festivals' field"
            )

    def test_festivals_has_valid_structure(self):
        with open(KB_PATH, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            for fest in item.get("festivals", []):
                assert "name" in fest
                assert "month" in fest
