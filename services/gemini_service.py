import os
import asyncio
from dotenv import load_dotenv
from google import genai
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            raise ValueError("GEMINI_API_KEY not found in environment")
            
        # Initialize official Google GenAI Client
        self.client = genai.Client(
            api_key=self.api_key
        )
        print("Gemini 1.5 Flash client initialized successfully")

    async def generate_response(self, message: str) -> str:
        """
        Generates an AI response using gemini-1.5-flash.
        Follows the official Google GenAI SDK format.
        """
        print(f"Sending request to Gemini (Model: gemini-1.5-flash)... Message: {message[:50]}...")
        
        try:
            # Use the official async client via client.aio as requested
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=message
                ),
                timeout=15.0
            )
            
            print("Gemini response received from gemini-1.5-flash")
            ai_text = response.text.strip()
            return ai_text

        except Exception as e:
            # Improved error logging to show real API error
            error_msg = f"Gemini API Error: {str(e)}"
            print(error_msg)
            logger.error(error_msg, exc_info=True)
            return f"AI assistant temporarily unavailable. Error detail: {str(e)[:100]}"
