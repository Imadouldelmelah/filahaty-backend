from pydantic import BaseModel
from typing import List, Optional

class YieldPredictionRequest(BaseModel):
    crop_name: str
    field_size_hectares: float
    monitoring_data: Optional[dict] = None
    weather_data: Optional[dict] = None
    field_id: Optional[str] = "default_field"

class YieldPredictionResponse(BaseModel):
    expected_yield: str
    confidence: str
    tips: List[str]
