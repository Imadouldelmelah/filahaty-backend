from pydantic import BaseModel

class SoilData(BaseModel):
    nitrogen: int
    phosphorus: int
    potassium: int
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class MSPRequest(BaseModel):
    crop_name: str
    current_year: int = 2024
