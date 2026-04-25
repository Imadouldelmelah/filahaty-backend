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
    lang = request.lang if hasattr(request, "lang") else "en"
    logger.info(f"Agronomy Request: Fetching plan for {crop} in {lang}")
    
    try:
        from services.agronomy_engine import get_crop_plan
        plan = get_crop_plan(crop, lang=lang)
    except Exception as e:
        logger.error(f"Endpoint Error: {str(e)}")
        # Guaranteed structured JSON fallback
        from services.agronomy_engine import _t
        from models.agronomy_models import AgronomistResponse
        return AgronomistResponse(
            advice=_t("baseline_advice", lang),
            actions=_t("baseline_tasks", lang)
        )
    
    # Check if the engine returned an error
    if "error" in plan:
        logger.warning(f"Agronomy Error: Plan for '{crop}' not found")
        raise HTTPException(status_code=404, detail=plan)
    
    return plan
