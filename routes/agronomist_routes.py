from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils.logger import logger

router = APIRouter(prefix="/agronomist", tags=["AI Agronomist"])

class AgronomistContext(BaseModel):
    crop_name: str
    current_stage: str
    weather: str
    soil: str
    field_size: str
    field_id: str = "default_field"
    monitoring_data: dict = None
    lang: str = "en"

class AgronomistResponse(BaseModel):
    advice: str
    actions: List[str]

@router.post("/advice", response_model=AgronomistResponse)
async def get_agronomist_advice_endpoint(context: AgronomistContext):
    try:
        # Convert Pydantic model to dict
        context_dict = context.model_dump()
        # Always fetch live monitoring data internally for consistency
        from services.fake_monitoring_service import FakeMonitoringService
        monitoring_svc = FakeMonitoringService()
        field_id = context_dict.get("field_id", "default_field")
        context_dict["monitoring_data"] = monitoring_svc.get_fake_monitoring_data(field_id)
        
        from services.ai_agronomist import AIAgronomistService
        agronomist_svc = AIAgronomistService()
        result = await agronomist_svc.generate_advice(context_dict)
        
        if "error" in result and len(result) == 1: # Basic error handling from service
             raise HTTPException(status_code=500, detail="AI failed to generate structured advice")
             
        return AgronomistResponse(**result)
        
    except Exception as e:
        logger.error(f"Endpoint Error: {str(e)}")
        # Guaranteed structured JSON fallback
        from services.agronomy_engine import _t
        lang = context.lang if hasattr(context, "lang") else "en"
        return AgronomistResponse(
            advice=_t("baseline_advice", lang),
            actions=_t("baseline_tasks", lang)
        )
