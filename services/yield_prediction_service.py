import json
from services.gemini_service import GeminiService
from utils.logger import logger

class YieldPredictionService:
    def __init__(self):
        self._ai = GeminiService()

    async def predict_yield(self, context: dict) -> dict:
        """
        Yield Prediction using HybridDecisionController.
        """
        from services.hybrid_controller import HybridDecisionController
        
        crop_name = context.get('crop_name', 'Unknown')
        field_size = context.get('field_size_hectares', 1.0)
        
        # 1. Step 1: Baseline (Conservative Estimates)
        def get_baseline():
            return {
                "expected_yield": f"Approx. {field_size * 5} - {field_size * 10} Quintals",
                "confidence": "Low",
                "tips": [
                    "Ensure adequate soil moisture during key growth stages.",
                    "Review NPK levels to support plant development.",
                    "Monitor and control local pest populations."
                ],
                "status": "offline_optimized"
            }

        # 2. Step 2 & 3: AI Refinement
        async def ai_predict_task():
            prompt = f"""
            ACT AS: Agricultural Data Scientist.
            CONTEXT: {crop_name} on {field_size} Ha.
            DATA: {json.dumps(context)}
            
            TASK: Provide a precise yield estimate and 3 specific yield-boosting tips.
            SCHEMA: {{"expected_yield": "...", "confidence": "High/Medium/Low", "tips": ["...", "...", "..."]}}
            """
            return await self._ai.generate(prompt)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=get_baseline,
            ai_func=ai_predict_task,
            schema_repair_keys=["expected_yield", "confidence", "tips"],
            feature_name="YIELD_PRED"
        )
# Export the class for lazy instantiation inside routes
