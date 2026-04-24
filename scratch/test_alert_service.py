from services.alert_service import AlertService

def test_alert_generation():
    alert_svc = AlertService()
    
    # Test case: Low soil moisture and high temperature
    mock_data = {
        "soil_moisture": 30,
        "temperature": 35,
        "nitrogen": 50,
        "humidity": 60
    }
    
    alerts = alert_svc.generate_alerts(mock_data)
    print(f"Generated {len(alerts)} alerts")
    for alert in alerts:
        print(f"[{alert['type'].upper()}] {alert['message']} (ID: {alert['id'][:8]})")
        
    assert len(alerts) == 2
    assert any(a['type'] == 'critical' for a in alerts)
    assert any("Irrigation needed" in a['message'] for a in alerts)
    
    # Test case: Low nitrogen and high humidity
    mock_data_2 = {
        "soil_moisture": 50,
        "temperature": 25,
        "nitrogen": 15,
        "humidity": 80
    }
    
    alerts_2 = alert_svc.generate_alerts(mock_data_2)
    print(f"\nGenerated {len(alerts_2)} alerts")
    for alert in alerts_2:
        print(f"[{alert['type'].upper()}] {alert['message']} (ID: {alert['id'][:8]})")
        
    assert len(alerts_2) == 2
    assert all(a['type'] == 'warning' for a in alerts_2)

if __name__ == "__main__":
    test_alert_generation()
    print("\nAll tests passed!")
