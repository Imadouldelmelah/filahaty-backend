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
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Unified Intelligence Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to synthesize field intelligence.")
