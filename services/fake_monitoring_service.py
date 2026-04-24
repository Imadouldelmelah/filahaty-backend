import random

class FakeMonitoringService:
    """
    Simulates real-time IoT sensor data for fields and crops.
    Providing a single source of truth for monitoring data across the platform.
    Now standardized to use long-form sensor names (nitrogen, phosphorus, potassium).
    """
    
    def get_fake_monitoring_data(self, field_id: str = "default_field"):
        """
        Returns dynamic simulated telemetry data with a unified schema.
        This is the single source of truth for IoT data across the platform.
        Wrapped in a global try-except to ensure 'Always Available' status.
        """
        try:
            data = {
                "field_id": field_id,
                "soil_moisture": random.randint(20, 80), # Allows for < 35 triggers
                "temperature": random.randint(15, 40),   # Allows for > 32 triggers
                "humidity": random.randint(30, 90),
                "soil_ph": round(random.uniform(5.5, 7.5), 1),
                "nitrogen": random.randint(0, 140),
                "phosphorus": random.randint(0, 120),
                "potassium": random.randint(0, 120),
                "rainfall": round(random.uniform(0.0, 400.0), 1)
            }
            
            # Calculate derived health score (Indestructible integration)
            try:
                from services.health_score_service import FieldHealthScoreService
                health_svc = FieldHealthScoreService()
                health_assessment = health_svc.calculate_health_score(data)
                data["health_score"] = health_assessment["score"]
                data["health_status"] = health_assessment["status"]
            except Exception as e:
                from utils.logger import logger
                logger.error(f"Health score calculation failed: {str(e)}")
                data["health_score"] = 85
                data["health_status"] = "Healthy"
            
            return data
            
        except Exception as e:
            from utils.logger import logger
            logger.error(f"CRITICAL_MONITORING_FAILURE: {str(e)}")
            # Guaranteed stable fallback
            return {
                "field_id": field_id,
                "soil_moisture": 65,
                "temperature": 25,
                "humidity": 70,
                "soil_ph": 6.5,
                "nitrogen": 40,
                "phosphorus": 35,
                "potassium": 35,
                "rainfall": 50.0,
                "health_score": 80,
                "health_status": "Stable",
                "status": "fallback"
            }

# Class exported for on-demand initialization
