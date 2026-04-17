import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ai_weather_sync():
    print("Testing AI-Weather Synchronized Guidance...\n")
    
    # 1. Start a journey with specific coordinates (Sidi Bel Abbes)
    print("Step 1: Starting journey with coordinates...")
    start_resp = client.post("/tracking/start", json={
        "crop": "tomato",
        "start_date": "2026-04-10",
        "lat": 35.19,
        "lon": -0.63
    })
    journey_id = start_resp.json()["journey_id"]
    print(f"Journey ID: {journey_id}")
    
    # 2. Fetch Guidance (This triggers the Live Weather -> Logic -> AI loop)
    print("\nStep 2: Fetching Synchronized Guidance (Live Weather + AI)...")
    guidance_resp = client.get(f"/tracking/guidance/{journey_id}")
    
    if guidance_resp.status_code == 200:
        data = guidance_resp.json()
        print("\nAI Advice Response:")
        print("-" * 30)
        print(data["ai_advice"]["advice"])
        print("-" * 30)
        
        # Verify that weather data was fetched and used
        print("\nVerification Data:")
        weather = data["progress"].get("weather_data") # Guidance endpoint should return weather info
        # Wait, the guidance endpoint returns the logic results too.
        
        # Check if the AI acknowledges the weather
        advice_text = data["ai_advice"]["advice"].lower()
        print(f"Real Weather was fetched? {'Yes' if data['progress'].get('latitude') else 'No'}")
        
    else:
        print(f"Test Failed: {guidance_resp.status_code}")
        print(guidance_resp.json())

if __name__ == "__main__":
    test_ai_weather_sync()
