# ✈️ AI Travel Planner Agent

An **AI-powered travel planning assistant** built with **LangChain**, **OpenAI**, **ChromaDB**, and **Streamlit**.  
It generates day-wise itineraries, budget breakdowns, and useful booking & map links, personalized to your preferences.

---

## 🚀 Features
- **Smart Trip Planning**  
  Generates a structured itinerary for any destination using GPT.
  
- **Budget Estimation**  
  Provides category-wise cost breakdown (travel, stay, food, activities, buffer).

- **Booking & Maps Integration**  
  Returns booking links (bus, train, flights, hotels) and Google Maps URLs.

- **Knowledge Base**  
  Uses **ChromaDB** to store and retrieve local travel knowledge (e.g., Goa itineraries).

- **Interactive Web UI**  
  Built with **Streamlit** for a simple and user-friendly experience.

---

## 🛠️ Tech Stack
- [Python]
- [LangChain]
- [OpenAI API] 
- [ChromaDB] 
- [Streamlit] 

---

## 📂 Project Structure

├── agent.py # Core agent logic (LLM + ChromaDB + tools)
├── app.py # Streamlit app frontend
├── tools/
│ ├── booking_tool.py # Generates booking search links
│ └── maps_tool.py # Generates Google Maps search & embed URLs
├── knowledge/
│ └── goa_itineraries.json # Example knowledge base (custom itineraries)
├── chroma_db/ # Persisted Chroma vector store (auto-created)
├── .env # API keys and configs
└── README.md # Project documentation

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner

### 2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_MAPS_API_KEY=add yout google map API key 
CHROMA_PERSIST_DIR=./chroma_db

### 5. Running the App
streamlit run app.py
