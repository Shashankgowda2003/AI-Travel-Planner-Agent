# agent.py
import os
import json
import logging
import time
from typing import Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

from config import settings

# local tools
from tools.booking_tool import booking_search_links
from tools.maps_tool import google_maps_search_url
from tools.weather_tool import get_weather_forecast, format_weather_context
from langchain_classic.memory import ConversationBufferMemory
from utils import compute_fallback_budget
from trip_types import TripPlan

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Chromadb persist dir
PERSIST_DIR = settings.chroma_persist_dir

if not settings.openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY is not set. Create a .env file with your OpenAI API key "
        "or set the OPENAI_API_KEY environment variable."
    )

def create_or_load_chroma():
    """
    Creates a Chroma vector store from the knowledge JSON if not present.
    """
    embeddings = OpenAIEmbeddings()
    if not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
        # populate from knowledge file
        knowledge_file = os.path.join("knowledge", "india_destinations.json")
        if not os.path.exists(knowledge_file):
            knowledge_file = os.path.join("knowledge", "goa_itineraries.json")
        docs = []
        try:
            with open(knowledge_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                docs.append(Document(page_content=item["content"], metadata={"title": item["title"], "id": item["id"]}))
        except Exception as e:
            # fallback doc
            docs.append(Document(page_content="Goa is a coastal state in India known for beaches.", metadata={"title":"fallback","id":"fb"}))
        vectordb = Chroma.from_documents(docs, embeddings, persist_directory=PERSIST_DIR)
    else:
        vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return vectordb

# initialize LLM
llm = ChatOpenAI(
    model=settings.model_name,
    temperature=settings.temperature,
    model_kwargs={"response_format": {"type": "json_object"}},
)

ORIGIN = settings.origin_city

def plan_trip_with_agent(destination: str, days: int, budget: int, prefer: Optional[str] = None, memory: Optional[ConversationBufferMemory] = None) -> TripPlan:
    """
    Top-level function to craft a trip plan. Uses:
      - ChromaDB to fetch local knowledge
      - LLM to synthesize an itinerary & budget
      - weather & booking tools
      - optional ConversationBufferMemory for multi-turn refinement
    """
    logger.info("Loading ChromaDB from %s", PERSIST_DIR)
    t0 = time.time()
    vectordb = create_or_load_chroma()
    logger.info("ChromaDB loaded in %.2fs", time.time() - t0)

    # retrieve relevant docs
    docs = vectordb.similarity_search(destination, k=3)
    context_text = "\n".join([d.page_content for d in docs])
    logger.info("Retrieved %d docs for destination '%s'", len(docs), destination)

    # fetch weather forecast
    weather_data = get_weather_forecast(destination, days=days)
    weather_context = format_weather_context(weather_data)
    logger.info("Weather fetched for %s", destination)

    # build a prompt for LLM
    prompt = PromptTemplate(
        input_variables=["destination", "days", "budget", "preferences", "context", "weather", "chat_history"],
        template=(
            "You are a helpful travel planner. Use the context and weather to produce a concise output:\n\n"
            "1) Day-wise itinerary (for {days} days) for {destination}. Adjust activities based on weather "
            "(e.g., indoor activities on rainy days, outdoor on clear days, early morning tours on hot days).\n"
            "2) Budget breakdown that keeps total <= ₹{budget}. Use categories: travel, stay, food, activities, buffer.\n"
            "3) Short bullet list of booking links and map URLs.\n\n"
            "Context: {context}\n"
            "Weather Forecast:\n{weather}\n"
            "User Preferences: {preferences}\n\n"
            "Previous conversation (for refinement): {chat_history}\n\n"
            "Return a JSON object with keys: itinerary (list of day strings), budget (dict), links (dict)."
        )
    )

    # Include chat history from memory if provided
    chat_context = ""
    if memory and memory.chat_memory and memory.chat_memory.messages:
        chat_context = "\n".join(
            [f"{'User' if m.type == 'human' else 'Assistant'}: {m.content}"
             for m in memory.chat_memory.messages[-6:]]
        )
        logger.info("Loaded %d previous messages from memory", len(memory.chat_memory.messages))

    template_vals = {
        "destination": destination,
        "days": days,
        "budget": budget,
        "preferences": prefer or "no specific preference",
        "context": context_text,
        "weather": weather_context,
        "chat_history": chat_context
    }

    chain = LLMChain(llm=llm, prompt=prompt)

    # Try primary model, then fallback models on failure
    models_to_try = [settings.model_name] + [m for m in settings.fallback_models if m != settings.model_name]
    last_error = None
    llm_response = ""

    for attempt, model_name in enumerate(models_to_try):
        try:
            if attempt > 0:
                logger.warning("Retrying with fallback model: %s", model_name)
                chain = LLMChain(
                    llm=ChatOpenAI(
                        model=model_name,
                        temperature=settings.temperature,
                        model_kwargs={"response_format": {"type": "json_object"}},
                    ),
                    prompt=prompt,
                )
            logger.info("Calling LLM for %s (%d days, \u20b9%d) with model %s", destination, days, budget, model_name)
            t0 = time.time()
            result = chain.invoke(template_vals)
            llm_response = result.get("text", "") if isinstance(result, dict) else str(result)
            logger.info("LLM call completed in %.2fs", time.time() - t0)
            break
        except Exception as e:
            logger.warning("Model %s failed: %s", model_name, e)
            last_error = e
            if attempt < len(models_to_try) - 1:
                backoff = 2 ** attempt
                logger.info("Waiting %ds before next attempt...", backoff)
                time.sleep(backoff)
    else:
        raise RuntimeError(f"All models failed. Last error: {last_error}") from last_error

    # Parse JSON from LLM (structured output ensures valid JSON)
    try:
        plan = json.loads(llm_response)
    except json.JSONDecodeError:
        logger.warning("JSON parse failed on LLM response, using fallback")
        plan = {
            "itinerary": [llm_response],
            "budget": {},
            "links": {}
        }

    # Enrich plan with tool outputs
    bookings = booking_search_links(destination, origin=ORIGIN)
    maps_url = google_maps_search_url(destination)

    # ensure keys exist
    plan.setdefault("budget", {})
    plan.setdefault("links", {})
    plan["links"].setdefault("booking", bookings)
    plan["links"].setdefault("maps_search", maps_url)
    
    if not plan["budget"]:
        logger.info("No budget in LLM response, using fallback split")
        plan["budget"] = compute_fallback_budget(budget)

    return plan
