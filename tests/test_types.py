import sys
import pytest


class TestTypesModule:
    def test_types_module_exists(self):
        from trip_types import TripPlan, Budget, Links, BookingLinks
        assert TripPlan is not None
        assert Budget is not None
        assert Links is not None
        assert BookingLinks is not None

    def test_budget_typeddict_keys(self):
        from trip_types import Budget
        b: Budget = {
            "travel": 2500,
            "stay": 3500,
            "food": 2000,
            "activities": 1500,
            "buffer": 500,
        }
        assert b["travel"] == 2500
        assert b["stay"] == 3500

    def test_trip_plan_structure(self):
        from trip_types import TripPlan
        plan: TripPlan = {
            "itinerary": ["Day 1: Beach", "Day 2: Fort"],
            "budget": {
                "travel": 2500,
                "stay": 3500,
                "food": 2000,
                "activities": 1500,
                "buffer": 500,
            },
            "links": {
                "booking": {
                    "bus_search": "https://example.com/bus",
                    "train_search": "https://example.com/train",
                    "flight_search": "https://example.com/flight",
                    "hotel_search": "https://example.com/hotel",
                },
                "maps_search": "https://maps.example.com/search",
            },
        }
        assert len(plan["itinerary"]) == 2
        assert plan["budget"]["travel"] == 2500

    def test_booking_links_structure(self):
        from trip_types import BookingLinks
        bl: BookingLinks = {
            "bus_search": "https://bus.example.com",
            "train_search": "https://train.example.com",
            "flight_search": "https://flight.example.com",
            "hotel_search": "https://hotel.example.com",
        }
        assert bl["bus_search"].startswith("https://")

    def test_links_are_typeddicts(self):
        from trip_types import Budget, TripPlan, Links, BookingLinks
        import typing
        assert typing.is_typeddict(Budget)
        assert typing.is_typeddict(TripPlan)
        assert typing.is_typeddict(Links)
        assert typing.is_typeddict(BookingLinks)
