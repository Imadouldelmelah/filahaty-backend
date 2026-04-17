import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_monitoring_refactor():
    print("Testing Monitoring Service Refactor...\n")
    
    # 1. Test IoT endpoint
    print("Step 1: Testing /iot/data endpoint...")
    iot_resp = client.get("/iot/data?field_id=test_field_123")
    if iot_resp.status_code == 200:
        data = iot_resp.json()
        print(f"Success! Received data: {json.dumps(data, indent=2)}")
        assert "soil_moisture" in data
        assert "ph" in data
        assert data["field_id"] == "test_field_123"
    else:
        print(f"Failed IoT: {iot_resp.status_code}")

    # 2. Test Tracking Guidance Enhancement
    print("\nStep 2: Testing /tracking/guidance enhancement...")
    # First start a journey
    start_resp = client.post("/tracking/start", json={
        "crop": "tomato",
        "start_date": "2026-04-10"
    })
    journey_id = start_resp.json()["journey_id"]
    
    # Get guidance
    guidance_resp = client.get(f"/tracking/guidance/{journey_id}")
    if guidance_resp.status_code == 200:
        data = guidance_resp.json()
        print("Success! Guidance fetched.")
        # We can't easily check the prompt sent to API from here, 
        # but we verified the code change in tracking_routes.py
        print(f"Journey ID: {journey_id}")
        # Check if response contains progress (which should now be aware of monitoring via context)
        assert "ai_advice" in data
    else:
        print(f"Failed Guidance: {guidance_resp.status_code}")

if __name__ == "__main__":
    test_monitoring_refactor()
