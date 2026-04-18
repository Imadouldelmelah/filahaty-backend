import asyncio
from utils.logger import logger

class UnifiedAIBrain:
    def __init__(self):
        pass

    async def get_unified_intelligence(self, field_id: str) -> dict:
        """
        Coordinates all intelligent services to provide a single, 
        comprehensive view of the field's health, decisions, and future outcomes.
        """
        try:
            logger.info(f"UNIFIED_BRAIN: Initiating central intelligence synthesis for {field_id}")
            
            # Local instantiations for lazy loading
            from services.tracking_service import TrackingService
            from services.fake_monitoring_service import FakeMonitoringService
            from services.weather_service import WeatherService
            from services.health_score_service import FieldHealthScoreService
            from services.ai_decision_engine import AIDecisionEngine
            from services.ai_agronomist import AIAgronomistService
            from services.yield_prediction_service import YieldPredictionService
            
            tracking_svc = TrackingService()
            monitoring_svc = FakeMonitoringService()
            weather_svc = WeatherService()
            health_svc = FieldHealthScoreService()
            decision_engine = AIDecisionEngine()
            agronomist_svc = AIAgronomistService()
            yield_svc = YieldPredictionService()

            # 1. Fetch Contextual Data
            progress = tracking_svc.get_progress(field_id)
            monitoring_data = monitoring_svc.get_field_monitoring_data(field_id)
            
            crop = progress.get("crop", "Generic Crop")
            stage = progress.get("stage", "Vegetative Growth")
            lat = progress.get("latitude")
            lon = progress.get("longitude")
            
            weather_data = {}
            if lat and lon:
                weather_data = weather_svc.get_weather(lat, lon)
            
            # 2. Run Deterministic Health Assessment
            health_report = health_svc.calculate_health_score(monitoring_data, stage)
            
            # 3. Synchronize AI Analysis (Run concurrently for performance)
            context = {
                "crop_name": crop,
                "current_stage": stage,
                "weather_data": weather_data,
                "monitoring_data": monitoring_data,
                "field_size_hectares": 1.0, # Default if not tracked
                "soil": "Not specified"
            }
            
            # Concurrent execution of heavy AI tasks
            decision_task = decision_engine.generate_decision(context)
            advice_task = agronomist_svc.generate_advice(context)
            yield_task = yield_svc.predict_yield(context)
            
            decision, advice, yield_prediction = await asyncio.gather(
                decision_task, advice_task, yield_task
            )
            
            # 4. Synthesize Unified Intelligence Package
            unified_report = {
                "field_id": field_id,
                "timestamp": progress.get("start_date", ""),
                "state": {
                    "crop": crop,
                    "stage": stage,
                    "day": progress.get("day", 1)
                },
                "health": health_report,
                "yield_projection": yield_prediction,
                "decision": decision,
                "advice": advice,
                "context": {
                    "weather": weather_data,
                    "sensors": monitoring_data
                }
            }
            
            logger.info(f"UNIFIED_BRAIN: Intelligence synthesis complete for {field_id}")
            return unified_report

        except Exception as e:
            logger.error(f"UNIFIED_BRAIN_ERROR: Synthesis failed: {str(e)}")
            return {
                "error": "Central intelligence core is temporarily overloaded.",
                "status": "partial_data"
            }
# Export the class for lazy instantiation inside routes
