import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_unification():
    print("Testing Monitoring Unification System...\n")
    
    # 1. Test Unified Auto-Prediction
    print("Step 1: Testing Unified Auto-Prediction...")
    auto_p_resp = client.get("/predict/auto?lat=35.19&lon=-0.63")
    if auto_p_resp.status_code == 200:
        data = auto_p_resp.json()
        print(f"Success! Auto-Prediction: {data['crop']} ({data['confidence']}%)")
        assert "crop" in data
    else:
        print(f"Failed Auto-Predict: {auto_p_resp.status_code}")

    # 2. Test Soil-Aware Alerts
    print("\nStep 2: Testing Soil-Aware Smart Alerts...")
    # This endpoint pulls monitoring data internally via the unified service
    alerts_resp = client.get("/weather/alerts?lat=35.19&lon=-0.63&crop=tomato&stage=growth")
    if alerts_resp.status_code == 200:
        alerts = alerts_resp.json()["alerts"]
        print(f"Success! Received {len(alerts)} alerts.")
        # Check for soil-specific alert types we added (waterlogging_risk or ph_mismatch)
        soil_related = [a for a in alerts if a["type"] in ["waterlogging_risk", "ph_mismatch"]]
        if soil_related:
            print(f"Detected Soil-Aware Alerts: {json.dumps(soil_related, indent=2)}")
        else:
            print("No soil-aware alerts triggered (randomized sensors were within range).")
    else:
        print(f"Failed Alerts: {alerts_resp.status_code}")

if __name__ == "__main__":
    test_unification()
