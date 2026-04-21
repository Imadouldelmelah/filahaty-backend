import json
from services.gemini_service import GeminiService
from utils.logger import logger

class DiseaseDetectionService:
    def __init__(self):
        self._ai = GeminiService()

    async def analyze_crop_image(self, base64_image: str, mime_type: str = "image/jpeg") -> dict:
        """
        Visual Disease detection using HybridDecisionController.
        """
        from services.hybrid_controller import HybridDecisionController
        
        # 1. Step 1: Baseline (Safe fallback)
        def get_baseline():
            return {
                "diagnosis": "Visual analysis is under maintenance",
                "confidence": "Low",
                "solution": "We cannot verify this image right now. Please monitor your crops for visible signs of pest or disease and consult a local agronomist.",
                "status": "offline_optimized"
            }

        # 2. Step 2 & 3: AI Refinement (Vision)
        async def ai_vision_task():
            # Define schema for strict output
            json_schema = {
                "type": "json_schema",
                "json_schema": {
                    "name": "plant_disease",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "diagnosis": {"type": "string"},
                            "confidence": {"type": "string", "enum": ["High", "Medium", "Low"]},
                            "solution": {"type": "string"}
                        },
                        "required": ["diagnosis", "confidence", "solution"]
                    }
                }
            }
            prompt = "Identify diseases, pests, or deficiencies in this plant image and provide actionable expert solutions."
            return await self._ai.generate_vision(prompt, base64_image, mime_type, response_format=json_schema)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=get_baseline,
            ai_func=ai_vision_task,
            schema_repair_keys=["diagnosis", "confidence", "solution"],
            feature_name="VISION_DISEASE"
        )
# Export the class for lazy instantiation inside routes
