from fastapi import APIRouter, HTTPException
from services.tracking_service import tracking_service
from services.weather_service import weather_service
from services.fake_monitoring_service import fake_monitoring_service
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
        progress = tracking_service.get_progress(field_id)
        
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
            weather_data = weather_service.get_weather(progress["latitude"], progress["longitude"])
        
        # Always fetch live monitoring data
        monitoring_data = fake_monitoring_service.get_field_monitoring_data(field_id)

        # Build context payload for the Decision Engine
        context = {
            "crop_name": crop,
            "current_stage": stage,
            "weather_data": weather_data,
            "monitoring_data": monitoring_data
        }

        # Generate intelligent decision (Lazy loaded)
        from services.ai_decision_engine import ai_decision_engine
        decision = await ai_decision_engine.generate_decision(context)
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
        from services.yield_prediction_service import yield_prediction_service
        prediction = await yield_prediction_service.predict_yield(context)
        return prediction
        
    except Exception as e:
        logger.error(f"Yield Prediction Route Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate yield prediction.")

