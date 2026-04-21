import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.crop_recommendation_service import CropRecommendationService

async def test_crop_fallback():
    print("Testing Agronomy-Based Fallback System...")
    service = CropRecommendationService()
    
    # 1. Force AI failure
    service._ai.generate = AsyncMock(side_effect=Exception("AI connection failed"))
    
    # Test cases
    test_data = [
        {"temperature": 35, "humidity": 50, "ph": 7.0, "expected": "Corn"},
        {"temperature": 25, "humidity": 85, "ph": 7.0, "expected": "Rice"},
        {"temperature": 25, "humidity": 50, "ph": 5.5, "expected": "Potato"},
        {"temperature": 25, "humidity": 50, "ph": 7.0, "expected": "Wheat"}
    ]
    
    for context in test_data:
        print(f"\nEvaluating: {context}")
        result = await service.generate_recommendation(context)
        print(f"Result: {result['crop']} | Status: {result['status']}")
        assert result["crop"] == context["expected"]
        assert result["status"] == "rule_engine_fallback"
        print(f"PASS: Correctly recommended {result['crop']}")

if __name__ == "__main__":
    asyncio.run(test_crop_fallback())
