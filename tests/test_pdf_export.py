import pytest
import io


class TestPDFExport:
    def test_pdf_export_module_exists(self):
        from tools.pdf_export import generate_itinerary_pdf
        assert callable(generate_itinerary_pdf)

    def test_generate_pdf_returns_bytes(self):
        from tools.pdf_export import generate_itinerary_pdf
        plan = {
            "itinerary": ["Day 1: Visit Fort Aguada", "Day 2: Relax at Palolem Beach"],
            "budget": {"travel": 2500, "stay": 3500, "food": 2000, "activities": 1500, "buffer": 500},
            "links": {
                "booking": {"hotel_search": "https://booking.com/goa"},
                "maps_search": "https://maps.google.com/goa",
            },
        }
        pdf_bytes = generate_itinerary_pdf(plan, "Goa", 2)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0

    def test_pdf_starts_with_pdf_header(self):
        from tools.pdf_export import generate_itinerary_pdf
        plan = {"itinerary": ["Day 1: Tour"], "budget": {}, "links": {}}
        pdf_bytes = generate_itinerary_pdf(plan, "Test", 1)
        assert pdf_bytes[:5] == b"%PDF-"
