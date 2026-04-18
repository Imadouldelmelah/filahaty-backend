from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
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
        from services.tracking_service import TrackingService
        tracking_svc = TrackingService()
        journey_id = tracking_svc.start_journey(
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
    from services.tracking_service import TrackingService
    tracking_svc = TrackingService()
    result = tracking_svc.get_progress(journey_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/action/record")
async def record_farming_action_endpoint(request: ActionRecordRequest):
    """
    Endpoint to record a completed farming action.
    """
    from services.tracking_service import TrackingService
    tracking_svc = TrackingService()
    result = tracking_svc.record_action(request.journey_id, request.action)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/guidance/{journey_id}")
async def get_journey_guidance_endpoint(journey_id: str):
    """
    Expert guidance based on journey progress + AI enhancement.
    """
    from services.tracking_service import TrackingService
    tracking_svc = TrackingService()
    progress = tracking_svc.get_progress(journey_id)
    if "error" in progress:
        raise HTTPException(status_code=404, detail=progress["error"])
    
    # Fetch real-time weather based on coordinates
    weather_data = None
    if progress.get("latitude") and progress.get("longitude"):
        from services.weather_service import WeatherService
        weather_svc = WeatherService()
        weather_data = weather_svc.get_weather(progress["latitude"], progress["longitude"])
    
    # Fetch real-time monitoring data for the field
    from services.fake_monitoring_service import FakeMonitoringService
    monitoring_svc = FakeMonitoringService()
    monitoring_data = monitoring_svc.get_fake_monitoring_data(journey_id)
    
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
    
    from services.ai_agronomist import AIAgronomistService
    agronomist_svc = AIAgronomistService()
    advice = await agronomist_svc.generate_advice(context)
    return {
        "progress": progress,
        "ai_advice": advice
    }
