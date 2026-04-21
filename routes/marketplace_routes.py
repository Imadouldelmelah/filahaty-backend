from fastapi import APIRouter, HTTPException
from models.marketplace_models import MarketplaceItem, MarketplaceItemCreate
from typing import List
from utils.logger import logger

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

@router.post("/add", response_model=MarketplaceItem)
async def add_marketplace_item(item: MarketplaceItemCreate):
    """
    Allows a farmer to list a crop for sale.
    """
    try:
        from services.marketplace_service import MarketplaceService
        marketplace_svc = MarketplaceService()
        new_item = marketplace_svc.add_item(item.model_dump())
        logger.info(f"Marketplace item added: {new_item['crop_name']} by {new_item['farmer_name']}")
        return new_item
    except Exception as e:
        logger.error(f"Error adding marketplace item: {str(e)}")
        # If adding fails, we still return a structured error result
        return {
            "error": "Submission Failed: System currently in offline mode.",
            "status": "system_maintenance"
        }

@router.get("/list", response_model=List[MarketplaceItem])
async def list_marketplace_items():
    """
    Allows buyers to browse all products for sale.
    """
    try:
        from services.marketplace_service import MarketplaceService
        marketplace_svc = MarketplaceService()
        return marketplace_svc.list_items()
    except Exception as e:
        logger.error(f"Error listing marketplace items: {str(e)}")
        # Return empty list to prevent UI crash on frontend
        return []
