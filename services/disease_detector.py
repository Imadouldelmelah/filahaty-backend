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
        prompt = """
        You are an expert plant pathologist and agricultural diagnostic AI.
        Analyze this image of a plant or crop. Identify any visible diseases, pests, nutrient deficiencies, or stress conditions.

        Strictly format your response as a valid JSON object matching this exact schema:
        {
            "diagnosis": "Name of the disease or stress factor. Be specific.",
            "confidence": "High/Medium/Low based on visual clarity",
            "solution": "Actionable, concrete steps the farmer should take to treat or mitigate this issue."
        }
        
        If the plant appears perfectly healthy, return:
        {
            "diagnosis": "Healthy",
            "confidence": "High",
            "solution": "Continue routine monitoring and maintenance."
        }

        Do NOT include any text outside the JSON object. Do not include markdown code block syntax around the JSON.
        """
        
        try:
            logger.info("Starting visual disease detection...")
            raw_response = await self._ai.generate_vision(prompt, base64_image, mime_type)
            
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

disease_detector_service = DiseaseDetectionService()
