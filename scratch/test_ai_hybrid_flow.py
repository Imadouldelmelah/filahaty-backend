import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crop_recommendation_service import CropRecommendationService
from services.ai_agronomist import AIAgronomistService

async def test_hybrid_enhancement_flow():
    print("Testing AI-as-Enhancement Hybrid Flow...")
    
    # 1. Test Crop Recommendation Enhancement
    print("\n1. Testing Crop Recommendation...")
    crop_svc = CropRecommendationService()
    
    # CASE A: AI Success (Refinement)
    crop_svc._ai.generate = AsyncMock(return_value='{"crop": "Tomato", "reason": "AI refined reason", "alternatives": ["Pepper", "Cucumber"]}')
    context = {"temperature": 25, "humidity": 60, "ph": 6.5}
    result = await crop_svc.generate_recommendation(context)
    print(f"AI Success Result: {result['crop']} | Status: {result['status']} | Reason: {result['reason'][:50]}...")
    assert result["status"] == "ai_optimized"
    assert "AI refined reason" in result["reason"]
    
    # CASE B: AI Failure (Baseline)
    crop_svc._ai.generate = AsyncMock(side_effect=Exception("Credits exhausted"))
    result = await crop_svc.generate_recommendation(context)
    print(f"AI Failure Result: {result['crop']} | Status: {result['status']} | Message: {result.get('message')}")
    assert result["status"] == "offline_optimized"
    assert result["message"] == "Smart offline mode activated"

    # 2. Test Advice Generation Enhancement
    print("\n2. Testing Advice Generation...")
    advice_svc = AIAgronomistService()
    
    # CASE A: AI Success
    advice_svc._ai.generate = AsyncMock(return_value='{"stage": "Growth", "tasks": ["Refined task"], "advice": "AI refined advice", "alerts": []}')
    context = {"crop_name": "Tomato", "current_stage": "Growth"}
    result = await advice_svc.generate_advice(context)
    print(f"AI Success Result: {result['stage']} | Status: {result['status']} | Advice: {result['advice']}")
    assert result["status"] == "ai_optimized"
    assert "AI refined advice" in result["advice"]
    
    # CASE B: AI Failure
    advice_svc._ai.generate = AsyncMock(side_effect=Exception("Timeout"))
    result = await advice_svc.generate_advice(context)
    print(f"AI Failure Result: {result['stage']} | Status: {result['status']} | Message: {result.get('message')}")
    assert result["status"] == "offline_optimized"
    assert result["message"] == "Smart offline mode activated"

    print("\nPASS: All hybrid enhancement flows verified successfully.")

if __name__ == "__main__":
    asyncio.run(test_hybrid_enhancement_flow())
