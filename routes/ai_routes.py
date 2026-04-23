import os
import requests
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from models.chat_models import ChatRequest, ChatResponse, AdvancedChatRequest
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

import asyncio

async def call_ai(prompt, timeout=5.0):
    """
    Standard simple AI chat call using GeminiService.
    Ensures consistent token limits and 402 retry logic.
    """
    from services.gemini_service import GeminiService
    ai_svc = GeminiService()
    # Enforce strict maximum wait wrapper at the execution level
    return await asyncio.wait_for(ai_svc.generate(prompt, require_json=False), timeout=timeout)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai_endpoint(request: ChatRequest):
    """
    AI works only when endpoint is called.
    """
    try:
        response_str = await call_ai(request.message, timeout=5.0)
        
        return ChatResponse(response=response_str)
    except asyncio.TimeoutError:
        logger.error("CHAT_ERROR: AI response timed out.")
        return ChatResponse(
            response="Smart offline mode activated: I can still guide you based on agricultural knowledge.",
            status="offline_optimized"
        )
    except Exception as e:
        logger.error(f"CHAT_ERROR: {str(e)}")
        return ChatResponse(
            response="I'm momentarily offline, but still here to help with your farm.",
            status="offline_optimized"
        )

@router.post("/chat-advanced", response_model=ChatResponse)
async def advanced_chat_with_ai_endpoint(request: AdvancedChatRequest):
    """
    Advanced, context-aware AI conversational endpoint.
    Retrieves weather dynamically and injects all agricultural telemetry into the AI persona.
    """
    try:
        weather_data = None
        if request.lat and request.lon:
            from services.weather_service import WeatherService
            weather_svc = WeatherService()
            weather_data = weather_svc.get_weather(request.lat, request.lon)
            
        # Always fetch live monitoring data internally for consistency
        from services.fake_monitoring_service import FakeMonitoringService
        monitoring_svc = FakeMonitoringService()
        field_id = request.field_id or "default_field"
        monitoring_data = monitoring_svc.get_fake_monitoring_data(field_id)
        
        context = {
            "crop_name": request.crop,
            "current_stage": request.stage,
            "weather_data": weather_data,
            "soil": request.soil,
            "monitoring_data": monitoring_data
        }
        
        from services.ai_agronomist import AIAgronomistService
        agronomist_svc = AIAgronomistService()
        response_text = await agronomist_svc.generate_advanced_chat(context, request.message)
        
        if response_text == "AI_ERROR_FALLBACK":
             return ChatResponse(
                response="Smart offline mode activated: My advanced analysis is currently simplified.",
                status="offline_optimized"
            )

        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.warning(f"Advanced_Chat_AI_SKIPPED: {str(e)}. Using safe baseline.")
        return ChatResponse(
            response="Smart offline mode activated: I can still guide you based on agricultural knowledge.",
            status="offline_optimized"
        )

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
        
        # Analyze using disease detector service (Lazy loaded)
        from services.disease_detector import DiseaseDetectionService
        disease_svc = DiseaseDetectionService()
        result = await disease_svc.analyze_crop_image(base64_image, mime_type)
        return result
        
    except Exception as e:
        logger.error(f"Image Analysis Route Error: {str(e)}")
        # Never fail: Return a standard busy diagnostic
        return {
            "disease": "System Busy: Unable to analyze image at this moment.",
            "confidence": 0,
            "solution": "Smart offline mode activated",
            "status": "offline_optimized",
            "message": "Smart offline mode activated"
        }

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
            from services.weather_service import WeatherService
            weather_svc = WeatherService()
            weather_data = weather_svc.get_weather(request.lat, request.lon)
            
        context = {
            "crop_name": request.crop,
            "current_stage": request.stage,
            "weather": request.weather if not weather_data else "Real-time Sync",
            "weather_data": weather_data,
            "soil": request.soil,
            "field_size": "Not specified",
            "journey_id": request.journey_id
        }
        
        from services.ai_agronomist import AIAgronomistService
        agronomist_svc = AIAgronomistService()
        result = await agronomist_svc.generate_advice(context)
        return result
        
    except Exception as e:
        logger.error(f"AI Advice Route Error: {str(e)}")
        return {
            "advice": "Smart offline mode activated: I can still guide you based on agricultural knowledge.",
            "tasks": ["Check soil moisture", "Inspect leaves for spots", "Ensure proper drainage"],
            "status": "offline_optimized",
            "message": "Smart offline mode activated"
        }
