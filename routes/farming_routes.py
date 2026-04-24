from fastapi import APIRouter, Query
from services.calendar_service import CalendarService
from services.fake_monitoring_service import FakeMonitoringService
import random

router = APIRouter(prefix="", tags=["Farming Operations"])

@router.get("/calendar")
async def get_general_farming_calendar(
    crop: str = Query("Tomato", description="Crop type for calendar generation"),
    day: int = Query(1, description="Current day in lifecycle")
):
    """
    Generates a 30-day dynamic farming calendar.
    Parameters are determined by lifecycle day and real-time monitoring.
    """
    calendar_svc = CalendarService()
    monitoring_svc = FakeMonitoringService()
    
    # 1. Fetch real-time context
    monitoring_data = monitoring_svc.get_fake_monitoring_data()
    
    # 2. Generate Projection (guaranteed 30 days of date, task, priority)
    projection = calendar_svc.generate_30_day_projection(
        crop_name=crop,
        current_day=day,
        monitoring_data=monitoring_data
    )
    
    # 3. Final formatting and safety assurance
    formatted_calendar = []
    for item in projection:
        formatted_calendar.append({
            "date": item["date"],
            "task": item["task"],
            "priority": item.get("priority", "medium")
        })
        
    return formatted_calendar
