import json
from services.gemini_service import GeminiService
from services.agronomy_engine import get_crop_plan
from utils.logger import logger

class AIAgronomistService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_advice(self, context: dict, is_retry: bool = False):
        """
        Refined Advice using the HybridDecisionController.
        """
        from services.agronomy_engine import get_rule_based_advice
        from services.hybrid_controller import HybridDecisionController
        
        crop_name = context.get('crop_name', '')
        current_stage = context.get('current_stage', '')
        
        # Define the AI refinement step
        async def ai_refinement():
            prompt = f"""
            Generate farming journey for crop: {crop_name} at stage: {current_stage}.
            
            Ensure the response strictly follows this JSON format:
            {{
                "advice": "Short expert advice.",
                "alerts": []
            }}
            """
            # Rely on system instructions and manual JSON extraction for weak models
            return await self._ai.generate(prompt)

        # Execute via Controller
        return await HybridDecisionController.execute(
            baseline_func=lambda: get_rule_based_advice(crop_name, current_stage),
            ai_func=ai_refinement,
            schema_repair_keys=["stage", "tasks", "advice", "alerts"],
            protected_keys=["tasks", "stage"],
            feature_name="AI_ADVICE"
        )

    async def generate_advanced_chat(self, context: dict, user_message: str) -> str:
        """
        Advanced Context-Aware Chat Assistant.
        Acts as a supportive, step-by-step agronomist answering direct questions.
        """
        crop_name = context.get('crop_name', 'Unknown')
        current_stage = context.get('current_stage', 'Unknown')
        weather_data = context.get('weather_data')
        monitoring_data = context.get('monitoring_data')
        soil = context.get('soil', 'Unknown')
        
        system_prompt = f"""
        Role: Filahaty AI, expert Algerian agronomist. 
        Context: Crop:{crop_name}, Stage:{current_stage}, Soil:{soil}.
        Weather: {weather_data if weather_data else 'None'}.
        Sensors: {monitoring_data if monitoring_data else 'None'}.
        Instruction: Answer concisely, step-by-step, no JSON/markdown blocks.
        """
        
        # Truncate user message to 200 chars to save tokens
        short_message = user_message[:200]
        user_prompt = f"Farmer says: {short_message}"
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        try:
            logger.info(f"Generating advanced chat response for {crop_name}")
            raw_response = await self._ai.generate(full_prompt, require_json=False)
            
            # Intercept service error strings
            if "AI error" in raw_response:
                 raise ValueError(raw_response)
                 
            return raw_response.strip()
        except Exception as e:
            logger.warning(f"Advanced_Chat_AI_SKIPPED: {str(e)}. Using safe baseline.")
            return "Smart offline mode activated: I can still guide you based on agricultural knowledge."
# Export the class for lazy instantiation inside routes
