import json
from services.gemini_service import GeminiService
from services.agronomy_engine import get_crop_plan
from utils.logger import logger

class AIAgronomistService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_advice(self, context: dict, is_retry: bool = False):
        """
        Generates structured agricultural advice based on a hybrid system.
        Supports a 'simplified retry' mode if the first AI response is unparseable.
        """
        crop_name = context.get('crop_name', '')
        current_stage_name = context.get('current_stage', '')
        journey_id = context.get('journey_id')
        weather_data = context.get('weather_data')
        monitoring_data = context.get('monitoring_data')
        
        # 1. Fetch Expert Rules from Agronomy Engine
        expert_rules = ""
        expert_plan = get_crop_plan(crop_name)
        
        scientific_insights = ""
        # Skip detailed weather analysis on retry to save tokens and simplify
        if weather_data and not is_retry:
            from services.weather_intelligence import WeatherIntelligenceService
            weather_intel = WeatherIntelligenceService()
            insights = weather_intel.analyze_weather(weather_data)
            alerts = "\n".join([f"!! {a}" for a in insights['alerts']])
            recs = "\n".join([f"* {r}" for r in insights['recommendations']])
            scientific_insights = f"\nSCIENTIFIC WEATHER GUARDRAILS (MANDATORY):\n{alerts}\n{recs}"
        
        # 3. Fetch Journey History - SKIPPED ON RETRY
        history_context = ""
        if journey_id and not is_retry:
            from services.tracking_service import TrackingService
            tracking_svc = TrackingService()
            progress = tracking_svc.get_progress(journey_id)
            if "history" in progress and progress["history"]:
                # ONLY take last 2 items
                last_actions = progress["history"][-2:]
                history_items = [f"- {h['action']} (at {h['timestamp']})" for h in last_actions]
                history_context = "\nRECENT ACTIONS:\n" + "\n".join(history_items)
            else:
                history_context = "\nRECENT ACTIONS: None."
        
        # 4. Process Real-time Monitoring Data
        monitoring_context = ""
        if monitoring_data:
            monitoring_context = f"IoT: M:{monitoring_data.get('soil_moisture')}% pH:{monitoring_data.get('ph')} N:{monitoring_data.get('nitrogen')} P:{monitoring_data.get('phosphorus')} K:{monitoring_data.get('potassium')} T:{monitoring_data.get('temperature')}C H:{monitoring_data.get('humidity')}%"
        else:
            monitoring_context = "IoT: No data."
        
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
        retry_warning = ""
        if is_retry:
            retry_warning = "CRITICAL: YOUR PREVIOUS ATTEMPT WAS INVALID. REPLY WITH ONLY THE JSON OBJECT BELOW.\n"

        prompt = f"""
        {retry_warning}
        ACT AS: A Senior Algerian Agronomist.
        TASK: Provide context-aware advice combining expert rules and real-time sensor data.
        
        USER CONTEXT:
        - Crop: {crop_name}
        - Current Growth Stage: {current_stage_name}
        - Soil Type: {context.get('soil')}
        
        {scientific_insights}
        {history_context}
        {monitoring_context}
        {expert_rules}
        
        STRICT OUTPUT FORMAT:
        You MUST return valid JSON only. No explanation.
        
        REQUIRED SCHEMA:
        {{
            "stage": "Growth",
            "tasks": ["Water plants", "Check soil moisture"],
            "advice": "Maintain moderate irrigation",
            "alerts": []
        }}
        """
        
        try:
            logger.info(f"AI_AGRONOMIST: Generating advice for {crop_name} (retry={is_retry})")
            raw_response = await self._ai.generate(prompt)
            
            # Log raw response for debugging JSON failure
            logger.debug(f"AI_AGRONOMIST_RAW: {raw_response}")
            
            # Indestructible JSON extraction logic
            clean_response = raw_response.strip()
            
            # Check for service-level errors
            if not clean_response.startswith("{") and "AI error" in clean_response:
                 logger.error(f"AI_AGRONOMIST: Service error: {clean_response}")
                 raise ValueError("Service error")

            # Deep cleaning: find first { and last }
            start_idx = clean_response.find("{")
            end_idx = clean_response.rfind("}")
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("JSON braces not found")
                
            json_str = clean_response[start_idx : end_idx + 1]
            data = json.loads(json_str)
            
            # Auto-repair schema
            required_keys = ["stage", "tasks", "advice", "alerts"]
            for key in required_keys:
                if key not in data:
                    data[key] = "Unknown" if key != "tasks" and key != "alerts" else []
            
            return data
            
        except Exception as e:
            if not is_retry:
                logger.warning(f"AI_AGRONOMIST_RETRY: Initial attempt failed ({str(e)}). Retrying with simplified prompt...")
                return await self.generate_advice(context, is_retry=True)
                
            logger.error(f"AI_AGRONOMIST_TOTAL_FAILURE: {str(e)} | raw: {raw_response if 'raw_response' in locals() else 'None'}")
            # Final safety fallback
            return {
                "stage": current_stage_name or "Unknown",
                "tasks": ["Check field conditions", "Monitor soil moisture"],
                "advice": "Our AI advisor is currently performing maintenance. Please follow standard regional protocols.",
                "alerts": []
            }

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
            raw_response = await self._ai.generate(full_prompt)
            return raw_response.strip()
        except Exception as e:
            logger.error(f"Advanced Chat Error: {str(e)}")
            return "I apologize, but I am currently unable to process your request due to a system error. Please try again shortly."
# Export the class for lazy instantiation inside routes
