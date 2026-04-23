import json
from services.gemini_service import GeminiService
from utils.logger import logger

class AIDecisionEngine:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_decision(self, context: dict) -> dict:
        """
        Decision synthesis using HybridDecisionController.
        """
        from services.hybrid_controller import HybridDecisionController
        
        crop_name = context.get('crop_name', 'Unknown')
        
        # 1. Step 1: Baseline (Safe Monitoring)
        def get_baseline():
            return {
                "decision": "Maintain Routine Monitoring",
                "priority": "low",
                "reason": "Current sensor baselines indicate a stable agricultural environment.",
                "action": "Ensure all sensors are clean and properly calibrated while monitoring plant vigor visually.",
                "status": "offline_optimized"
            }

        # 2. Step 2 & 3: AI Refinement
        async def ai_decision_task():
            # Compress context strictly to core details
            short_context = {
                "crop": crop_name,
                "stage": context.get("current_stage", "Unknown")
            }
            prompt = f"""
            ACT AS: Master Agronomist.
            CONTEXT: {short_context}
            
            TASK: Synthesize a unified farming decision.
            SCHEMA: {{"decision": "...", "priority": "high/medium/low", "reason": "...", "action": "..."}}
            """
            return await self._ai.generate(prompt)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=get_baseline,
            ai_func=ai_decision_task,
            schema_repair_keys=["decision", "priority", "reason", "action"],
            feature_name="CENTRAL_DECISION"
        )
# Export the class for lazy instantiation inside routes
