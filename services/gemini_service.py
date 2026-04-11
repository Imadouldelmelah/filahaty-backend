import os
import asyncio
from dotenv import load_dotenv
from google import genai
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        # Initialize the official Google GenAI Client
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(
            api_key=api_key
        )
        print("Gemini 1.5 Flash client initialized with explicit content format")

    async def generate_response(self, message: str):
        print("Sending prompt to Gemini (Strict Format):", message)
        
        try:
            # Using the explicit request format requested by the user
            # Note: Using .aio for non-blocking FastAPI performance
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[{
                        "role": "user",
                        "parts": [{"text": message}]
                    }]
                ),
                timeout=15.0
            )
            
            print("Gemini response received")
            ai_text = response.text.strip()
            return ai_text

        except Exception as e:
            print("Gemini API error:", str(e))
            logger.error(f"Gemini API Exception: {str(e)}", exc_info=True)
            return "AI assistant temporarily unavailable"
