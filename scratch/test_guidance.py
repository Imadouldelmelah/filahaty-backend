import sys
import os
import json
import asyncio
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_guidance_system():
    print("Testing Daily AI Guidance System...\n")
    
    # 1. Start a journey for Tomato (5 days in - Seed stage)
    start_date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    print(f"--- Starting journey for Tomato (start_date: {start_date}) ---")
    response = client.post("/tracking/start", json={
        "crop_name": "tomato",
        "start_date": start_date
    })
    journey_id = response.json()["journey_id"]
    
    # 2. Get AI Guidance
    print(f"\n--- Fetching AI Guidance for Journey: {journey_id} ---")
    response = client.get(f"/tracking/guidance/{journey_id}")
    assert response.status_code == 200
    data = response.json()
    
    print(f"Day: {data['day']}")
    print(f"Stage: {data['stage']}")
    print("-" * 30)
    print(f"AI Guidance: {data['guidance']}")
    print("-" * 30)
    
    # Assertions
    assert data["guidance"].startswith("Today you should")
    assert "irrigation" in data["guidance"].lower() or "water" in data["guidance"].lower()
    assert "tomato" in data["guidance"].lower()

if __name__ == "__main__":
    try:
        test_guidance_system()
        print("\nAll guidance tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
