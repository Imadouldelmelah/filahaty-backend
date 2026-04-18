from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

from typing import Optional

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

class AdvancedChatRequest(BaseModel):
    message: str
    crop: Optional[str] = None
    stage: Optional[str] = None
    weather: Optional[str] = None
    soil: Optional[str] = None
    monitoring_data: Optional[dict] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    field_id: Optional[str] = "default_field"

