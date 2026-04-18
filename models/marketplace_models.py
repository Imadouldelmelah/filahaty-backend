from pydantic import BaseModel
from typing import Optional

class MarketplaceItemCreate(BaseModel):
    farmer_name: str
    crop_name: str
    price: float
    unit: str
    location: str

class MarketplaceItem(BaseModel):
    id: str
    farmer_name: str
    crop_name: str
    price: float
    unit: str
    location: str
    timestamp: str
