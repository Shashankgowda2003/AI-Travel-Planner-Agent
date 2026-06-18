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
from langchain_classic.memory import ConversationBufferMemory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("\u2708\ufe0f AI Travel Planner Agent")

if not settings.openai_api_key:
    st.error("OPENAI_API_KEY is not set. Create a .env file with your OpenAI API key.")
    st.stop()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

with st.sidebar:
    st.header("Default Trip Parameters")
    default_destination = st.text_input("Destination", value="Goa")
    default_days = st.number_input("Number of days", min_value=1, max_value=settings.max_days, value=settings.default_days)
    default_budget = st.number_input("Budget (\u20b9)", min_value=500, value=settings.default_budget, step=500)
    prefer = st.text_input("Preferences", value="beach, budget")

col1, col2 = st.columns((2, 1))

with col1:
    st.subheader("Your Trip Request")
    query = st.text_area(
        "Enter your request:",
        value=f"Plan me a {default_days}-day trip to {default_destination} under \u20b9{default_budget}. Preferences: {prefer}",
    )

    if st.button("Plan Trip"):
        dest, days, budget = default_destination, default_days, default_budget

        match = re.search(r"(\d+)[ -]?day", query, re.I)
        if match:
            days = int(match.group(1))
        match = re.search(r"under\s*\u20b9?(\d+)", query, re.I)
        if match:
            budget = int(match.group(1))
        match = re.search(r"trip to (.+?)\s*(?:under|for|in\s*\d|\d+\s*day|$)", query, re.I)
        if match:
            dest = match.group(1).strip()

        pref_match = re.search(r"preferences?:\s*(.+?)(?:$)", query, re.I)
        if pref_match:
            active_prefer = pref_match.group(1).strip()
        else:
            active_prefer = prefer

        logger.info("Planning trip: dest=%s, days=%d, budget=%d, preferences=%s", dest, days, budget, active_prefer)

        st.session_state.memory.chat_memory.add_user_message(query)

        try:
            with st.spinner(f"Planning {days}-day trip to {dest} within \u20b9{budget}..."):
                plan = plan_trip_with_agent(dest, days, budget, active_prefer, memory=st.session_state.memory)
        except Exception as e:
            logger.error("Trip planning failed: %s", e, exc_info=True)
            st.error(f"Failed to generate trip plan: {e}")
            st.info("Try reducing days/budget or selecting a different destination.")
            st.stop()

        ai_summary = f"Trip planned for {dest}: {len(plan.get('itinerary', []))} day itinerary, total budget \u20b9{budget}."
        st.session_state.memory.chat_memory.add_ai_message(ai_summary)
        st.session_state.last_plan = plan
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "assistant", "content": ai_summary})

        st.success("Plan ready!")
        st.subheader("Itinerary")
        for idx, d in enumerate(plan.get("itinerary", []), start=1):
            clean_day = re.sub(r"^Day\s*\d+:?\s*", "", d, flags=re.I).strip()
            st.markdown(f"**Day {idx}:** {clean_day}")

        st.subheader("Budget Breakdown (\u20b9)")
        budget_dict = plan.get("budget", {})
        for k, v in budget_dict.items():
            clean_val = str(v).replace("\u20b9\u20b9", "\u20b9")
            st.write(f"- **{k.capitalize()}**: {clean_val}")

        st.subheader("Links & Extras")
        links = plan.get("links", {})
        booking = links.get("booking", [])

        if isinstance(booking, dict):
            st.write("Booking links:")
            for k, v in booking.items():
                st.write(f"- [{k.replace('_',' ').title()}]({v})")
        elif isinstance(booking, list):
            st.write("Booking links:")
            for link in booking:
                if isinstance(link, dict):
                    for k, v in link.items():
                        st.write(f"- [{k.replace('_',' ').title()}]({v})")
                else:
                    st.write(f"- [Booking Option]({link})")
        elif isinstance(booking, str):
            st.write(f"- [Booking Link]({booking})")

        if "maps_search" in links:
            st.write(f"\U0001f5fa Map: [Open in Google Maps]({links['maps_search']})")

    if st.session_state.get("last_plan"):
        st.divider()
        st.subheader("Refine Your Trip")
        refine_query = st.text_input("Ask for changes (e.g., 'add more adventure activities', 'reduce budget')", key="refine_input")
        if st.button("Refine Plan") and refine_query:
            last_plan = st.session_state.last_plan
            if last_plan:
                st.session_state.memory.chat_memory.add_user_message(refine_query)
                try:
                    with st.spinner("Refining your trip plan..."):
                        refined_plan = plan_trip_with_agent(
                            default_destination, default_days, default_budget,
                            f"{prefer} | Refinement: {refine_query}",
                            memory=st.session_state.memory,
                        )
                    st.session_state.last_plan = refined_plan
                    st.session_state.memory.chat_memory.add_ai_message(f"Plan refined with: {refine_query}")
                    st.session_state.chat_history.append({"role": "user", "content": refine_query})
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Plan refined with: {refine_query}"})
                    st.success("Plan refined!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Refinement failed: {e}")

    if st.session_state.get("chat_history"):
        with st.expander("Conversation History"):
            for msg in st.session_state.chat_history:
                role = "You" if msg["role"] == "user" else "Assistant"
                st.markdown(f"**{role}:** {msg['content'][:200]}{'...' if len(msg['content']) > 200 else ''}")

        if st.button("Clear Conversation"):
            st.session_state.memory = ConversationBufferMemory()
            st.session_state.chat_history = []
            st.session_state.last_plan = None
            st.rerun()

with col2:
    st.subheader("Map preview")
    lat, lng = lookup_coords(default_destination)
    embed_url = google_maps_embed_iframe_url(lat, lng, zoom=9)
    st.components.v1.html(
        f'<iframe src="{embed_url}" width="100%" height="400"></iframe>', height=420
    )
