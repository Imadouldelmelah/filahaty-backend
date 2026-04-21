import json
import os
from services.gemini_service import GeminiService
from utils.logger import logger

class CropRecommendationService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_recommendation(self, context: dict, last_crop: str = None, candidates: list = None) -> dict:
        """
        Generates a hybrid AI crop recommendation by refining rule-engine candidates.
        Ensures the response always matches the schema: {crop, confidence, reason}.
        """
        history_context = f"\n        PREVIOUSLY RECOMMENDED: {last_crop}" if last_crop else ""
        candidate_context = f"\n        SCIENTIFIC CANDIDATES: {', '.join(candidates)}" if candidates else ""

        # Task 2: Prepare hybrid scientific input for AI
        prompt = f"""
        ACT AS: An elite Agronomist and Soil Scientist specializing in specialized N-African agriculture.
        TASK: Refine and select the best crop from the identified scientific candidates.
        {history_context}
        {candidate_context}
        
        SENSOR INPUTS:
        - Nitrogen: {context.get('nitrogen')} mg/kg
        - Phosphorus: {context.get('phosphorus')} mg/kg
        - Potassium: {context.get('potassium')} mg/kg
        - Soil Moisture: {context.get('soil_moisture')}%
        - Temperature: {context.get('temperature')}°C
        - Humidity: {context.get('humidity')}%
        - pH Level: {context.get('ph')}
        - Rainfall: {context.get('rainfall')}mm
        
        HYBRID INSTRUCTIONS:
        1. SELECTION PRIORITY: If SCIENTIFIC CANDIDATES are provided, you MUST select the BEST one from that specific list. 
        2. DATA REFINEMENT: Use the N-P-K ratios to differentiate between candidates (e.g., if Tomato and Pepper are both candidates, high N favors Tomato).
        3. DIVERSITY: Do not repeat the PREVIOUSLY RECOMMENDED crop if a suitable alternative exists in the candidates.
        4. JUSTIFICATION: Provide an expert reasoning that links the specific sensor data to why you chose this specific candidate.
        
        STRICT OUTPUT FORMAT:
        Return ONLY a JSON object. No markdown backticks.
        
        REQUIRED JSON SCHEMA:
        {{
            "crop": "The chosen crop name from candidates (e.g., Wheat, Potato, Olive, etc.)",
            "confidence": "high" | "medium" | "low",
            "reason": "Expert scientific refinement for selecting this specific candidate."
        }}
        """
        
        try:
            # Task 7: Log monitoring data input
            logger.info(f"CROP_RECOMMENDATION_INPUT: {context}")
            print(f"[AI_AUDIT] Input Context: {context}")
            
            raw_response = await self._ai.generate(prompt)
            
            # Task 7: Log AI raw response
            logger.info(f"CROP_RECOMMENDATION_AI_RAW: {raw_response}")
            print(f"[AI_AUDIT] Raw Response: {raw_response}")
            
            if not raw_response or "AI temporarily unavailable" in raw_response:
                raise ValueError("AI Service down")

            # Task 4: Hardened JSON Extraction Logic
            clean_response = raw_response.strip()
            
            # Remove markdown backticks if present
            if "```json" in clean_response:
                clean_response = clean_response.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_response:
                clean_response = clean_response.split("```")[1].split("```")[0].strip()
            
            # Locate first '{' and last '}' to handle conversational noise
            start_idx = clean_response.find("{")
            end_idx = clean_response.rfind("}")
            
            if start_idx == -1 or end_idx == -1:
                logger.error("CROP_RECOMMENDATION: Could not find JSON braces in response.")
                raise ValueError("Malformed AI response format")
                
            json_str = clean_response[start_idx : end_idx + 1]
            
            try:
                result = json.loads(json_str)
            except json.JSONDecodeError as jde:
                logger.error(f"CROP_RECOMMENDATION: JSON parse failed: {str(jde)}")
                raise ValueError("AI response not valid JSON")

            # Task 4: Validate and Map Data for Android Contract
            # Confidence Mapper: high/medium/low -> Int (Android contract requirement)
            raw_conf = str(result.get("confidence", "medium")).lower()
            conf_map = {"high": 95, "medium": 70, "low": 40}
            mapped_confidence = conf_map.get(raw_conf, 60)
            
            final_result = {
                "crop": result.get("crop", "Wheat"),
                "confidence": mapped_confidence,
                "reason": result.get("reason", "Standard recommended profile based on sensors."),
                "status": "ai_optimized"
            }
            
            logger.info(f"CROP_RECOMMENDATION_SUCCESS: Recommended {final_result['crop']}")
            return final_result

        except Exception as e:
            # Robust fallback to rule-based expert system
            logger.error(f"CROP_RECOMMENDATION_AI_FAILURE: {str(e)}")
            return self._get_rule_based_fallback(context)

    def _get_rule_based_fallback(self, context: dict) -> dict:
        """
        Agronomy-based expert system fallback when AI is unavailable.
        Uses temperature, humidity, and pH rules.
        """
        # 1. Decision Logic based on USER requirements:
        # IF temperature > 30: corn
        # IF humidity > 80: rice
        # IF pH < 6: potato
        
        temp = context.get("temperature", 0)
        humidity = context.get("humidity", 0)
        ph = context.get("ph", 7.0)
        
        crop = "Wheat" # Default
        reason = "AI recommendation engine is recovering. Recommending stable Algerian Wheat based on historic soil resilience."
        
        if temp > 30:
            crop = "Corn"
            reason = f"High temperature detected ({temp}°C). Recommending heat-tolerant Corn as a resilient fallback."
        elif humidity > 80:
            crop = "Rice"
            reason = f"High humidity detected ({humidity}%). Recommending Rice based on moisture compatibility."
        elif ph < 6:
            crop = "Potato"
            reason = f"Acidic soil detected (pH {ph}). Recommending Potato as it thrives in lower pH conditions."
            
        return {
            "crop": crop,
            "confidence": 60, # Standard medium confidence for rule-based engine
            "reason": reason,
            "status": "rule_engine_fallback"
        }

# Export the class for late local instantiation
