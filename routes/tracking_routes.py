from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.tracking_service import tracking_service
from services.ai_agronomist import ai_agronomist
from services.weather_service import weather_service
from services.fake_monitoring_service import fake_monitoring_service
from utils.logger import logger

router = APIRouter(prefix="/tracking", tags=["Crop Tracking"])

class JourneyStartRequest(BaseModel):
    crop: str
    start_date: str
    lat: float = None
    lon: float = None

class ActionRecordRequest(BaseModel):
    journey_id: str
    action: str

@router.post("/start")
async def start_farming_journey_endpoint(request: JourneyStartRequest):
    try:
        journey_id = tracking_service.start_journey(
            request.crop, 
            request.start_date,
            request.lat,
            request.lon
        )
        return {"journey_id": journey_id, "status": "started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/progress/{journey_id}")
async def get_farming_progress_endpoint(journey_id: str):
    result = tracking_service.get_progress(journey_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/action/record")
async def record_farming_action_endpoint(request: ActionRecordRequest):
    """
    Endpoint to record a completed farming action.
    """
    result = tracking_service.record_action(request.journey_id, request.action)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/guidance/{journey_id}")
async def get_journey_guidance_endpoint(journey_id: str):
    """
    Expert guidance based on journey progress + AI enhancement.
    """
    progress = tracking_service.get_progress(journey_id)
    if "error" in progress:
        raise HTTPException(status_code=404, detail=progress["error"])
    
    # Fetch real-time weather based on coordinates
    weather_data = None
    if progress.get("latitude") and progress.get("longitude"):
        weather_data = weather_service.get_weather(progress["latitude"], progress["longitude"])
    
    # Fetch real-time monitoring data for the field
    monitoring_data = fake_monitoring_service.get_field_monitoring_data(journey_id)
    
    # context for AI
    context = {
        "crop_name": progress["crop"],
        "current_stage": progress["stage"],
        "journey_id": journey_id,
        "weather": "Dynamic" if weather_data else "Sunny", 
        "weather_data": weather_data,
        "monitoring_data": monitoring_data,
        "soil": "Sandy",
        "field_size": "Standard"
    }
    
    advice = await ai_agronomist.generate_advice(context)
    return {
        "progress": progress,
        "ai_advice": advice
    }
