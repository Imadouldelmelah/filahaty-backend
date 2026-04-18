from fastapi import APIRouter, HTTPException
from models.marketplace_models import MarketplaceItem, MarketplaceItemCreate
from services.marketplace_service import marketplace_service
from typing import List
from utils.logger import logger

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

@router.post("/add", response_model=MarketplaceItem)
async def add_marketplace_item(item: MarketplaceItemCreate):
    """
    Allows a farmer to list a crop for sale.
    """
    try:
        new_item = marketplace_service.add_item(item.model_dump())
        logger.info(f"Marketplace item added: {new_item['crop_name']} by {new_item['farmer_name']}")
        return new_item
    except Exception as e:
        logger.error(f"Error adding marketplace item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add item to marketplace.")

@router.get("/list", response_model=List[MarketplaceItem])
async def list_marketplace_items():
    """
    Allows buyers to browse all products for sale.
    """
    try:
        return marketplace_service.list_items()
    except Exception as e:
        logger.error(f"Error listing marketplace items: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve marketplace items.")
