from pydantic import BaseModel
from typing import List, Optional

class YieldPredictionRequest(BaseModel):
    crop_name: str
    field_size_hectares: float
    monitoring_data: dict
    weather_data: Optional[dict] = None

class YieldPredictionResponse(BaseModel):
    expected_yield: str
    confidence: str
    tips: List[str]
