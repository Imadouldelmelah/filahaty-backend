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
        
        # Reliable models ordered by cost/speed (Primary to Fallback)
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        
        last_error = ""

        for model_name in models_to_try:
            print(f"Sending request to Gemini (Model: {model_name})...")
            try:
                response = await asyncio.wait_for(
                    self.client.aio.models.generate_content(
                        model=model_name,
                        contents=full_prompt
                    ),
                    timeout=self.request_timeout
                )
                
                print(f"Gemini response received from {model_name}")
                ai_text = response.text.strip()
                print("AI OUTPUT:", ai_text)
                return ai_text

            except asyncio.TimeoutError:
                err_msg = f"Timeout reached with {model_name}"
                print(f"Gemini error: {err_msg}")
                logger.warning(f"AI Model Error: {err_msg}")
                last_error = err_msg
                continue # Try next model
                
            except Exception as e:
                err_msg = f"{model_name} failed: {str(e)}"
                print(f"Gemini error: {err_msg}")
                logger.warning(f"AI Model Error: {err_msg}")
                last_error = err_msg
                
                # Check for specific quota or permission issues that might affect all models
                if "PERMISSION_DENIED" in str(e) or "403" in str(e):
                    # We continue to the next model just in case it's a specific model restriction
                    pass
                
                continue # Try next model

        # If we get here, all models failed
        logger.error(f"AI Assistant Failed: All models exhausted. Last error: {last_error}")
        return f"AI assistant temporarily unavailable. Last error: {last_error[:100]}"
