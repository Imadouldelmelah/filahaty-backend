import asyncio
import sys
import os
import json
from unittest.mock import AsyncMock, patch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crop_recommendation_service import CropRecommendationService
from services.ai_agronomist import AIAgronomistService
from services.disease_detector import DiseaseDetectionService
from services.yield_prediction_service import YieldPredictionService
from services.ai_decision_engine import AIDecisionEngine

async def verify_global_json_safety():
    print("Initiating Global AI JSON Safety Verification...")
    
    # 1. Setup Mock for Catastrophic AI Failure
    # We mock generate and generate_vision to return garbage/error strings
    mock_ai = AsyncMock(side_effect=Exception("API CREDITS EXHAUSTED / TIMEOUT"))
    
    services = [
        ("Crop Recommendation", CropRecommendationService(), {"temperature": 35}),
        ("Farming Advice", AIAgronomistService(), {"crop_name": "Tomato", "current_stage": "Growth"}),
        ("Disease Detection", DiseaseDetectionService(), {}), # base64 and mime added in call
        ("Yield Prediction", YieldPredictionService(), {"crop_name": "Wheat", "field_size_hectares": 2.0}),
        ("Central Decision", AIDecisionEngine(), {"crop_name": "Potato"})
    ]
    
    all_passed = True
    
    for name, svc, context in services:
        print(f"\nTesting Service: {name}")
        # Patch the _ai.generate and _ai.generate_vision of each service
        svc._ai.generate = mock_ai
        svc._ai.generate_vision = mock_ai
        
        try:
            # Special handling for vision
            if name == "Disease Detection":
                result = await svc.analyze_crop_image("dummy_base64")
            else:
                result = await svc.predict_yield(context) if name == "Yield Prediction" else \
                         await svc.generate_recommendation(context) if name == "Crop Recommendation" else \
                         await svc.generate_advice(context) if name == "Farming Advice" else \
                         await svc.generate_decision(context)
            
            # 1. Check if result is a valid JSON (dict in Python)
            if not isinstance(result, dict):
                print(f"FAILED: {name} did not return a dictionary.")
                all_passed = False
                continue
            
            # 2. Check for offline status
            if result.get("status") != "offline_optimized":
                print(f"FAILED: {name} did not return 'offline_optimized' status on AI failure.")
                all_passed = False
            
            # 3. Check for notification message
            if result.get("message") != "Smart offline mode activated":
                print(f"FAILED: {name} missing 'Smart offline mode activated' message.")
                all_passed = False
                
            print(f"PASS: {name} safely recovered with offline logic.")
            print(f"Data: {json.dumps(result, indent=2)[:100]}...")
            
        except Exception as e:
            print(f"CRITICAL FAILURE: {name} crashed with error: {str(e)}")
            all_passed = False

    if all_passed:
        print("\nSUCCESS: Global AI JSON Safety Verified. Zero parsing errors detected.")
    else:
        print("\nFAILURE: Some services are still vulnerable to JSON parsing errors.")

if __name__ == "__main__":
    asyncio.run(verify_global_json_safety())
