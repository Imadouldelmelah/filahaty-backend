import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_get_agronomy_plan():
    print("Testing /agronomy/plan endpoint...\n")
    
    # Test valid crop
    print("--- Testing Valid Crop: tomato ---")
    response = client.post("/agronomy/plan", json={"crop": "tomato"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=4)}")
    assert response.status_code == 200
    
    # Test valid crop (case insensitive)
    print("\n--- Testing Valid Crop (Case Insensitive): Pepper ---")
    response = client.post("/agronomy/plan", json={"crop": "Pepper"})
    print(f"Status: {response.status_code}")
    assert response.status_code == 200
    
    # Test unknown crop
    print("\n--- Testing Unknown Crop: cucumber ---")
    response = client.post("/agronomy/plan", json={"crop": "cucumber"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=4)}")
    assert response.status_code == 404
    
    # Test invalid payload
    print("\n--- Testing Invalid Payload ---")
    response = client.post("/agronomy/plan", json={"not_a_crop": "tomato"})
    print(f"Status: {response.status_code}")
    assert response.status_code == 422 # FastAPI validation error

if __name__ == "__main__":
    try:
        test_get_agronomy_plan()
        print("\nAll API tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
