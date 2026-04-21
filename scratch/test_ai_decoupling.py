import asyncio
import os
import sys
import json
from unittest.mock import AsyncMock, patch

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

from services.crop_recommendation_service import CropRecommendationService
from services.ai_agronomist import AIAgronomistService

async def test_ai_decoupling():
    print("Verifying AI Decoupling (Protection of Core Logic)...")
    
    # Mock AI response that tries to overwrite core decisions
    conflicting_ai_response = json.dumps({
        "crop": "CACTUS_OVERWRITE",
        "stage": "DOOMSDAY_STAGE",
        "tasks": ["DELETE_EVERYTHING"],
        "reason": "AI is trying to take over.",
        "confidence": "high",
        "advice": "This advice should be kept, but the crop and tasks should be blocked."
    })

    with patch("services.gemini_service.GeminiService.generate", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = conflicting_ai_response
        
        print("\n--- Testing Crop Recommendation Decoupling ---")
        recommendation_svc = CropRecommendationService()
        # Temp 35 triggers 'Corn' in rule-based engine
        context_crop = {"temperature": 35, "humidity": 40, "ph": 6.5}
        rec = await recommendation_svc.generate_recommendation(context_crop)
        print(f"Result Crop: {rec['crop']}")
        print(f"AI Reason: {rec['reason']}")
        
        # ASSERT: Crop must be 'Corn' (Baseline), NOT 'CACTUS_OVERWRITE'
        assert rec["crop"] == "Corn"
        print("PASS: Rule-based 'Corn' was preserved despite AI attempts to overwrite.")

        print("\n--- Testing Farming Journey Decoupling ---")
        agronomist_svc = AIAgronomistService()
        # Tomato Growth stage baseline
        context_journey = {"crop_name": "Tomato", "current_stage": "Growth"}
        advice = await agronomist_svc.generate_advice(context_journey)
        
        print(f"Result Stage: {advice['stage']}")
        print(f"Number of Tasks: {len(advice['tasks'])}")
        print(f"AI Advice: {advice['advice']}")

        # ASSERT: Stage and Tasks must come from Baseline
        assert advice["stage"] == "Growth"
        assert "DELETE_EVERYTHING" not in advice["tasks"]
        assert len(advice["tasks"]) > 1 # Should have real tasks from engine
        print("PASS: Rule-based tasks and stage were preserved despite AI attempts to overwrite.")

    print("\nAI DECOUPLING VERIFIED: Core decisions are 100% offline-driven.")

if __name__ == "__main__":
    asyncio.run(test_ai_decoupling())
