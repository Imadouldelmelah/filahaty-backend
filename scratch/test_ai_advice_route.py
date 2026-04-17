import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ai_advice_route():
    print("Testing /ai/advice route...\n")
    
    context = {
        "crop": "Pepper",
        "stage": "Flowering",
        "weather": "Dry and windy",
        "soil": "Clay"
    }
    
    print(f"Request: {json.dumps(context, indent=4)}")
    
    response = client.post("/ai/advice", json=context)
    
    if response.status_code == 200:
        data = response.json()
        print("\nAI Advice Response:")
        print("-" * 30)
        print(json.dumps(data, indent=4))
        print("-" * 30)
        
        assert "advice" in data
        assert "actions" in data
        print("\nTest Passed: Advanced AI advice received.")
    else:
        print(f"Test Failed: Status code {response.status_code}")
        print(response.content)

if __name__ == "__main__":
    test_ai_advice_route()
