from fastapi import APIRouter, HTTPException
from models.prediction_models import YieldPredictionRequest
from utils.logger import logger

router = APIRouter(prefix="/field", tags=["Field Analytics"])

@router.get("/decision")
async def get_field_decision(field_id: str):
    """
    Combines tracking, weather, and real-time monitoring data to produce 
    a highly intelligent AI decision for the field.
    """
    try:
        from services.tracking_service import TrackingService
        tracking_svc = TrackingService()
        progress = tracking_svc.get_progress(field_id)
        
        # Determine crop attributes (fallback gracefully if not fully tracked)
        if "error" not in progress:
            crop = progress.get("crop", "Generic Crop")
            stage = progress.get("stage", "Vegetative Growth")
        else:
            logger.warning(f"Field tracking not found for field_id {field_id}. Using defaults.")
            crop = "Generic Crop"
            stage = "Vegetative Growth"

        # Fetch local weather if we have coordinates
        weather_data = {}
        if "error" not in progress and progress.get("latitude") and progress.get("longitude"):
            from services.weather_service import WeatherService
            weather_svc = WeatherService()
            weather_data = weather_svc.get_weather(progress["latitude"], progress["longitude"])
        
        # Always fetch live monitoring data
        from services.fake_monitoring_service import FakeMonitoringService
        monitoring_svc = FakeMonitoringService()
        monitoring_data = monitoring_svc.get_field_monitoring_data(field_id)

        # Build context payload for the Decision Engine
        context = {
            "crop_name": crop,
            "current_stage": stage,
            "weather_data": weather_data,
            "monitoring_data": monitoring_data
        }

        # Generate intelligent decision (Lazy loaded)
        from services.ai_decision_engine import AIDecisionEngine
        decision_engine = AIDecisionEngine()
        decision = await decision_engine.generate_decision(context)
        return decision

    except Exception as e:
        logger.error(f"Error fetching field decision: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to compute field decision.")

@router.post("/predict-yield")
async def predict_field_yield(request: YieldPredictionRequest):
    """
    Predicts crop yield based on field size, crop, monitoring, and weather data.
    """
    try:
        context = {
            "crop_name": request.crop_name,
            "field_size_hectares": request.field_size_hectares,
            "monitoring_data": request.monitoring_data,
            "weather_data": request.weather_data
        }
        
        # Predict yield (Lazy loaded)
        from services.yield_prediction_service import YieldPredictionService
        yield_svc = YieldPredictionService()
        prediction = await yield_svc.predict_yield(context)
        return prediction
        
    except Exception as e:
        logger.error(f"Yield Prediction Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate yield prediction.")

