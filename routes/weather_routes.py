from fastapi import APIRouter, HTTPException, Query
from services.weather_service import weather_service
from services.weather_intelligence import weather_intelligence
from services.fake_monitoring_service import fake_monitoring_service
from utils.logger import logger

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
async def get_weather_endpoint(
    lat: float = Query(..., description="Latitude of the location"),
    lon: float = Query(..., description="Longitude of the location")
):
    """
    Exposes real-time weather data for a specific location.
    """
    try:
        weather_data = weather_service.get_weather(lat, lon)
        
        # Check if we got valid data
        if weather_data["temperature"] is None:
            raise HTTPException(status_code=503, detail="Weather service currently unavailable")
            
        return weather_data
    except Exception as e:
        logger.error(f"Weather Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching weather")

@router.get("/insights")
async def get_weather_insights_endpoint(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Returns weather data combined with agricultural decision logic.
    """
    try:
        weather_data = weather_service.get_weather(lat, lon)
        if weather_data["temperature"] is None:
            raise HTTPException(status_code=503, detail="Weather service unavailable")
            
        monitoring_data = fake_monitoring_service.get_field_monitoring_data()
        insights = weather_intelligence.analyze_weather(weather_data, monitoring_data)
        
        return {
            "weather": weather_data,
            "insights": insights
        }
    except Exception as e:
        logger.error(f"Weather Insights Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/alerts")
async def get_weather_alerts_endpoint(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    crop: str = Query("", description="Crop name"),
    stage: str = Query("", description="Growth stage")
):
    """
    Returns specific, crop-aware farming alerts based on weather and stage.
    """
    try:
        weather_data = weather_service.get_weather(lat, lon)
        if weather_data["temperature"] is None:
            raise HTTPException(status_code=503, detail="Weather service unavailable")
            
        monitoring_data = fake_monitoring_service.get_field_monitoring_data()
        alerts = weather_intelligence.generate_smart_alerts(weather_data, crop, stage, monitoring_data)
        return {"alerts": alerts}
    except Exception as e:
        logger.error(f"Weather Alerts Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
