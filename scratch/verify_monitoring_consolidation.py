from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from main import app

client = TestClient(app)

def test_consolidation():
    print("--- VERIFYING MONITORING CONSOLIDATION ---")

    # 1. Verify /iot/data removal (Should be 404)
    print("\nPhase 1: Verifying /iot/data removal...")
    resp = client.get("/iot/data")
    print(f"GET /iot/data status: {resp.status_code}")
    assert resp.status_code == 404, "Endpoint /iot/data should have been removed"

    # 2. Verify Advanced Chat Internal Fetch
    print("\nPhase 2: Verifying Advanced Chat internal fetch...")
    chat_payload = {
        "message": "What is my soil moisture?",
        "field_id": "test_field_consolidation"
    }
    resp = client.post("/ai/chat-advanced", json=chat_payload)
    print(f"POST /ai/chat-advanced status: {resp.status_code}")
    assert resp.status_code == 200
    # We can't easily check the response content without real AI, 
    # but the success indicates the internal fetch didn't crash.

    # 3. Verify Agronomist Advice Internal Fetch
    print("\nPhase 3: Verifying Agronomist Advice internal fetch...")
    advice_payload = {
        "crop_name": "Tomato",
        "current_stage": "Flowering",
        "weather": "Sunny",
        "soil": "Clay",
        "field_size": "2 hectares",
        "field_id": "test_field_advice"
    }
    resp = client.post("/agronomist/advice", json=advice_payload)
    print(f"POST /agronomist/advice status: {resp.status_code}")
    assert resp.status_code == 200

    # 4. Verify Yield Prediction Internal Fetch
    print("\nPhase 4: Verifying Yield Prediction internal fetch...")
    yield_payload = {
        "crop_name": "Wheat",
        "field_size_hectares": 5.0,
        "field_id": "test_field_yield"
    }
    resp = client.post("/field/predict-yield", json=yield_payload)
    print(f"POST /field/predict-yield status: {resp.status_code}")
    assert resp.status_code == 200

    print("\n--- ALL CONSOLIDATION CHECKS PASSED ---")

if __name__ == "__main__":
    try:
        test_consolidation()
    except Exception as e:
        print(f"TEST FAILED: {str(e)}")
        sys.exit(1)
