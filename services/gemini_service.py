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
        
        # Diagnostic: Try to list models to help the user identify valid ones in Render logs
        try:
            print("Diagnostic: List of available models for this key:")
            # We don't block the startup, but we print for visibility
            # Note: client.models.list() is synchronous in this SDK version
            for model in self.client.models.list():
                if "generateContent" in model.supported_methods:
                    print(f"- {model.name}")
        except Exception as e:
            print(f"Diagnostic: Could not list models (this is likely a key issue): {e}")

    async def generate_response(self, message: str):
        # Logging before the request
        print("Sending prompt to Gemini:", message)
        
        # Prioritized list of modern models (2.0 is the new standard)
        models_to_try = [
            "gemini-2.0-flash", 
            "gemini-1.5-flash-latest", 
            "gemini-1.5-flash"
        ]
        
        last_error = ""
        
        for model_name in models_to_try:
            print(f"Attempting with model: {model_name}...")
            try:
                # Using the exact structure requested by the user
                # Note: Using .aio with await for proper async execution in FastAPI
                response = await asyncio.wait_for(
                    self.client.aio.models.generate_content(
                        model=model_name,
                        contents=[{
                            "role": "user",
                            "parts": [{"text": message}]
                        }]
                    ),
                    timeout=15.0
                )
                
                if hasattr(response, "text") and response.text:
                    print(f"Success with {model_name}")
                    return response.text
                else:
                    print(f"Empty response from {model_name}, trying next...")
                    continue

            except Exception as e:
                last_error = str(e)
                print(f"Model {model_name} failed: {last_error}")
                # If it's a 404 or 503, definitely try the next one
                continue

        # Logging final error to Render logs
        print("Gemini API error (All models exhausted):", last_error)
        # Return a safe fallback to the user
        return "AI assistant temporarily unavailable"
