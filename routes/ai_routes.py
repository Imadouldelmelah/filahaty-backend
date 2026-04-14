import os
import requests
from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai_endpoint(request: ChatRequest):
    message = request.message
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Filahaty AI, an agricultural expert helping farmers in Algeria."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
        )
        
        # Consistent return format
        return ChatResponse(response=response.json()["choices"][0]["message"]["content"])

    except Exception as e:
        print("Chat Error:", str(e))
        return ChatResponse(response="AI assistant temporarily unavailable")
