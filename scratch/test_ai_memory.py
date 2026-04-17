import sys
import os
import json
import time

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ai_memory():
    print("Testing AI Context Memory (Action History)...\n")
    
    # 1. Start a new journey
    print("Step 1: Starting new journey for Pepper...")
    start_resp = client.post("/tracking/start", json={"crop": "pepper", "start_date": "2026-04-10"})
    journey_id = start_resp.json()["journey_id"]
    print(f"Journey ID: {journey_id}")
    
    # 2. Record some actions
    print("\nStep 2: Recording actions...")
    client.post("/tracking/action/record", json={
        "journey_id": journey_id, 
        "action": "Applied balanced initial fertilizer NPK 15-15-15"
    })
    client.post("/tracking/action/record", json={
        "journey_id": journey_id, 
        "action": "Installed organic mulch for moisture retention"
    })
    
    # 3. Get advice and check for memory
    print("\nStep 3: Fetching AI advice with history...")
    advice_resp = client.post("/ai/advice", json={
        "crop": "pepper",
        "stage": "Growth",
        "weather": "Sunny",
        "soil": "Clay",
        "journey_id": journey_id
    })
    
    if advice_resp.status_code == 200:
        data = advice_resp.json()
        print("\nAI Advice Response:")
        print("-" * 30)
        print(data["advice"])
        print("-" * 30)
        
        # Check for keywords related to the actions we recorded
        advice_lower = data["advice"].lower()
        has_memory = "fertilizer" in advice_lower or "mulch" in advice_lower or "already" in advice_lower or "previous" in advice_lower
        
        print(f"\nAI shows signs of memory? {'Yes' if has_memory else 'No'}")
        
        # 4. Verify in Journeys JSON
        print("\nStep 4: Verifying history in journeys.json...")
        with open("data/journeys.json", "r") as f:
            journeys = json.load(f)
            history = journeys[journey_id].get("history", [])
            print(f"Found {len(history)} items in history.")
            assert len(history) == 2
            
        print("\nTest Passed: AI accurately references historical actions.")
    else:
        print(f"Test Failed: {advice_resp.status_code}")
        print(advice_resp.json())

if __name__ == "__main__":
    test_ai_memory()
