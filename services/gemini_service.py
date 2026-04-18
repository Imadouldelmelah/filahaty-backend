import os
import requests
import asyncio
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # API key loading from environment variable
        key = os.getenv("OPENROUTER_API_KEY")
        if not key:
            print("API key missing")
            self.api_key = None
        else:
            self.api_key = key
            print("OpenRouter client initialized")

    async def generate(self, message: str):
        """
        Safe AI execution without crashing server.
        """
        import os
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("AI execution attempted but OPENROUTER_API_KEY is missing.")
            return "AI temporarily unavailable"

        try:
            logger.info(f"AI_EXECUTION: Sending chat completion request to OpenRouter.")
            print("Calling AI...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an agricultural expert specialized in Algeria farming."
                        },
                        {"role": "user", "content": message}
                    ]
                },
                timeout=20
            )
            print(f"AI Response Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"OpenRouter Error: {response.text}")
                return "AI temporarily unavailable"

            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Safe AI Execution Error: {str(e)}")
            return "AI temporarily unavailable"

    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg"):
        """
        Safe Vision AI execution.
        """
        import os
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "AI temporarily unavailable"

        try:
            logger.info(f"AI_EXECUTION: Sending vision request to OpenRouter.")
            print("Calling AI Vision...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                },
                timeout=25
            )
            print(f"AI Vision Response Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"OpenRouter Vision Error: {response.text}")
                return "AI temporarily unavailable"

            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Safe Vision Execution Error: {str(e)}")
            return "AI temporarily unavailable"
