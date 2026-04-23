import asyncio
import os
import sys
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

from services.crop_recommendation_service import CropRecommendationService
from services.ai_agronomist import AIAgronomistService

async def test_offline_mode():
    print("Verifying Structured Offline Mode...")
    
    # Force AI failure via invalid key
    os.environ["OPENAI_API_KEY"] = "sk-bad-key"
    
    print("\n--- Testing Crop Idea Fallback ---")
    recommendation_svc = CropRecommendationService()
    context_crop = {"temperature": 35, "humidity": 40, "ph": 6.5}
    rec = await recommendation_svc.generate_recommendation(context_crop)
    print(f"Result: {json.dumps(rec, indent=2)}")
    
    # Assertions for Crop Idea
    assert rec["crop"] == "Corn"
    assert "alternatives" in rec
    assert rec["confidence"] == "medium"
    assert rec["status"] == "offline_optimized"
    print("PASS: Crop recommendation returned structured alternatives.")

    print("\n--- Testing Farming Journey Fallback ---")
    agronomist_svc = AIAgronomistService()
    context_journey = {"crop_name": "Tomato", "current_stage": "Growth"}
    advice = await agronomist_svc.generate_advice(context_journey)
    print(f"Result: {json.dumps(advice, indent=2)}")
    
    # Assertions for Farming Journey
    assert advice["stage"] == "Growth"
    assert "tasks" in advice
    assert "advice" in advice
    assert "alerts" in advice
    assert advice["status"] == "offline_optimized"
    print("PASS: Farming journey returned structured tasks and advice.")

    print("\nALL OFFLINE STRUCTURES VERIFIED.")

if __name__ == "__main__":
    asyncio.run(test_offline_mode())
