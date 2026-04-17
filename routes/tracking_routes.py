from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.tracking_service import tracking_service
from services.guidance_service import guidance_service

router = APIRouter(prefix="/tracking", tags=["Crop Tracking"])

class StartJourneyRequest(BaseModel):
    crop_name: str
    start_date: str # YYYY-MM-DD

@router.post("/start")
async def start_journey_endpoint(request: StartJourneyRequest):
    try:
        journey_id = tracking_service.start_journey(request.crop_name, request.start_date)
        return {"journey_id": journey_id, "status": "started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/progress/{journey_id}")
async def get_progress_endpoint(journey_id: str):
    progress = tracking_service.get_progress(journey_id)
    if "error" in progress:
        raise HTTPException(status_code=404, detail=progress["error"])
    return progress

@router.get("/guidance/{journey_id}")
async def get_guidance_endpoint(journey_id: str):
    guidance = await guidance_service.get_daily_guidance(journey_id)
    if "error" in guidance:
        raise HTTPException(status_code=400, detail=guidance["error"])
    return guidance
