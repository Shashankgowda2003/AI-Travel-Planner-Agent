import re
import pytest


def parse_destination(query: str) -> str:
    """Simulates the destination regex parsing in app.py."""
    match = re.search(r"trip to (.+?)\s*(?:under|for|in\s*\d|\d+\s*day|$)", query, re.I)
    if match:
        return match.group(1).strip()
    return ""


class TestDestinationParsing:
    def test_single_word_destination(self):
        assert parse_destination("trip to Goa under 10000") == "Goa"

    def test_multi_word_destination(self):
        assert parse_destination("Plan me a trip to New Delhi for 3 days") == "New Delhi"

    def test_three_word_destination(self):
        assert parse_destination("trip to Andaman and Nicobar under 50000") == "Andaman and Nicobar"

    def test_destination_with_hyphens(self):
        result = parse_destination("trip to Mount Abu for 4 days")
        assert result == "Mount Abu"

    def test_destination_with_ampersand(self):
        result = parse_destination("trip to Andaman & Nicobar under 30000")
        assert "Andaman" in result
        assert "Nicobar" in result

    def test_destination_before_days_number(self):
        assert parse_destination("trip to Jaipur 3 day") == "Jaipur"

    def test_destination_end_of_string(self):
        assert parse_destination("trip to Goa") == "Goa"

    def test_destination_case_insensitive(self):
        assert parse_destination("Trip to KERALA under 20000") == "KERALA"


def parse_days(query: str) -> int:
    """Simulates the days regex parsing in app.py."""
    match = re.search(r"(\d+)[ -]?day", query, re.I)
    if match:
        return int(match.group(1))
    return 3


class TestDaysParsing:
    def test_standard_format(self):
        assert parse_days("3-day trip to Goa") == 3

    def test_with_space(self):
        assert parse_days("5 day trip to Goa") == 5

    def test_two_digit_days(self):
        assert parse_days("12-day trip to Goa") == 12

    def test_no_days_match(self):
        assert parse_days("trip to Goa") == 3


def parse_budget(query: str) -> int:
    """Simulates the budget regex parsing in app.py."""
    match = re.search(r"under\s*₹?(\d+)", query, re.I)
    if match:
        return int(match.group(1))
    return 10000


class TestBudgetParsing:
    def test_with_rupee_symbol(self):
        assert parse_budget("trip to Goa under ₹5000") == 5000

    def test_without_rupee_symbol(self):
        assert parse_budget("trip to Goa under 15000") == 15000

    def test_large_budget(self):
        assert parse_budget("trip to Goa under ₹100000") == 100000

    def test_no_budget_match(self):
        assert parse_budget("trip to Goa") == 10000
