from fastapi import APIRouter
from services.fake_monitoring_service import FakeMonitoringService
from utils.logger import logger

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/fake")
async def get_monitoring_fake():
    """
    Returns dynamic simulated telemetry as requested by the user.
    Simulates real-time IoT sensors. Guaranteed 'Always Available'.
    """
    try:
        monitoring_svc = FakeMonitoringService()
        data = monitoring_svc.get_fake_monitoring_data()
        
        # Audit log for generated data
        logger.info(f"FAKE_MONITORING: Generated data: {data}")
        print(f"FAKE_MONITORING: Generated data: {data}")
        
        return data
    except Exception as e:
        logger.error(f"ROUTE_MONITORING_FAILURE: {str(e)}")
        # Ultimate fallback to ensure JSON is always returned
        return {
            "soil_moisture": 65,
            "temperature": 25,
            "humidity": 70,
            "ph": 6.5,
            "status": "system_fallback"
        }
