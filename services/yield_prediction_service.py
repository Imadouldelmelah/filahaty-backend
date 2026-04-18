import json
from services.gemini_service import GeminiService
from utils.logger import logger

class YieldPredictionService:
    def __init__(self):
        self._ai = GeminiService()

    async def predict_yield(self, context: dict) -> dict:
        """
        Uses AI to predict the expected yield of a crop based on environmental and field context.
        """
        crop_name = context.get('crop_name', 'Unknown')
        field_size = context.get('field_size_hectares', 1.0)
        monitoring_data = context.get('monitoring_data', {})
        weather_data = context.get('weather_data', {})
        
        prompt = f"""
        You are an advanced agricultural data scientist. Your job is to predict the expected yield for a farmer's crop.
        
        INPUT DATA:
        - Crop: {crop_name}
        - Field Size: {field_size} Hectares
        - Sensors (IoT): {json.dumps(monitoring_data)}
        - Weather: {json.dumps(weather_data)}
        
        YOUR TASK:
        1. Calculate the estimated yield (e.g., Tons, Quintals). Be realistic based on typical yields for the crop and the provided field size.
        2. Assign a confidence level (High, Medium, Low) based on the consistency of the data (e.g., if weather is missing, confidence might be lower).
        3. Provide 3 specific tips to maximize this yield based on the sensor data (e.g., if moisture is low, suggest optimized irrigation).

        Strictly format your response as a valid JSON object matching this exact schema:
        {{
            "expected_yield": "Estimated amount + Unit (e.g., 45 Tons)",
            "confidence": "High/Medium/Low",
            "tips": ["Tip 1", "Tip 2", "Tip 3"]
        }}
        
        Do NOT include any text outside the JSON object. Do not include markdown code block syntax around the JSON.
        """
        
        try:
            logger.info(f"Predicting yield for {crop_name} on {field_size} ha.")
            raw_response = await self._ai.generate(prompt)
            
            # Clean response for JSON parsing
            clean_response = raw_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
                
            prediction = json.loads(clean_response)
            
            # Basic validation
            if "expected_yield" not in prediction or "tips" not in prediction:
                raise ValueError("Yield AI response did not match the expected schema.")
                
            return prediction
            
        except Exception as e:
            logger.error(f"Yield Prediction Service Error: {str(e)}")
            return {
                "expected_yield": "Prediction Unavailable",
                "confidence": "Low",
                "tips": [
                    "Ensure sensors are online and reporting accurate data.",
                    "Check weather forecast for upcoming temperature peaks.",
                    "Monitor soil nutrients to maintain optimal growth baseline."
                ]
            }
# Export the class for lazy instantiation inside routes
