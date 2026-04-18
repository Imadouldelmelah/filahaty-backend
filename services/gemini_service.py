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
        # Temporarily disabled to check server startup
        # if not self.api_key:
        #     logger.error("AI call failed: Missing API Key")
        #     return "AI service unavailable (Missing API Key)"
            
        print("AI DISABLED: Returning dummy response")
        return '{"response": "test ok"}'
        
        # try:
        #     url = "https://openrouter.ai/api/v1/chat/completions"
        #     headers = {
        #         "Authorization": "Bearer " + self.api_key,
        #         "Content-Type": "application/json"
        #     }
        #     body = {
        #         "model": "openai/gpt-4o-mini",
        #         "messages": [
        #             {
        #                 "role": "system",
        #                 "content": "You are an agricultural expert specialized in Algeria farming."
        #             },
        #             {
        #                 "role": "user",
        #                 "content": message
        #             }
        #         ]
        #     }
        #     
        #     response = requests.post(url, headers=headers, json=body)
        #     response.raise_for_status()
        #     
        #     print("API response received")
        #     return response.json()["choices"][0]["message"]["content"]
        # 
        # except Exception as e:
        #     # Capture real error for debugging
        #     print("API error:", str(e))
        #     return "AI unavailable, please try again later"

    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg"):
        # Temporarily disabled to check server startup
        print("AI VISION DISABLED: Returning dummy response")
        return {"response": "test ok"}
        
        # if not self.api_key:
        #     logger.error("AI vision call failed: Missing API Key")
        #     return "AI vision analysis unavailable (Missing API Key)"
        #     
        # print("Sending vision prompt to API")
        # 
        # try:
        #     url = "https://openrouter.ai/api/v1/chat/completions"
        #     headers = {
        #         "Authorization": "Bearer " + self.api_key,
        #         "Content-Type": "application/json"
        #     }
        #     body = {
        #         "model": "openai/gpt-4o-mini",
        #         "messages": [
        #             {
        #                 "role": "user",
        #                 "content": [
        #                     {
        #                         "type": "text",
        #                         "text": prompt
        #                     },
        #                     {
        #                         "type": "image_url",
        #                         "image_url": {
        #                             "url": f"data:{mime_type};base64,{base64_image}"
        #                         }
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        #     
        #     response = requests.post(url, headers=headers, json=body)
        #     response.raise_for_status()
        #     
        #     print("Vision API response received")
        #     return response.json()["choices"][0]["message"]["content"]
        # 
        # except Exception as e:
        #     print("Vision API error:", str(e))
        #     return "AI vision analysis temporarily unavailable"
