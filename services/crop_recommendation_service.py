import json
import os
from services.gemini_service import GeminiService
from utils.logger import logger

class CropRecommendationService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_recommendation(self, context: dict, last_crop: str = None, candidates: list = None) -> dict:
        """
        Refined Recommendation using the HybridDecisionController.
        """
        from services.agronomy_engine import get_rule_based_crop
        from services.hybrid_controller import HybridDecisionController
        
        # Define the AI refinement step
        async def ai_refinement():
            from services.deepseek_service import get_deepseek_svc
            import asyncio
            
            prompt = f"""
            Suggest best crop based on soil, weather and region.
            Return JSON only:
            {{
                "crop": "string",
                "confidence": "string",
                "reason": "string",
                "alternatives": []
            }}
            
            Context Data: {json.dumps(context)}
            """
            # Use DeepSeek R1 for specialized agronomic reasoning
            svc = get_deepseek_svc()
            ai_data = await asyncio.to_thread(svc.generate_reasoning, prompt)
            return ai_data.get("response", "{}")

        # Execute via Controller (AI-First)
        return await HybridDecisionController.execute(
            baseline_func=lambda: get_rule_based_crop(context),
            ai_func=ai_refinement,
            schema_repair_keys=["crop", "confidence", "reason", "alternatives"],
            feature_name="CROP_IDEA_AI"
        )

# Export the class for late local instantiation
