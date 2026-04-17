from fastapi import APIRouter, HTTPException
from models.agronomy_models import AgronomyRequest
from services.agronomy_engine import get_crop_plan
from utils.logger import logger

router = APIRouter(prefix="/agronomy", tags=["Agronomy Engine"])

@router.post("/plan")
async def get_agronomy_plan_endpoint(request: AgronomyRequest):
    """
    POST /agronomy/plan
    Returns a structured crop plan for the requested crop.
    """
    crop = request.crop
    logger.info(f"Agronomy Request: Fetching plan for {crop}")
    
    plan = get_crop_plan(crop)
    
    # Check if the engine returned an error
    if "error" in plan:
        logger.warning(f"Agronomy Error: Plan for '{crop}' not found")
        # We can return 404 or just return the JSON with error as defined in engine
        # Let's return a 404 for unknown crops to follow REST best practices
        raise HTTPException(status_code=404, detail=plan)
    
    return plan
