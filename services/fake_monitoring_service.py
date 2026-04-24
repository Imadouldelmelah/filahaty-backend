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
        Ensures consistency between endpoints using a time-seeded randomizer.
        """
        try:
            import time
            from utils.logger import logger
            
            # Use field_id and current minute as seed for 60s consistency across all systems
            seed_val = hash(field_id) + (int(time.time()) // 60)
            rng = random.Random(seed_val)
            
            data = {
                "field_id": field_id,
                "temperature": rng.randint(20, 35),
                "humidity": rng.randint(40, 80),
                "soil_moisture": rng.randint(30, 70),
                "soil_ph": round(rng.uniform(5.5, 7.5), 1),
                "nitrogen": rng.randint(10, 50),
                "phosphorus": rng.randint(10, 40),
                "potassium": rng.randint(10, 40),
                "rainfall": round(rng.uniform(0.0, 10.0), 1)
            }
            
            # Calculate derived health score (Indestructible integration)
            try:
                from services.health_score_service import FieldHealthScoreService
                health_svc = FieldHealthScoreService()
                health_assessment = health_svc.calculate_health_score(data)
                data["health_score"] = health_assessment["health_score"]
                data["health_status"] = health_assessment["status"]
            except Exception as e:
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
