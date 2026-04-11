from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
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
            return response.text

        except Exception as e:
            # Logging for errors to Render logs
            print("Gemini API error:", str(e))
            # Return a safe fallback to the user
            return "AI assistant temporarily unavailable"
