import os
import asyncio
from dotenv import load_dotenv
from google import genai
from utils.logger import logger

# Explicitly load environment variables for this service
load_dotenv()

class GeminiService:
    def __init__(self):
        # AI requests usually take some time, we set a reasonable timeout
        self.request_timeout = 15.0 # seconds
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Debug log for API key
        if api_key:
            print("Loaded GEMINI_API_KEY:", api_key[:10] + "...")
        else:
            print("Loaded GEMINI_API_KEY: None")
            
        if not api_key:
            logger.error("GEMINI_API_KEY initialization failed: Key not found")
            raise ValueError("GEMINI_API_KEY not found in environment")
            
        # Initialize the official Google GenAI Client
        self.client = genai.Client(api_key=api_key)
        
        print("Gemma 3 1B model initialized successfully")
        logger.info("GeminiService initialized successfully (Model: gemma-3-1b-it)")

    async def ask_ai(self, message: str) -> str:
        print("User question:", message)
        
        system_prompt = """
You are Filahaty AI, a smart agricultural assistant helping farmers.

You provide advice about:
- crops
- irrigation
- soil health
- pest control
- fertilizers
- climate adaptation
"""
        
        full_prompt = system_prompt + "\nFarmer question:\n" + message
        
        print("Sending request to Gemini...")
        try:
            # Use the official async client via client.aio
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model="gemma-3-1b-it",
                    contents=full_prompt
                ),
                timeout=self.request_timeout
            )
            
            print("Gemini response received")
            ai_text = response.text.strip()
            print("AI OUTPUT:", ai_text)
            return ai_text

        except asyncio.TimeoutError:
            print("Gemini error: Timeout reached")
            logger.error("AI Request Failed: Timeout reached")
            return "AI assistant temporarily unavailable"
            
        except Exception as e:
            # Explicitly log the full error for debugging as requested
            print("Gemini error:", e)
            logger.error(f"AI Request Failed: {str(e)}", exc_info=True)
            return f"AI assistant temporarily unavailable. Error detail: {str(e)[:50]}..."
