from fastapi import APIRouter
from services.fake_monitoring_service import fake_monitoring_service

router = APIRouter(tags=["IoT Simulation"])

@router.get("/iot/data")
def get_iot_data(field_id: str = "default_field"):
    """
    Returns simulated real-time IoT sensor data from the field.
    Standardized via centralized FakeMonitoringService.
    """
    return fake_monitoring_service.get_field_monitoring_data(field_id)
