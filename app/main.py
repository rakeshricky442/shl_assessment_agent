from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import SHLAgent

# --------------------------------------------------
# Initialize FastAPI
# --------------------------------------------------

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="AI-powered SHL Assessment Recommendation Assistant",
    version="1.0.0"
)

# Load the AI agent only once
agent = SHLAgent()

# --------------------------------------------------
# Request Model
# --------------------------------------------------

from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]

# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "SHL Assessment Recommendation API",
        "status": "running"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:
        response = agent.chat(request.messages)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
