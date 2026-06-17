# tools/booking_tool.py
from urllib.parse import urlencode

def booking_search_links(destination: str, origin: str = "Bangalore"):
    """
    Return a dict of useful booking links (mocked via search query URLs).
    """
    q = destination.replace(" ", "+")
    o = origin.replace(" ", "+")
    links = {
        "bus_search": f"https://www.redbus.in/search?fromCity={o}&toCity={q}",
        "train_search": f"https://www.irctc.co.in/nget/train-search?key={q}",
        "flight_search": f"https://www.google.com/search?q=flights+to+{q}",
        "hotel_search": f"https://www.booking.com/searchresults.html?ss={q}"
    }
    return links
