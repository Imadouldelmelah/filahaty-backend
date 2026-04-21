import json
from services.gemini_service import GeminiService
from utils.logger import logger

class DiseaseDetectionService:
    def __init__(self):
        self._ai = GeminiService()

    async def analyze_crop_image(self, base64_image: str, mime_type: str = "image/jpeg") -> dict:
        """
        Analyzes an image of a plant/crop to detect diseases, stress, or deficiencies.
        """
        # Define JSON schema for strict vision output
        json_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "plant_disease_detection",
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
        
        try:
            logger.info("Starting visual disease detection...")
            
            # Revised prompt for schema-based vision support
            vision_prompt = "Identify diseases, pests, or deficiencies in this plant image and suggest solutions."
            
            raw_response = await self._ai.generate_vision(vision_prompt, base64_image, mime_type, response_format=json_schema)
            
            clean_response = raw_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
                
            diagnosis = json.loads(clean_response)
            
            if "diagnosis" not in diagnosis or "solution" not in diagnosis:
                raise ValueError("Vision AI response did not match the expected schema.")
                
            return diagnosis
            
        except Exception as e:
            logger.error(f"Disease Detection Error: {str(e)}")
            return {
                "diagnosis": "Analysis Unavailable",
                "confidence": "Low",
                "solution": "We could not securely process this image due to a system error. Please consult a local agronomist."
            }
# Export the class for lazy instantiation inside routes
