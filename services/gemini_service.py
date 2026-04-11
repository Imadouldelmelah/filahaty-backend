from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # Verify the API key status as requested
        api_key = os.getenv("GEMINI_API_KEY")
        print("Gemini API key loaded:", api_key is not None)
        
        if not api_key:
            print("Gemini API ERROR: GEMINI_API_KEY is missing from environment variables")
            
        self.client = genai.Client(
            api_key=api_key
        )

    async def generate_response(self, message: str):
        # Logging before the request
        print("Sending prompt to Gemini:", message)
        
        try:
            # Using the exact structure and model requested
            # Note: Using .aio with await for proper async execution in FastAPI
            response = await self.client.aio.models.generate_content(
                model="gemini-1.5-flash",
                contents=[{
                    "role": "user",
                    "parts": [{"text": message}]
                }]
            )
            if hasattr(response, "text") and response.text:
                return response.text
            else:
                return str(response)

        except Exception as e:
            # Detailed logging for Render logs
            print("Gemini API ERROR:", str(e))
            # Return the real error message for debugging as requested
            return f"Gemini error: {str(e)}"
