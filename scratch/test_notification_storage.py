import time
from services.alert_service import AlertService

def test_notification_storage():
    alert_svc = AlertService()
    
    # Clear previous notifications for clean test
    alert_svc._notifications.clear()
    
    mock_data = {
        "soil_moisture": 30,  # Should trigger
        "temperature": 25,
        "nitrogen": 50,
        "humidity": 60
    }
    
    # 1. Generate first alert
    print("Generating first alert...")
    alerts = alert_svc.generate_alerts(mock_data)
    assert len(alerts) == 1
    assert len(alert_svc.get_all_notifications()) == 1
    print("First alert stored successfully.")
    
    # 2. Try to generate same alert again (should be duplicate)
    print("\nGenerating same alert again (within 10 mins)...")
    alerts_2 = alert_svc.generate_alerts(mock_data)
    assert len(alerts_2) == 0
    assert len(alert_svc.get_all_notifications()) == 1
    print("Duplicate prevented successfully.")
    
    # 3. Test max limit (50)
    print("\nTesting 50 alert limit...")
    for i in range(60):
        # Using unique messages to avoid deduplication for this test
        dummy_alert = {
            "id": f"dummy_{i}",
            "message": f"Unique message {i}",
            "type": "info",
            "timestamp": (time.time())
        }
        # Directly append to bypass deduplication for capacity test
        alert_svc._notifications.append(dummy_alert)
        
    history = alert_svc.get_all_notifications()
    print(f"History size: {len(history)}")
    assert len(history) == 50
    print("Capacity limit respected.")

if __name__ == "__main__":
    test_notification_storage()
    print("\nNotification storage tests passed!")
