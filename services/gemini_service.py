import os
import requests
import asyncio
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # API key loading from environment variable ONLY
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.error("Missing OPENROUTER_API_KEY environment variable")
            raise ValueError("Missing OPENROUTER_API_KEY")

        print("OpenRouter client initialized")

    async def generate(self, message: str):
        # Logging for diagnostic visibility in Render
        print("Sending prompt to API:", message)
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            body = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an agricultural expert specialized in Algeria farming."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            
            print("API response received")
            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            # Capture real error for debugging
            print("API error:", str(e))
            return "AI unavailable, please try again later"

    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg"):
        print("Sending vision prompt to API")
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            body = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            
            print("Vision API response received")
            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            print("Vision API error:", str(e))
            return "AI vision analysis temporarily unavailable"
