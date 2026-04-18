from fastapi import APIRouter, HTTPException
from models.agronomy_models import AgronomyRequest
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
    
    from services.agronomy_engine import get_crop_plan
    plan = get_crop_plan(crop)
    
    # Check if the engine returned an error
    if "error" in plan:
        logger.warning(f"Agronomy Error: Plan for '{crop}' not found")
        raise HTTPException(status_code=404, detail=plan)
    
    return plan
