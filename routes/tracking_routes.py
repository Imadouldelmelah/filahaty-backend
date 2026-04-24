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
    
    # 1. Fetch real-time monitoring data (Smart Agriculture Layer)
    from services.fake_monitoring_service import FakeMonitoringService
    monitoring_svc = FakeMonitoringService()
    monitoring_data = monitoring_svc.get_fake_monitoring_data(journey_id)
    
    # 2. Hybrid Guidance (AI with Rule-based fallback)
    from services.ai_agronomist import AIAgronomistService
    agronomist_svc = AIAgronomistService()
    
    context = {
        "crop_name": progress["crop"],
        "current_stage": progress["stage"],
        "day": progress["day"],
        "monitoring_data": monitoring_data,
        "history": progress.get("history", [])
    }
    
    # 3. Apply consolidated Smart Logic (Rule-based layer)
    from services.agronomy_engine import get_smart_journey_logic
    smart_guidance = get_smart_journey_logic(progress, monitoring_data)
    
    try:
        # Get hybrid advice (AI call will happen inside)
        advice_data = await agronomist_svc.generate_advice(context)
        
        return {
            "status": advice_data.get("status", "hybrid"),
            "journey_id": journey_id,
            "day": progress["day"],
            "stage": progress["stage"],
            "tasks": list(set(smart_guidance["tasks"] + advice_data.get("tasks", []))),
            "alerts": list(set(smart_guidance["alerts"] + advice_data.get("alerts", []))),
            "tips": list(set(smart_guidance["tips"] + advice_data.get("tips", []))),
            "monitoring": {
                "soil_moisture": monitoring_data.get("soil_moisture"),
                "temperature": monitoring_data.get("temperature"),
                "humidity": monitoring_data.get("humidity"),
                "nitrogen": monitoring_data.get("nitrogen"),
                "soil_ph": monitoring_data.get("soil_ph")
            }
        }
    except Exception as e:
        logger.error(f"JOURNEY_AI_EXCEPTION: {str(e)}")
        # Ultimate fallback
        return {
            "status": "rule_based_fallback",
            "journey_id": journey_id,
            "day": progress.get("day"),
            "stage": progress.get("stage"),
            "tasks": smart_guidance["tasks"],
            "alerts": smart_guidance["alerts"],
            "tips": smart_guidance["tips"],
            "monitoring": {
                "soil_moisture": monitoring_data.get("soil_moisture"),
                "temperature": monitoring_data.get("temperature"),
                "humidity": monitoring_data.get("humidity"),
                "nitrogen": monitoring_data.get("nitrogen"),
                "soil_ph": monitoring_data.get("soil_ph")
            }
        }

@router.get("/calendar/{journey_id}")
async def get_journey_calendar_endpoint(journey_id: str):
    """
    Generates a dynamic 30-day agricultural calendar based on current conditions.
    """
    from services.tracking_service import TrackingService
    from services.calendar_service import CalendarService
    from services.fake_monitoring_service import FakeMonitoringService
    
    tracking_svc = TrackingService()
    calendar_svc = CalendarService()
    monitoring_svc = FakeMonitoringService()
    
    progress = tracking_svc.get_progress(journey_id)
    if "error" in progress:
        raise HTTPException(status_code=404, detail=progress["error"])
        
    monitoring_data = monitoring_svc.get_fake_monitoring_data(journey_id)
    
    calendar = calendar_svc.generate_30_day_projection(
        crop_name=progress["crop"],
        current_day=progress["day"],
        monitoring_data=monitoring_data
    )
    
    return {
        "journey_id": journey_id,
        "crop": progress["crop"],
        "current_day": progress["day"],
        "calendar": calendar
    }
