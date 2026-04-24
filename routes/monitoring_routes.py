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
        # Return full agricultural dataset requested
        data = {
            "temperature": random.randint(20, 35),
            "humidity": random.randint(40, 80),
            "soil_moisture": random.randint(30, 70),
            "soil_ph": round(random.uniform(5.5, 7.5), 1),
            "nitrogen": random.randint(10, 50),
            "phosphorus": random.randint(10, 40),
            "potassium": random.randint(10, 40),
            "rainfall": random.randint(0, 10),
            "status": "healthy"
        }
        
        # Log generated data for observability
        logger.info(f"MONITOR_DATA_FULL: {data}")
        return data
    except Exception as e:
        logger.error(f"MONITOR_ERROR: {str(e)}")
        # Stable full-schema fallback to ensure 200 response with no missing values
        return {
            "temperature": 25,
            "humidity": 60,
            "soil_moisture": 50,
            "soil_ph": 6.5,
            "nitrogen": 30,
            "phosphorus": 25,
            "potassium": 25,
            "rainfall": 2,
            "status": "system_fallback"
        }
