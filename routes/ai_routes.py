import os
import requests
from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from services.ai_agronomist import ai_agronomist
from services.weather_service import weather_service
from pydantic import BaseModel
from typing import List
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
        
        return ChatResponse(response=response.json()["choices"][0]["message"]["content"])

    except Exception as e:
        logger.error(f"Chat Error: {str(e)}")
        return ChatResponse(response="AI assistant temporarily unavailable")

class AdviceRequest(BaseModel):
    crop: str
    stage: str
    weather: str
    soil: str
    journey_id: str = None
    lat: float = None
    lon: float = None

@router.post("/advice")
async def get_farming_advice_endpoint(request: AdviceRequest):
    """
    Highly specialized AI agronomy advice endpoint with context memory and weather sync support.
    """
    try:
        weather_data = None
        if request.lat and request.lon:
            weather_data = weather_service.get_weather(request.lat, request.lon)
            
        context = {
            "crop_name": request.crop,
            "current_stage": request.stage,
            "weather": request.weather if not weather_data else "Real-time Sync",
            "weather_data": weather_data,
            "soil": request.soil,
            "field_size": "Not specified",
            "journey_id": request.journey_id
        }
        
        result = await ai_agronomist.generate_advice(context)
        return result
        
    except Exception as e:
        logger.error(f"AI Advice Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Advice generator temporarily unavailable")
