import json
from services.gemini_service import GeminiService
from utils.logger import logger

class AIDecisionEngine:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_decision(self, context: dict) -> dict:
        """
        Generates a central, intelligent decision by combining multiple environmental
        and monitoring factors.
        
        Expected context keys:
        - crop_name (str)
        - current_stage (str)
        - weather_data (dict)
        - monitoring_data (dict)
        """
        crop_name = context.get('crop_name', 'Unknown Crop')
        current_stage = context.get('current_stage', 'Unknown Stage')
        weather_data = context.get('weather_data', {})
        monitoring_data = context.get('monitoring_data', {})
        
        prompt = f"""
        You are the Central Intelligent Decision Engine for an advanced agricultural platform.
        Your job is to analyze real-time conditions and produce a single overarching decision
        to optimize crop health and yield.

        INPUT CONTEXT:
        - Crop: {crop_name}
        - Current Growth Stage: {current_stage}
        
        WEATHER CONDITIONS:
        - Temperature: {weather_data.get('temperature', 'N/A')}°C
        - Humidity: {weather_data.get('humidity', 'N/A')}%
        - Rainfall: {weather_data.get('rain', 0.0)} mm
        
        FIELD MONITORING SENSOR DATA:
        - Soil Moisture: {monitoring_data.get('soil_moisture', 'N/A')}%
        - Soil pH: {monitoring_data.get('ph', 'N/A')}
        - Nitrogen (N): {monitoring_data.get('N', 'N/A')} mg/kg
        - Phosphorus (P): {monitoring_data.get('P', 'N/A')} mg/kg
        - Potassium (K): {monitoring_data.get('K', 'N/A')} mg/kg
        - Field Temp: {monitoring_data.get('temperature', 'N/A')}°C
        - Field Humidity: {monitoring_data.get('humidity', 'N/A')}%

        YOUR TASK:
        Analyze the combined inputs. Make a concrete decision for the farmer.
        Act like a real, experienced agronomist explaining decisions directly to the farmer.
        Your explanation must cover:
        1. WHY the decision was made (based on the real-time data).
        2. Exactly WHAT the farmer should do.
        Keep the language exceptionally simple, clear, and highly practical. Avoid dense academic jargon.
        
        Examples of decisions: "Irrigate now", "Delay irrigation", "Apply fertilizer", "Apply Fungicide", "Continue routine monitoring".
        
        Strictly format your response as a valid JSON object matching this exact schema:
        {{
            "decision": "Short, concrete decision statement",
            "priority": "high", // Must be one of: "high", "medium", "low"
            "reason": "Simple, clear agronomist explanation of WHY this decision was made.",
            "action": "Clear, practical, actionable steps the farmer must take right now."
        }}
        
        Do NOT include any text outside the JSON object. Do not include markdown code block syntax around the JSON.
        """
        
        try:
            logger.info(f"Generating AI decision for {crop_name} in {current_stage} stage.")
            raw_response = await self._ai.generate(prompt)
            
            # Clean response for JSON parsing
            clean_response = raw_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
                
            decision = json.loads(clean_response)
            
            # Basic validation
            if "decision" not in decision or "priority" not in decision:
                raise ValueError("AI response did not match the expected schema.")
                
            return decision
            
        except Exception as e:
            logger.error(f"AI Decision Engine Error: {str(e)}")
            return {
                "decision": "System Error: Unable to compute decision.",
                "priority": "low",
                "reason": "The AI service is temporarily unavailable or returned malformed data.",
                "action": "Proceed with standard agricultural practices for your crop stage."
            }

ai_decision_engine = AIDecisionEngine()
