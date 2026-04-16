from pydantic import BaseModel
from typing import Optional

class SoilData(BaseModel):
    nitrogen: Optional[int] = 50
    phosphorus: Optional[int] = 50
    potassium: Optional[int] = 50
    temperature: Optional[float] = 25.0
    humidity: Optional[float] = 60.0
    ph: Optional[float] = 6.5
    rainfall: Optional[float] = 500.0

class MSPRequest(BaseModel):
    crop_name: str
    current_year: int = 2024
