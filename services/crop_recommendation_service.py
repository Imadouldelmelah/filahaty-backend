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
            prompt = f"""
            ACT AS: Senior Agronomist.
            SUBJECT: Crop Selection Refinement.
            INPUT: {context}
            
            TASK: Refine the baseline recommendation with scientific reasoning and alternatives.
            SCHEMA: {{"crop": "...", "confidence": "high", "reason": "...", "alternatives": []}}
            """
            return await self._ai.generate(prompt)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=lambda: get_rule_based_crop(context),
            ai_func=ai_refinement,
            schema_repair_keys=["crop", "confidence", "reason", "alternatives"],
            feature_name="CROP_REC"
        )

# Export the class for late local instantiation
