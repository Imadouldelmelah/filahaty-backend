import json
from services.gemini_service import GeminiService
from services.agronomy_engine import get_crop_plan
from services.tracking_service import tracking_service
from utils.logger import logger

class AIAgronomistService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_advice(self, context: dict):
        """
        Generates structured agricultural advice based on a hybrid system:
        Expert Rules (Agronomy Engine) + AI Intelligence (OpenRouter/Gemini).
        """
        crop_name = context.get('crop_name', '')
        current_stage_name = context.get('current_stage', '')
        journey_id = context.get('journey_id')
        
        # 1. Fetch Expert Rules from Agronomy Engine
        expert_rules = ""
        expert_plan = get_crop_plan(crop_name)
        
        # 2. Fetch Journey History (Context Memory)
        history_context = ""
        if journey_id:
            progress = tracking_service.get_progress(journey_id)
            if "history" in progress and progress["history"]:
                history_items = [f"- {h['action']} (at {h['timestamp']})" for h in progress["history"]]
                history_context = "\nPREVIOUS ACTIONS TAKEN:\n" + "\n".join(history_items)
            else:
                history_context = "\nPREVIOUS ACTIONS TAKEN:\n- No history recorded yet."
        
        if "error" not in expert_plan:
            # Find the specific stage in the expert plan
            stage_data = next(
                (s for s in expert_plan.get("stages", []) if s["name"].lower() == current_stage_name.lower()), 
                None
            )
            if stage_data:
                expert_rules = f"""
                EXPERT RULES (MANDATORY BASELINE):
                - Standard Tasks: {', '.join(stage_data.get('tasks', []))}
                - Expert Irrigation: {stage_data.get('irrigation')}
                - Expert Fertilization: {stage_data.get('fertilizer')}
                - Expert Monitoring: {stage_data.get('monitoring')}
                """
            else:
                logger.warning(f"Stage '{current_stage_name}' not found in expert plan for {crop_name}")
        else:
            logger.warning(f"No expert plan found for crop: {crop_name}")

        # 2. Construct the Hybrid Prompt
        prompt = f"""
        You are an expert agronomist. You guide farmers step by step to maximize yield. 
        Your advice must be practical, simple, and precise.
        
        STRICT QUALITY GUIDELINES:
        - NO GENERIC ANSWERS: Avoid broad advice like "water your plants". Instead, say e.g. "Water 3L per plant at 6 AM".
        - ACTIONABLE ADVICE: Every step must be a concrete action a farmer can perform today.
        - AGRICULTURAL CORRECTNESS: Use precise agricultural terminology and scientifically sound methods.
        
        USER CONTEXT:
        - Crop: {crop_name}
        - Current Growth Stage: {current_stage_name}
        - Current Weather: {context.get('weather')}
        - Soil Type: {context.get('soil')}
        - Field Size: {context.get('field_size')}
        
        {history_context}
        
        {expert_rules}
        
        YOUR TASK:
        1. Start with the EXPERT RULES as your scientific foundation.
        2. Respect the PREVIOUS ACTIONS:
           - Do not recommend redundant tasks that have already been recorded as completed.
           - Provide continuity (e.g., "Continuing from your last action of...")
        3. ENHANCE the rules by:
           - Explaining the importance of each task (the "why").
           - Increasing precision based on the local weather and soil (e.g., if it's hot, adjust irrigation).
           - Adapting the instructions to the the field size.
        3. Provide clear, simple, step-by-step instructions.
        4. Format your entire response as a VALID JSON object.
        5. Do NOT include any text outside the JSON object.
        6. The JSON schema MUST be:
        {{
            "advice": "Grounded expert advice string with professional tone.",
            "actions": ["Step 1: description", "Step 2: description", ...]
        }}
        """
        
        try:
            logger.info(f"Generating hybrid expert advice for {crop_name}")
            raw_response = await self._ai.generate(prompt)
            
            # Clean response for JSON parsing
            clean_response = raw_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
                
            return json.loads(clean_response)
            
        except Exception as e:
            logger.error(f"AI Agronomist Error: {str(e)}")
            return {
                "advice": "Our AI expert is currently busy. Please follow standard stage guidelines for your crop.",
                "actions": ["Check soil moisture", "Inspect for common pests"]
            }

ai_agronomist = AIAgronomistService()
