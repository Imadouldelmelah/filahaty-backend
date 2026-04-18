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
        """
        prompt = f"""
        You are a professional Algerian agronomist. 
        Analyze the following soil and climate conditions and recommend the most suitable crop.

        INPUT CONDITIONS:
        - Nitrogen: {context.get('nitrogen')}
        - Phosphorus: {context.get('phosphorus')}
        - Potassium: {context.get('potassium')}
        - Temperature: {context.get('temperature')}°C
        - Humidity: {context.get('humidity')}%
        - pH: {context.get('ph')}
        - Rainfall: {context.get('rainfall')}mm
        
        STRICT REQUIREMENT:
        Return ONLY a valid JSON object. No explanation outside JSON. No markdown code blocks.
        
        RESPONSE FORMAT:
        {{
            "crop": "crop_name",
            "confidence": "high/medium/low",
            "reason": "expert reasoning for this selection"
        }}
        """
        
        try:
            print("\n[AI_DEBUG] Initiating Crop Recommendation AI call...")
            logger.info("CROP_RECOMMENDATION: Calling AI for structured advice...")
            
            raw_response = await self._ai.generate(prompt)
            
            # Task 1: Print raw AI response before parsing
            print(f"[AI_DEBUG] Raw AI Response: {raw_response}")
            
            # Safe JSON parsing logic
            clean_response = raw_response.strip()
            
            # Handle markdown code blocks
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
            
            # Attempt to parse
            try:
                result = json.loads(clean_response)
            except json.JSONDecodeError as jde:
                # Task 3: Log errors clearly
                print(f"[AI_DEBUG] JSON Parsing Failed. Raw was: {clean_response}")
                logger.error(f"CROP_RECOMMENDATION: JSON parsing failed: {str(jde)}")
                raise ValueError("AI returned invalid JSON format")

            # Validate keys
            required_keys = ["crop", "confidence", "reason"]
            if not all(k in result for k in required_keys):
                 print(f"[AI_DEBUG] Validation Failed. Missing keys in: {list(result.keys())}")
                 logger.error(f"CROP_RECOMMENDATION: AI response missing keys.")
                 raise KeyError("AI response missing required schema keys")

            print("[AI_DEBUG] AI Call and Parsing Successful.")
            return result

        except Exception as e:
            # Task 3: Log errors clearly
            print(f"[AI_DEBUG] EXCEPTION OCCURRED: {type(e).__name__}: {str(e)}")
            logger.error(f"CROP_RECOMMENDATION_FAILURE: {str(e)}")
            # Fallback response
            return {
                "crop": "wheat",
                "confidence": "low",
                "reason": "fallback due to AI parsing error or service unavailability"
            }

# Export the class for late local instantiation
