import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.crop_recommendation_service import CropRecommendationService

class MockGeminiService:
    def __init__(self, mock_response):
        self.mock_response = mock_response
    async def generate(self, prompt):
        return self.mock_response

async def test_scenarios():
    print("--- TESTING CROP RECOMMENDATION HARDENING ---")
    
    # Scenario 1: Valid JSON
    print("\nScenario 1: Valid JSON")
    svc = CropRecommendationService()
    svc._ai = MockGeminiService('{"crop": "Tomato", "confidence": "High", "reason": "Perfect pH and humidity."}')
    res = await svc.generate_recommendation({})
    print(f"Result: {res}")
    assert res['crop'] == "Tomato"

    # Scenario 2: Markdown Wrapped JSON
    print("\nScenario 2: Markdown Wrapped JSON")
    svc._ai = MockGeminiService('```json\n{"crop": "Potato", "confidence": "Medium", "reason": "Wait for rain."}\n```')
    res = await svc.generate_recommendation({})
    print(f"Result: {res}")
    assert res['crop'] == "Potato"

    # Scenario 3: Invalid JSON (Fallback)
    print("\nScenario 3: Invalid JSON (Fallback)")
    svc._ai = MockGeminiService('Not a JSON string')
    res = await svc.generate_recommendation({})
    print(f"Result: {res}")
    assert res['crop'] == "wheat"
    assert "fallback" in res['reason']

    # Scenario 4: Missing Keys (Fallback)
    print("\nScenario 4: Missing Keys (Fallback)")
    svc._ai = MockGeminiService('{"wrong_key": "val"}')
    res = await svc.generate_recommendation({})
    print(f"Result: {res}")
    assert res['crop'] == "wheat"

    print("\n--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    asyncio.run(test_scenarios())
