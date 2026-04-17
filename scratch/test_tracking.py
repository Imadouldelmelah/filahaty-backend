import sys
import os
import json
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_tracking_system():
    print("Testing Crop Progress Tracking System...\n")
    
    # 1. Start a journey with a start date 5 days ago
    start_date_5_days_ago = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    print(f"--- Starting journey for Tomato (start_date: {start_date_5_days_ago}) ---")
    response = client.post("/tracking/start", json={
        "crop_name": "tomato",
        "start_date": start_date_5_days_ago
    })
    assert response.status_code == 200
    journey_id = response.json()["journey_id"]
    print(f"Journey started: {journey_id}")
    
    # 2. Check progress (should be day 5, stage: Seed)
    # tomato Seed stage: 1-14 days
    print("\n--- Checking progress for day 5 journey ---")
    response = client.get(f"/tracking/progress/{journey_id}")
    progress = response.json()
    print(json.dumps(progress, indent=4))
    assert progress["day"] == 5
    assert progress["stage"] == "Seed"
    
    # 3. Start a journey for Pepper 20 days ago (Growth stage)
    # pepper Seed: 1-10, Growth: 11-50
    start_date_20_days_ago = (datetime.now() - timedelta(days=19)).strftime("%Y-%m-%d")
    print(f"\n--- Starting journey for Pepper (start_date: {start_date_20_days_ago}) ---")
    response = client.post("/tracking/start", json={
        "crop_name": "pepper",
        "start_date": start_date_20_days_ago
    })
    journey_id_pepper = response.json()["journey_id"]
    
    print("\n--- Checking progress for day 20 journey ---")
    response = client.get(f"/tracking/progress/{journey_id_pepper}")
    progress_pepper = response.json()
    print(json.dumps(progress_pepper, indent=4))
    assert progress_pepper["day"] == 20
    assert progress_pepper["stage"] == "Growth"

    # 4. Test error handling
    print("\n--- Testing error: Non-existent journey ---")
    response = client.get("/tracking/progress/some-fake-id")
    print(f"Status: {response.status_code}, Detail: {response.json()['detail']}")
    assert response.status_code == 404

if __name__ == "__main__":
    try:
        test_tracking_system()
        print("\nAll tracking tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
