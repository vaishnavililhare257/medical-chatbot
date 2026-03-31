from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

from retrieval.search_engine import load_models, search

app = FastAPI()

# 🔐 Gemini setup (replace with your new API key later)
genai.configure(api_key="api key")

# 🧠 Chat memory (session-based)
chat_sessions = {}

# 🧠 Smart doctor-like behavior
system_prompt = """
You are a professional medical assistant like a doctor.

Your goal is to help the user safely and correctly.

Rules:

- Understand the query carefully.
- If the question is clear → give a direct answer.
- If important info is missing → ask follow-up questions.
- Do NOT ask unnecessary questions.
- Keep responses concise (3–5 lines max).
- Use simple, natural conversational language.
- Avoid long paragraphs.
- Avoid bullet points unless necessary.
- Only suggest medicines when enough information is available.

Act like a real doctor helping a patient.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load SBERT model once
load_models()

class Query(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "Medical Chatbot API Running"}


@app.post("/chat")
def chat_api(query: Query):

    user_query = query.query
    session_id = "user1"   # simple session (can improve later)

    # 🔥 create new chat session if not exists
    if session_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_prompt
        )
        chat_sessions[session_id] = model.start_chat(history=[])

    chat = chat_sessions[session_id]

    # 🔥 SBERT context (helps accuracy)
    results = search(user_query, "sbert")
    context = results[0]["answer"][:300]

    # 🔥 clean + short prompt
    prompt = f"""
Context: {context}

User: {user_query}
"""

    response = chat.send_message(prompt)

    return {
        "answer": response.text
    }