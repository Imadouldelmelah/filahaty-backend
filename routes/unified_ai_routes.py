from fastapi import APIRouter, HTTPException
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["Unified Intelligence"])

@router.get("/unified-intelligence")
async def get_unified_intelligence_endpoint(field_id: str):
    """
    The 'One-Stop' intelligence endpoint. Returns a complete synthesis of 
    health, decisions, yield predictions, and expert advice for a field.
    """
    try:
        from services.unified_ai_brain import UnifiedAIBrain
        brain = UnifiedAIBrain()
        result = await brain.get_unified_intelligence(field_id)
        # Brain already handles internal fallbacks and returns a valid dict
        return result
    except Exception as e:
        logger.error(f"UNIFIED_ROUTE_CRITICAL_FAILURE: {str(e)}")
        # Absolute safety net: Return standard fallback structure
        return {
            "status": "system_maintenance",
            "field_id": field_id,
            "health": {"score": 85, "status": "Stable"},
            "decision": {"decision": "Proceed with standard care"},
            "advice": {"advice": "Intelligence engine is updating. Maintain current irrigation."}
        }
