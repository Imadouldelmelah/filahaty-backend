import json
import os
from services.gemini_service import GeminiService
from utils.logger import logger

class CropRecommendationService:
    def __init__(self):
        self._ai = GeminiService()

    async def generate_recommendation(self, context: dict) -> dict:
        """
        Generates a hardened AI crop recommendation with strict JSON enforcement.
        Ensures the response always matches the schema: {crop, confidence, reason}.
        Zero-failure design with multi-layer fallback.
        """
        # Task 2: Prepare clean input for AI
        prompt = f"""
        ACT AS: An elite Algerian Agronomist and Soil Scientist.
        TASK: Analyze real-time sensing data and recommend the most profitable and viable crop.
        
        SENSOR INPUTS:
        - Nitrogen: {context.get('nitrogen')}
        - Phosphorus: {context.get('phosphorus')}
        - Potassium: {context.get('potassium')}
        - Soil Moisture: {context.get('soil_moisture')}%
        - Temperature: {context.get('temperature')}°C
        - Humidity: {context.get('humidity')}%
        - pH Level: {context.get('ph')}
        - Rainfall: {context.get('rainfall')}mm
        
        STRICT OUTPUT FORMAT:
        Return ONLY a JSON object. No explanation, no markdown backticks, no text before or after.
        
        REQUIRED JSON SCHEMA:
        {{
            "crop": "Exact name of recommended crop",
            "confidence": "high" | "medium" | "low",
            "reason": "Detailed expert reasoning for the recommendation"
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
            # Task 5 & 7: Robust Fallback and Error Logging
            logger.error(f"CROP_RECOMMENDATION_ENGINE_FAILURE: {str(e)}")
            print(f"[AI_AUDIT] CRITICAL_FAILURE: {str(e)}")
            
            # Static Fallback System (Guaranteed valid JSON)
            return {
                "crop": "Wheat",
                "confidence": 50,
                "reason": "AI recommendation engine is recovering from a timeout. Recommending stable Algerian Wheat based on historic soil resilience.",
                "status": "system_fallback"
            }

# Export the class for late local instantiation
