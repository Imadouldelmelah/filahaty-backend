from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.ai_agronomist import ai_agronomist
from utils.logger import logger

router = APIRouter(prefix="/agronomist", tags=["AI Agronomist"])

class AgronomistContext(BaseModel):
    crop_name: str
    current_stage: str
    weather: str
    soil: str
    field_size: str

class AgronomistResponse(BaseModel):
    advice: str
    actions: List[str]

@router.post("/advice", response_model=AgronomistResponse)
async def get_agronomist_advice_endpoint(context: AgronomistContext):
    try:
        # Convert Pydantic model to dict
        context_dict = context.model_dump()
        result = await ai_agronomist.generate_advice(context_dict)
        
        if "error" in result and len(result) == 1: # Basic error handling from service
             raise HTTPException(status_code=500, detail="AI failed to generate structured advice")
             
        return AgronomistResponse(**result)
        
    except Exception as e:
        logger.error(f"Endpoint Error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI assistant temporarily unavailable")
