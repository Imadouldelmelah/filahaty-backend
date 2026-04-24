from fastapi import APIRouter
import random
from utils.logger import logger

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/fake")
async def get_monitoring_fake():
    """
    Returns dynamic simulated telemetry as requested by the user.
    Simulates real IoT data reliably with specific ranges.
    """
    try:
        # Return exact structure: temperature, humidity, soil_moisture, status
        data = {
            "temperature": random.randint(20, 35),
            "humidity": random.randint(40, 80),
            "soil_moisture": random.randint(30, 70),
            "status": "healthy"
        }
        
        # Log generated data for observability
        logger.info(f"MONITOR_DATA: {data}")
        return data
    except Exception as e:
        logger.error(f"MONITOR_ERROR: {str(e)}")
        # Stable fallback to ensure 200 response
        return {
            "temperature": 25,
            "humidity": 60,
            "soil_moisture": 50,
            "status": "healthy"
        }
