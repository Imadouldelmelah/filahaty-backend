from fastapi import APIRouter

router = APIRouter(tags=["IoT Simulation"])

@router.get("/iot/data")
def get_iot_data(field_id: str = "default_field"):
    """
    Returns simulated real-time IoT sensor data from the field.
    Standardized via centralized FakeMonitoringService.
    """
    from services.fake_monitoring_service import FakeMonitoringService
    monitoring_svc = FakeMonitoringService()
    return monitoring_svc.get_field_monitoring_data(field_id)
