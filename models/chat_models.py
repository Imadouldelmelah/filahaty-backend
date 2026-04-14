from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

from typing import Optional

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None
