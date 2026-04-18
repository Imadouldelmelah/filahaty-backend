import json
from services.gemini_service import GeminiService
from services.agronomy_engine import get_crop_plan
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
        weather_data = context.get('weather_data')
        monitoring_data = context.get('monitoring_data')
        
        # 1. Fetch Expert Rules from Agronomy Engine
        expert_rules = ""
        expert_plan = get_crop_plan(crop_name)
        
        scientific_insights = ""
        if weather_data:
            from services.weather_intelligence import WeatherIntelligenceService
            weather_intel = WeatherIntelligenceService()
            insights = weather_intel.analyze_weather(weather_data)
            alerts = "\n".join([f"!! {a}" for a in insights['alerts']])
            recs = "\n".join([f"* {r}" for r in insights['recommendations']])
            scientific_insights = f"\nSCIENTIFIC WEATHER GUARDRAILS (MANDATORY):\n{alerts}\n{recs}"
        
        # 3. Fetch Journey History (Context Memory)
        history_context = ""
        if journey_id:
            from services.tracking_service import TrackingService
            tracking_svc = TrackingService()
            progress = tracking_svc.get_progress(journey_id)
            if "history" in progress and progress["history"]:
                history_items = [f"- {h['action']} (at {h['timestamp']})" for h in progress["history"]]
                history_context = "\nPREVIOUS ACTIONS TAKEN:\n" + "\n".join(history_items)
            else:
                history_context = "\nPREVIOUS ACTIONS TAKEN:\n- No history recorded yet."
        
        # 4. Process Real-time Monitoring Data
        monitoring_context = ""
        if monitoring_data:
            monitoring_context = f"""
            REAL-TIME IOT SENSOR READINGS (CRITICAL):
            - Soil Moisture: {monitoring_data.get('soil_moisture')}%
            - Soil pH: {monitoring_data.get('ph')}
            - Nitrogen (N): {monitoring_data.get('N')} mg/kg
            - Phosphorus (P): {monitoring_data.get('P')} mg/kg
            - Potassium (K): {monitoring_data.get('K')} mg/kg
            - Field Temp: {monitoring_data.get('temperature')}°C
            - Field Humidity: {monitoring_data.get('humidity')}%
            """
        else:
            monitoring_context = "\nREAL-TIME SENSOR DATA:\n- Offline/No data available."
        
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
        You are an expert agronomist. You act like a real, experienced agronomist explaining decisions directly to the farmer.
        Your advice must be highly practical, clear, and simple. Avoid dense academic jargon.
        
        STRICT QUALITY GUIDELINES:
        - EXPLAIN WHY AND WHAT: Always explain exactly WHY a decision was made, and clearly state WHAT the farmer should do.
        - NO GENERIC ANSWERS: Avoid broad advice like "water your plants". Instead, say e.g. "Water 3L per plant at 6 AM".
        - ACTIONABLE ADVICE: Every step must be a concrete, practical action a farmer can perform today.
        - AGRICULTURAL CORRECTNESS: Use precise agricultural terminology only when necessary, keeping it easy to understand.
        
        USER CONTEXT:
        - Crop: {crop_name}
        - Current Growth Stage: {current_stage_name}
        - Current Weather: {context.get('weather')}
        - Soil Type: {context.get('soil')}
        - Field Size: {context.get('field_size')}
        
        {scientific_insights}
        
        {history_context}
        
        {monitoring_context}
        
        {expert_rules}
        
        YOUR TASK:
        1. Start with the EXPERT RULES as your scientific foundation.
        2. MANDATORY WEATHER OVERRIDE:
           - Priority 1: Observe the SCIENTIFIC WEATHER GUARDRAILS.
           - If a guardrail contradicts an expert rule (e.g., skip irrigation due to rain), YOU MUST prioritize the guardrail.
           - Mention the specific weather metric (e.g., "Because temperature has reached 42°C, you must...")
        3. Respect the PREVIOUS ACTIONS:
           - Do not recommend redundant tasks that have already been recorded as completed.
           - Provide continuity (e.g., "Continuing from your last action of...")
        4. REACT TO SENSOR DATA (URGENT):
           - Analyze the REAL-TIME IOT SENSOR READINGS.
           - If moisture is low (<30%), prioritize irrigation.
           - If pH is unbalanced, explain how it affects nutrient uptake.
           - Explicitly mention the sensor values in your explanation (e.g., "Current moisture is 22%, which is dangerously low...").
        5. ENHANCE the rules by:
           - Explaining the importance of each task (the "why").
           - Increasing precision based on the local weather and soil.
           - Adapting the instructions to the the field size.
        5. Provide clear, simple, step-by-step instructions.
        6. Format your entire response as a VALID JSON object.
        7. Do NOT include any text outside the JSON object.
        8. The JSON schema MUST be:
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
        You are Filahaty AI, a highly advanced agricultural chat assistant. 
        You act like a real, experienced agronomist explaining things to a farmer.
        Keep your language Simple, Clear, and Practical. Do NOT use markdown code blocks or structured JSON responses. Simply write conversationally.
        
        FARMER'S CURRENT CONTEXT:
        - Crop: {crop_name}
        - Growth Stage: {current_stage}
        - Soil Type: {soil}
        
        WEATHER:
        {weather_data if weather_data else 'No live weather data provided.'}
        
        FIELD MONITORING SENSORS:
        {monitoring_data if monitoring_data else 'No live sensor data provided.'}
        
        YOUR INSTRUCTIONS:
        1. Answer the farmer's question directly and politely.
        2. Give step-by-step, actionable advice.
        3. Use the provided context to explain WHY your advice is correct.
        4. Focus exclusively on problem solving and optimizing their farm operation based directly on their real-time sensor/weather context if applicable.
        """
        
        user_prompt = f"Farmer says: {user_message}"
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        try:
            logger.info(f"Generating advanced chat response for {crop_name}")
            raw_response = await self._ai.generate(full_prompt)
            return raw_response.strip()
        except Exception as e:
            logger.error(f"Advanced Chat Error: {str(e)}")
            return "I apologize, but I am currently unable to process your request due to a system error. Please try again shortly."
# Export the class for lazy instantiation inside routes
