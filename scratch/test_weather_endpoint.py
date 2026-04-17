from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_weather_endpoint():
    print("Testing GET /weather endpoint...")
    lat, lon = 35.19, -0.63
    
    response = client.get(f"/weather/?lat={lat}&lon={lon}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response Content:")
        print(data)
        
        # Validation
        keys = ["temperature", "humidity", "rain", "wind"]
        if all(k in data for k in keys):
            print("\nTest Passed: Endpoint returned all expected weather fields.")
        else:
            print("\nTest Failed: Missing fields in response.")
    else:
        print(f"Test Failed: {response.text}")

if __name__ == "__main__":
    test_weather_endpoint()
