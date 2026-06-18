import pytest


class TestPackingListType:
    def test_trip_plan_includes_packing_list(self):
        from trip_types import TripPlan
        plan: TripPlan = {
            "itinerary": ["Day 1: Beach"],
            "budget": {"travel": 1000, "stay": 2000, "food": 1000, "activities": 500, "buffer": 500},
            "links": {"booking": {}, "maps_search": ""},
            "packing_list": ["Sunscreen", "Swimwear", "Sunglasses", "Sandals"],
        }
        assert "packing_list" in plan
        assert len(plan["packing_list"]) == 4

    def test_packing_list_is_list_of_strings(self):
        from trip_types import TripPlan
        plan: TripPlan = {
            "itinerary": ["Day 1: Hike"],
            "budget": {"travel": 1000, "stay": 2000, "food": 1000, "activities": 500, "buffer": 500},
            "links": {"booking": {}, "maps_search": ""},
            "packing_list": ["Hiking boots", "Water bottle", "First aid kit"],
        }
        for item in plan["packing_list"]:
            assert isinstance(item, str)

    def test_packing_list_categories_present(self):
        from trip_types import TripPlan
        plan: TripPlan = {
            "itinerary": ["Day 1: Beach"],
            "budget": {"travel": 1000, "stay": 2000, "food": 1000, "activities": 500, "buffer": 500},
            "links": {"booking": {}, "maps_search": ""},
            "packing_list": [
                "Clothing: Light shirts, shorts, swimwear",
                "Toiletries: Sunscreen, insect repellent",
                "Electronics: Camera, power bank",
                "Documents: ID, tickets, insurance",
                "Gear: Beach towel, snorkel",
                "Medicines: Pain reliever, motion sickness pills",
            ],
        }
        categories = {"Clothing", "Toiletries", "Electronics", "Documents", "Gear", "Medicines"}
        found = set()
        for item in plan["packing_list"]:
            if ":" in item:
                found.add(item.split(":")[0])
        assert found == categories
