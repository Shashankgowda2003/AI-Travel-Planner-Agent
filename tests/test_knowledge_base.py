import json
import os
import pytest


KNOWLEDGE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "knowledge", "india_destinations.json"
)

ALL_DESTINATIONS = [
    "goa", "jaipur", "kerala", "manali", "ladakh", "agra",
    "delhi", "mumbai", "bangalore", "chennai", "kolkata",
    "hyderabad", "udaipur", "varanasi", "rishikesh", "mount abu",
]


class TestKnowledgeBaseCoverage:
    def test_all_destinations_have_entries(self):
        with open(KNOWLEDGE_FILE, encoding="utf-8") as f:
            items = json.load(f)

        covered = set()
        for item in items:
            for dest in ALL_DESTINATIONS:
                if dest in item["content"].lower() or dest in item["title"].lower():
                    covered.add(dest)

        missing = [d for d in ALL_DESTINATIONS if d not in covered]
        assert not missing, (
            f"Knowledge base missing entries for: {missing}. "
            f"Add overview + day_plan for each."
        )

    def test_each_destination_has_overview_and_day_plan(self):
        with open(KNOWLEDGE_FILE, encoding="utf-8") as f:
            items = json.load(f)

        dest_ids = {}
        for item in items:
            did = item.get("id", "")
            for dest in ALL_DESTINATIONS:
                if dest.replace(" ", "_") in did:
                    dest_ids.setdefault(dest, set()).add(did)

        for dest in ALL_DESTINATIONS:
            ids = dest_ids.get(dest, set())
            has_overview = any("overview" in i for i in ids)
            has_day = any("day" in i for i in ids)
            assert has_overview, f"{dest} missing overview entry"
            assert has_day, f"{dest} missing day_plan entry"
