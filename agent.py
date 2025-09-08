# agent.py
import os
import json
from typing import Dict, Any

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# local tools
from tools.booking_tool import booking_search_links
from tools.maps_tool import google_maps_search_url

# Chromadb persist dir
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_or_load_chroma():
    """
    Creates a Chroma vector store from the knowledge JSON if not present.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    if not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
        # populate from knowledge file
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
        vectordb.persist()
    else:
        vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return vectordb

# initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.2, openai_api_key=OPENAI_API_KEY)

booking_tool = Tool.from_function(
    func=booking_search_links,
    name="booking",
    description="Return booking search links for a destination."
)

maps_tool = Tool.from_function(
    func=google_maps_search_url,
    name="maps",
    description="Return a Google Maps search URL for a place or query."
)

def plan_trip_with_agent(destination: str, days: int, budget: int, prefer: str | None = None) -> Dict[str, Any]:
    """
    Top-level function to craft a trip plan. Uses:
      - ChromaDB to fetch local knowledge
      - LLM to synthesize an itinerary & budget
      - weather & booking tools
    """
    vectordb = create_or_load_chroma()
    # retrieve relevant docs
    docs = vectordb.similarity_search(destination, k=3)
    context_text = "\n".join([d.page_content for d in docs])

    # build a prompt for LLM
    prompt = PromptTemplate(
        input_variables=["destination", "days", "budget", "preferences", "context"],
        template=(
            "You are a helpful travel planner. Use the context to produce a concise 3-part output:\n\n"
            "1) Day-wise itinerary (for {days} days) for {destination}.\n"
            "2) Budget breakdown that keeps total <= ₹{budget}. Use categories: travel, stay, food, activities, buffer.\n"
            "3) Short bullet list of booking links and map URLs.\n\n"
            "Context: {context}\n"
            "User Preferences: {preferences}\n\n"
            "Return a JSON object with keys: itinerary (list of day strings), budget (dict), links (dict)."
        )
    )

    template_vals = {
        "destination": destination,
        "days": days,
        "budget": budget,
        "preferences": prefer or "no specific preference",
        "context": context_text
    }

    chain = LLMChain(llm=llm, prompt=prompt)
    llm_response = chain.run(template_vals)

    # try to parse JSON from LLM (expecting JSON). If not JSON, wrap in fallback.
    import json, re
    json_text = None
    try:
        # find JSON substring
        match = re.search(r"\{.*\}", llm_response, re.S)
        if match:
            json_text = match.group(0)
            plan = json.loads(json_text)
        else:
            # fallback: put llm_response into itinerary text
            plan = {
                "itinerary": [llm_response],
                "budget": {},
                "links": {}
            }
    except Exception:
        plan = {
            "itinerary": [llm_response],
            "budget": {},
            "links": {}
        }

    # Enrich plan with tool outputs
    bookings = booking_search_links(destination)
    maps_url = google_maps_search_url(destination)

    # ensure keys exist
    plan.setdefault("budget", {})
    plan.setdefault("links", {})
    plan["links"].setdefault("booking", bookings)
    plan["links"].setdefault("maps_search", maps_url)
    
    if not plan["budget"]:
        # naive split
        travel = int(budget * 0.25)
        stay = int(budget * 0.35)
        food = int(budget * 0.2)
        activities = int(budget * 0.15)
        buffer = budget - (travel + stay + food + activities)
        plan["budget"] = {
            "travel": travel,
            "stay": stay,
            "food": food,
            "activities": activities,
            "buffer": buffer
        }

    return plan
