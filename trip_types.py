from typing import TypedDict, List, Dict


class Budget(TypedDict, total=False):
    travel: int
    stay: int
    food: int
    activities: int
    buffer: int


class BookingLinks(TypedDict, total=False):
    bus_search: str
    train_search: str
    flight_search: str
    hotel_search: str


class Links(TypedDict, total=False):
    booking: BookingLinks
    maps_search: str


class TripPlan(TypedDict):
    itinerary: List[str]
    budget: Budget
    links: Links
