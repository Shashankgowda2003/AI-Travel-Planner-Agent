import pytest
from tools.booking_tool import booking_search_links


class TestBookingTool:
    def test_basic_links_returned(self):
        links = booking_search_links("Goa")
        assert isinstance(links, dict)
        assert "bus_search" in links
        assert "train_search" in links
        assert "flight_search" in links
        assert "hotel_search" in links

    def test_spaces_replaced_with_plus(self):
        links = booking_search_links("New Delhi")
        assert "New+Delhi" in links["bus_search"] or "New%20Delhi" in links["bus_search"]

    def test_default_origin_is_bangalore(self):
        links = booking_search_links("Goa")
        assert "fromCity=Bangalore" in links["bus_search"]

    def test_custom_origin(self):
        links = booking_search_links("Goa", origin="Mumbai")
        assert "fromCity=Mumbai" in links["bus_search"]

    def test_origin_with_spaces_encoded(self):
        links = booking_search_links("Jaipur", origin="New Delhi")
        assert "fromCity=New+Delhi" in links["bus_search"] or "fromCity=New%20Delhi" in links["bus_search"]

    def test_train_search_url(self):
        links = booking_search_links("Goa")
        assert "irctc" in links["train_search"].lower()

    def test_flight_search_url(self):
        links = booking_search_links("Goa")
        assert "flights" in links["flight_search"]

    def test_hotel_search_url(self):
        links = booking_search_links("Goa")
        assert "booking.com" in links["hotel_search"]
