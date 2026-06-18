# app.py
import re
import logging
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config import settings
from agent import plan_trip_with_agent
from tools.maps_tool import google_maps_embed_iframe_url
from utils import lookup_coords

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("✈️ AI Travel Planner Agent")

if not settings.openai_api_key:
    st.error("OPENAI_API_KEY is not set. Create a .env file with your OpenAI API key.")
    st.stop()

with st.sidebar:
    st.header("Default Trip Parameters")
    default_destination = st.text_input("Destination", value="Goa")
    default_days = st.number_input("Number of days", min_value=1, max_value=settings.max_days, value=settings.default_days)
    default_budget = st.number_input("Budget (₹)", min_value=500, value=settings.default_budget, step=500)
    prefer = st.text_input("Preferences", value="beach, budget")

col1, col2 = st.columns((2, 1))

with col1:
    st.subheader("Your Trip Request")
    query = st.text_area(
        "Enter your request:",
        value=f"Plan me a {default_days}-day trip to {default_destination} under ₹{default_budget}. Preferences: {prefer}",
    )

    if st.button("Plan Trip"):
        # --- Parse free-text request ---
        dest, days, budget = default_destination, default_days, default_budget

        match = re.search(r"(\d+)[ -]?day", query, re.I)
        if match:
            days = int(match.group(1))
        match = re.search(r"under\s*₹?(\d+)", query, re.I)
        if match:
            budget = int(match.group(1))
        match = re.search(r"trip to (.+?)\s*(?:under|for|in\s*\d|\d+\s*day|$)", query, re.I)
        if match:
            dest = match.group(1).strip()

        # Extract preferences from edited query text, fallback to sidebar
        pref_match = re.search(r"preferences?:\s*(.+?)(?:$)", query, re.I)
        if pref_match:
            active_prefer = pref_match.group(1).strip()
        else:
            active_prefer = prefer

        logger.info("Planning trip: dest=%s, days=%d, budget=%d, preferences=%s", dest, days, budget, active_prefer)

        try:
            with st.spinner(f"Planning {days}-day trip to {dest} within ₹{budget}..."):
                plan = plan_trip_with_agent(dest, days, budget, active_prefer)
        except Exception as e:
            logger.error("Trip planning failed: %s", e, exc_info=True)
            st.error(f"Failed to generate trip plan: {e}")
            st.info("Try reducing days/budget or selecting a different destination.")
            st.stop()

        # --- Display itinerary ---
        st.success("Plan ready!")
        st.subheader("Itinerary")
        for idx, d in enumerate(plan.get("itinerary", []), start=1):
            # Remove duplicate "Day X:" if already present
            clean_day = re.sub(r"^Day\s*\d+:?\s*", "", d, flags=re.I).strip()
            st.markdown(f"**Day {idx}:** {clean_day}")

        # --- Display budget ---
        st.subheader("Budget Breakdown (₹)")
        budget_dict = plan.get("budget", {})
        for k, v in budget_dict.items():
            clean_val = str(v).replace("₹₹", "₹")  # Remove accidental double ₹
            st.write(f"- **{k.capitalize()}**: {clean_val}")

        # --- Display links ---
        st.subheader("Links & Extras")
        links = plan.get("links", {})
        booking = links.get("booking", [])

        if isinstance(booking, dict):  # if model outputs dict
            st.write("Booking links:")
            for k, v in booking.items():
                st.write(f"- [{k.replace('_',' ').title()}]({v})")
        elif isinstance(booking, list):  # if model outputs list
            st.write("Booking links:")
            for link in booking:
                if isinstance(link, dict):
                    for k, v in link.items():
                        st.write(f"- [{k.replace('_',' ').title()}]({v})")
                else:
                    st.write(f"- [Booking Option]({link})")
        elif isinstance(booking, str):  # fallback if string
            st.write(f"- [Booking Link]({booking})")

        if "maps_search" in links:
            st.write(f"🗺 Map: [Open in Google Maps]({links['maps_search']})")

with col2:
    st.subheader("Map preview")
    lat, lng = lookup_coords(default_destination)
    embed_url = google_maps_embed_iframe_url(lat, lng, zoom=9)
    st.components.v1.html(
        f'<iframe src="{embed_url}" width="100%" height="400"></iframe>', height=420
    )
