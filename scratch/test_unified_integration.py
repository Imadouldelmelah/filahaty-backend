import requests
import json

def test_unified_system():
    # Since we can't easily run the server, we'll verify integration by calling services directly
    from services.fake_monitoring_service import FakeMonitoringService
    from services.crop_recommender import CropRecommenderService
    from services.agronomy_engine import get_smart_journey_logic, get_static_journey_data
    from services.calendar_service import CalendarService
    
    # 1. GENERATE MONITORING DATA
    mon_svc = FakeMonitoringService()
    monitoring = mon_svc.get_fake_monitoring_data("test_field")
    print(f"UNIFIED MONITORING: {json.dumps(monitoring, indent=2)}")
    
    # 2. FEED TO RECOMENDER
    rec_svc = CropRecommenderService()
    rec = rec_svc.get_recommendations(monitoring)
    print(f"CROP SUGGESTION (from monitoring): {json.dumps(rec, indent=2)}")
    
    # 3. FEED TO JOURNEY
    base_journey = get_static_journey_data(15) # Day 15 (Growth)
    smart_journey = get_smart_journey_logic(base_journey, monitoring)
    print(f"SMART JOURNEY (from monitoring): {json.dumps(smart_journey, indent=2)}")
    
    # 4. FEED TO CALENDAR
    cal_svc = CalendarService()
    calendar = cal_svc.generate_30_day_projection("Tomato", 15, monitoring)
    print(f"CALENDAR (from monitoring): Day 1 Task -> {calendar[0]['task']}")

if __name__ == "__main__":
    test_unified_system()
