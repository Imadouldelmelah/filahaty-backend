import random

class FakeMonitoringService:
    """
    Simulates real-time IoT sensor data for fields and crops.
    Providing a single source of truth for monitoring data across the platform.
    """
    
    def get_field_monitoring_data(self, field_id: str = "default"):
        """
        Returns randomized but realistically bound set of monitoring data.
        
        Args:
            field_id (str): ID of the field to monitor.
            
        Returns:
            dict: {temperature, humidity, soil_moisture, ph, N, P, K, rainfall}
        """
        data = {
            "field_id": field_id,
            "temperature": round(random.uniform(18.0, 38.0), 1),
            "humidity": round(random.uniform(45.0, 92.0), 1),
            "soil_moisture": round(random.uniform(25.0, 75.0), 1),
            "ph": round(random.uniform(5.8, 7.2), 1),
            "N": random.randint(40, 95),
            "P": random.randint(25, 55),
            "K": random.randint(20, 45),
            "rainfall": round(random.uniform(0.0, 150.0), 1)
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
            logger.error(f"Health score calculation failed in FakeMonitoringService: {str(e)}")
            data["health_score"] = 85
            data["health_status"] = "Healthy"
        
        return data

# Class exported for on-demand initialization
