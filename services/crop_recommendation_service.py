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
            from services.agronomy_engine import get_rule_based_crop
            base_crop = get_rule_based_crop(context)["crop"]
            
            prompt = f"""
            ACT AS: Master Agronomist.
            SUBJECT: Scientific Reasoning for Crop Selection.
            INPUT_DATA: {context}
            RECOMMENDED_CROP: {base_crop}
            
            TASK: 
            1. Provide a detailed scientific 'reason' for why '{base_crop}' is the absolute best choice based on the input data.
            2. Suggest 2-3 compatible 'alternatives'.
            
            FORMAT: JSON only.
            SCHEMA: {{"crop": "{base_crop}", "confidence": "high", "reason": "Scientific explanation...", "alternatives": []}}
            """
            return await self._ai.generate(prompt)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=lambda: get_rule_based_crop(context),
            ai_func=ai_refinement,
            schema_repair_keys=["crop", "confidence", "reason", "alternatives"],
            protected_keys=["crop"],
            feature_name="CROP_REC"
        )

# Export the class for late local instantiation
