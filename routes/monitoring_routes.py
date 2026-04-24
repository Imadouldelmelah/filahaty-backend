from fastapi import APIRouter
import random
from utils.logger import logger

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/fake")
async def get_monitoring_fake():
    """
    Unified entry point for simulated telemetry.
    Consumes the centralized FakeMonitoringService for consistent data flow.
    """
    try:
        from services.fake_monitoring_service import FakeMonitoringService
        mon_svc = FakeMonitoringService()
        return mon_svc.get_fake_monitoring_data()
    except Exception as e:
        logger.error(f"MONITOR_ROUTE_ERROR: {str(e)}")
        # Ultimate indestructible baseline
        return {
            "temperature": 25,
            "humidity": 60,
            "soil_moisture": 50,
            "soil_ph": 6.5,
            "nitrogen": 30,
            "phosphorus": 25,
            "potassium": 25,
            "rainfall": 2.0,
            "health_score": 85,
            "health_status": "Stable (Backup)",
            "status": "emergency_sync"
        }

@router.get("/health")
async def get_field_health(field_id: str = "default_field"):
    """
    Dedicated health endpoint for the unified agricultural engine.
    Returns the same consistent data as /fake but framed for analytics.
    """
    try:
        from services.fake_monitoring_service import FakeMonitoringService
        mon_svc = FakeMonitoringService()
        return mon_svc.get_fake_monitoring_data(field_id)
    except Exception as e:
        logger.error(f"HEALTH_ROUTE_ERROR: {str(e)}")
        return {"status": "syncing", "health_score": 50, "health_status": "Calculating"}

@router.get("/notifications")
async def get_notifications():
    """
    Returns the history of agricultural alerts stored in the system.
    """
    try:
        from services.alert_service import AlertService
        alert_svc = AlertService()
        return alert_svc.get_all_notifications()
    except Exception as e:
        logger.error(f"NOTIFICATION_ROUTE_ERROR: {str(e)}")
        return []
