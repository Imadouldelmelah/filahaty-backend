import os
import requests
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from models.chat_models import ChatRequest, ChatResponse, AdvancedChatRequest
from services.ai_agronomist import ai_agronomist
from services.disease_detector import disease_detector_service
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

@router.post("/chat-advanced", response_model=ChatResponse)
async def advanced_chat_with_ai_endpoint(request: AdvancedChatRequest):
    """
    Advanced, context-aware AI conversational endpoint.
    Retrieves weather dynamically and injects all agricultural telemetry into the AI persona.
    """
    try:
        weather_data = None
        if request.lat and request.lon:
            weather_data = weather_service.get_weather(request.lat, request.lon)
            
        context = {
            "crop_name": request.crop,
            "current_stage": request.stage,
            "weather_data": weather_data,
            "soil": request.soil,
            "monitoring_data": request.monitoring_data
        }
        
        response_text = await ai_agronomist.generate_advanced_chat(context, request.message)
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Advanced Chat Error: {str(e)}")
        return ChatResponse(error="AI assistant temporarily unavailable", response="Sorry, I am facing a temporary system issue.")

@router.post("/analyze-image")
async def analyze_plant_image(file: UploadFile = File(...)):
    """
    Visual plant disease detection endpoint.
    Accepts an image and returns a diagnosis, confidence level, and solution.
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Encode to base64
        base64_image = base64.b64encode(contents).decode("utf-8")
        
        # Get mime type
        mime_type = file.content_type or "image/jpeg"
        
        # Analyze using disease detector service
        result = await disease_detector_service.analyze_crop_image(base64_image, mime_type)
        return result
        
    except Exception as e:
        logger.error(f"Image Analysis Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image analysis service temporarily unavailable")

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
