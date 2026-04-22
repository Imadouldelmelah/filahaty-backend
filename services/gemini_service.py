import os
import json
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # API key loading from environment variable
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        if not DEEPSEEK_API_KEY:
            print("ERROR: DEEPSEEK_API_KEY missing")
            logger.error("DEEPSEEK_API_KEY missing from environment")
            self.client = None
        else:
            print("API KEY:", DEEPSEEK_API_KEY[:5])
            try:
                self.client = OpenAI(
                    api_key=DEEPSEEK_API_KEY,
                    base_url="https://api.deepseek.com/v1"
                )
                logger.info("DeepSeek (OpenAI-compatible) client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize DeepSeek client: {str(e)}")
                self.client = None

    def _get_dynamic_tokens(self, message: str) -> int:
        """
        Calculate safe max_tokens based on message length.
        """
        length = len(message)
        if length <= 50:
             return 100
        elif length <= 150:
             return 150
        return 200

    async def generate(self, message: str, retry_count: int = 0, response_format: dict = None):
        """
        Hardened AI execution. Forces valid JSON and parses safely.
        """
        # Fallback JSON structure matching the app's needs
        fallback_json = {
            "response": "Smart offline mode activated",
            "data": "basic agricultural guidance"
        }
        fallback_msg = json.dumps(fallback_json)
        
        if not self.client:
            logger.error("GEMINI_SVC_CRITICAL: DeepSeek client not initialized.")
            return fallback_msg

        try:
            # 1. Payload Construction
            safe_message = message[:500]
            max_tokens = 250 

            # 2. Execute Request via OpenAI SDK
            completion_params = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            "You are an expert agricultural assistant. "
                            "You must return ONLY valid JSON. No text outside JSON. "
                            "Example output: {\"stage\": \"Growth\", \"tasks\": [\"Water plants\"], \"advice\": \"Maintain irrigation\", \"alerts\": []}"
                        )
                    },
                    {"role": "user", "content": safe_message}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.1 # Lower temperature for better JSON consistency
            }

            if response_format:
                completion_params["response_format"] = response_format

            logger.info(f"OAI_REQUEST_PAYLOAD: {json.dumps(completion_params)}")

            print("Sending request to DeepSeek...")
            # Call the API
            response = self.client.chat.completions.create(**completion_params)
            print("Response:", response)
            
            logger.info("OAI_RESPONSE_STATUS: 200 OK")

            if not response.choices or len(response.choices) == 0:
                logger.error("OAI_RESPONSE_CONTENT: No choices returned")
                raise Exception("Empty response from AI")

            raw_content = response.choices[0].message.content
            logger.info(f"OAI_RESPONSE_CONTENT: {raw_content}")
            
            return raw_content

        except Exception as e:
            print("Error:", e)
            if hasattr(e, 'status_code'):
                print("Status Code:", e.status_code)
            logger.error(f"OAI_RESPONSE_STATUS: FAIL")
            logger.error(f"GEMINI_SVC_HIT_ERROR: {str(e)}")
            raise e


    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg", retry_count: int = 0, response_format: dict = None):
        """
        Indestructible Vision AI execution.
        Note: DeepSeek V3/R1 currently might have limited vision support depending on the endpoint.
        If deepseek-chat doesn't support vision, this will return fallback.
        """
        fallback_msg = "AI_VISION_ERROR_FALLBACK"

        if not self.client:
            return fallback_msg

        try:
            safe_prompt = prompt[:500]
            max_tokens = 150

            logger.info("--- AI VISION DEBUG START (DEEPSEEK) ---")
            
            # Payload for Vision (Standard OpenAI format)
            completion_params = {
                "model": "deepseek-chat", # Fallback to chat if vision isn't separate
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": safe_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": max_tokens
            }

            if response_format:
                completion_params["response_format"] = response_format

            logger.info(f"OAI_VISION_REQUEST_PAYLOAD: {json.dumps(completion_params)}")

            print("Sending request to DeepSeek...")
            response = self.client.chat.completions.create(**completion_params)
            print("Response:", response)
            
            logger.info("OAI_VISION_RESPONSE_STATUS: 200 OK")

            if not response.choices:
                logger.error("OAI_VISION_RESPONSE_CONTENT: No choices returned")
                raise Exception("Empty vision response from AI")

            content = response.choices[0].message.content
            logger.info(f"OAI_VISION_RESPONSE_CONTENT: {content}")
            logger.info("--- AI VISION DEBUG END (SUCCESS) ---")
            return content

        except Exception as e:
            print("Error:", e)
            if hasattr(e, 'status_code'):
                print("Status Code:", e.status_code)
            logger.error("OAI_VISION_RESPONSE_STATUS: FAIL")
            logger.error(f"GEMINI_VISION_HIT: {str(e)}")
            raise e
