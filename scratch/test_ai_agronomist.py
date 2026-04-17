import sys
import os
import json
import asyncio

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_agronomist_advice():
    print("Testing AI Agronomist Service...\n")
    
    context = {
        "crop_name": "Tomato",
        "current_stage": "Growth",
        "weather": "Sunny with high humidity",
        "soil": "Sandy Loam",
        "field_size": "2 Hectares"
    }
    
    print(f"Context: {json.dumps(context, indent=4)}")
    
    # Use TestClient to call the endpoint
    response = client.post("/agronomist/advice", json=context)
    
    if response.status_code == 200:
        data = response.json()
        print("\nAI Advice:")
        print("-" * 30)
        print(data["advice"])
        print("\nRecommended Actions:")
        for i, action in enumerate(data["actions"], 1):
            print(f"{i}. {action}")
        print("-" * 30)
        
        # Verify schema
        assert "advice" in data
        assert isinstance(data["actions"], list)
        print("\nTest Passed: Structured AI advice received.")
    else:
        print(f"Test Failed: Status code {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_agronomist_advice()
