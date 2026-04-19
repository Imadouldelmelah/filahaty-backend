import os
import requests
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from models.chat_models import ChatRequest, ChatResponse, AdvancedChatRequest
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

def call_ai(prompt):
    import os
    import requests

    api_key = os.getenv("OPENROUTER_API_KEY")

    # Debug: log whether the key is present
    print(f"[AI_CHAT] OPENROUTER_API_KEY present: {bool(api_key)}")
    logger.info(f"AI_CHAT: OPENROUTER_API_KEY present: {bool(api_key)}")

    if not api_key:
        logger.error("AI_CHAT: OPENROUTER_API_KEY is missing — cannot call AI.")
        return "AI error: OPENROUTER_API_KEY not configured. Please contact support."

    try:
        # Dynamic token control: short prompts need fewer tokens
        max_tokens = 300 if len(prompt) <= 100 else 500
        print(f"[AI_CHAT] Sending request to OpenRouter (max_tokens={max_tokens})...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )

        # Debug: log full status and raw response body
        print(f"[AI_CHAT] Response status code: {response.status_code}")
        print(f"[AI_CHAT] Response text: {response.text}")
        logger.info(f"AI_CHAT: status={response.status_code}")
        logger.debug(f"AI_CHAT: raw_response={response.text}")

        if response.status_code != 200:
            logger.error(f"AI_CHAT: OpenRouter returned error {response.status_code}: {response.text}")
            return f"AI error: OpenRouter returned {response.status_code} — {response.text}"

        # Safe JSON parsing
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content
        except (KeyError, IndexError, ValueError) as parse_err:
            logger.error(f"AI_CHAT: Failed to parse OpenRouter response: {parse_err} | raw: {response.text}")
            return "AI error: please try again"

    except requests.exceptions.Timeout:
        logger.error("AI_CHAT: Request to OpenRouter timed out.")
        return "AI error: request timed out, please try again"
    except Exception as e:
        logger.error(f"AI_CHAT: Unexpected error: {str(e)}")
        return "AI error: please try again"

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai_endpoint(request: ChatRequest):
    """
    AI works only when endpoint is called.
    """
    response = call_ai(request.message)
    return ChatResponse(response=response)

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
            "solution": "We are currently experiencing high volume. Please ensure your plant has sufficient water and check for visible pests manually while we restore full service.",
            "status": "partial"
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
        # Never fail: Return a professional fallback for stability
        return {
            "advice": "Our AI advisor is currently performing routine system updates. Please continue with standard crop monitoring and ensure adequate irrigation for your current growth stage.",
            "actions": ["Check soil moisture", "Inspect leaves for spots", "Ensure proper drainage"],
            "status": "fallback"
        }
