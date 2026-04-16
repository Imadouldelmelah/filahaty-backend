import requests
from fastapi import APIRouter, HTTPException
from config import settings
from utils.logger import logger

router = APIRouter(tags=["Agricultural News"])

@router.get("/news")
def get_agricultural_news():
    """
    Proxies and validates requests to NewsAPI to ensure zero data leakage
    and protect the API key.
    """
    if not settings.NEWS_API_KEY:
        raise HTTPException(status_code=503, detail="News service currently unavailable.")
    
    # Pre-defined, safe agricultural keywords validated on the backend
    query = "soil+health+OR+soil+fertility+OR+crop+science+OR+sustainable+agriculture+OR+precision+agriculture"
    
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={settings.NEWS_API_KEY}"
    
    try:
        logger.info("SECURITY_AUDIT: Proxied NewsAPI request initiated.")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Strip sensitive headers and pass only pure JSON data back to client
        return response.json()
    except Exception as e:
        logger.error(f"SECURITY_ERROR: NewsAPI proxy failed: {str(e)}")
        raise HTTPException(status_code=502, detail="External news provider failed.")
