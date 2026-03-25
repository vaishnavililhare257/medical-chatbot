from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

from retrieval.search_engine import load_models, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load models once when server starts
load_models()

class Query(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "Medical Chatbot API Running"}

@app.post("/chat")
def chat(query: Query):

    user_query = query.query

    # use best model 
    results = search(user_query, "sbert")

    best = results[0]

    answer = results[0]["answer"][:500]

    return {
        "query": user_query,
        "answer": answer
    }