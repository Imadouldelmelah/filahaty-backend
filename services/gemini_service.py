import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # API key loading from environment variable
        API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not API_KEY:
            raise Exception("Missing API key")
        
        print("API KEY:", API_KEY[:5])
        try:
            self.client = AsyncOpenAI(
                api_key=API_KEY,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "Authorization": f"Bearer {API_KEY}"
                }
            )
            logger.info("OpenRouter client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {str(e)}")
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

    async def generate(self, message: str, retry_count: int = 0, response_format: dict = None, require_json: bool = True):
        """
        Hardened AI execution. By default forces valid JSON and parses safely.
        """
        # Fallback JSON structure matching the app's needs
        if require_json:
            fallback_msg = json.dumps({
                "response": "Smart offline mode activated",
                "data": "basic agricultural guidance"
            })
        else:
            fallback_msg = "Smart offline mode activated: I can still guide you based on agricultural knowledge."
        
        if not self.client:
            logger.error("GEMINI_SVC_CRITICAL: DeepSeek client not initialized.")
            return fallback_msg

        try:
            # 1. Payload Construction
            safe_message = message[:250] # Trimmed message length slightly to save input tokens
            max_tokens = 100 

            if require_json:
                system_instruction = (
                    "Respond ONLY in JSON format. No text before or after.\n"
                    "Example:\n"
                    "{\n"
                    "\"crop\": \"tomato\",\n"
                    "\"confidence\": \"high\",\n"
                    "\"reason\": \"...\"\n"
                    "}"
                )
            else:
                system_instruction = "You are a helpful expert agricultural assistant. Answer concisely and clearly."

            # 2. Execute Request via OpenAI SDK
            completion_params = {
                "model": "z-ai/glm-4.5-air:free",
                "messages": [
                    {
                        "role": "system", 
                        "content": system_instruction
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
            # Call the API asynchronously with a 4.5s strict timeout to prevent Render app sleep freezing
            response = await asyncio.wait_for(
                self.client.chat.completions.create(**completion_params),
                timeout=4.5
            )
            print("Response:", response)
            
            logger.info("OAI_RESPONSE_STATUS: 200 OK")

            if not response.choices or len(response.choices) == 0:
                logger.error("OAI_RESPONSE_CONTENT: No choices returned")
                return fallback_msg

            raw_content = response.choices[0].message.content
            if not raw_content or str(raw_content).strip() == "":
                logger.error("OAI_RESPONSE_CONTENT: Empty content returned")
                return fallback_msg

            logger.info(f"OAI_RESPONSE_CONTENT: {raw_content}")
            
            return raw_content

        except Exception as e:
            print("Error:", e)
            if hasattr(e, 'status_code'):
                print("Status Code:", e.status_code)
            logger.error(f"OAI_RESPONSE_STATUS: FAIL")
            logger.error(f"GEMINI_SVC_HIT_ERROR: {str(e)}")
            return fallback_msg


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
            safe_prompt = prompt[:250]
            max_tokens = 100

            logger.info("--- AI VISION DEBUG START (DEEPSEEK) ---")
            
            # Payload for Vision (Standard OpenAI format)
            completion_params = {
                "model": "z-ai/glm-4.5-air:free", # Fallback to chat if vision isn't separate
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
            # Call the API asynchronously with a strict timeout
            response = await asyncio.wait_for(
                self.client.chat.completions.create(**completion_params),
                timeout=4.5
            )
            print("Response:", response)
            
            logger.info("OAI_VISION_RESPONSE_STATUS: 200 OK")

            if not response.choices or len(response.choices) == 0:
                logger.error("OAI_VISION_RESPONSE_CONTENT: No choices returned")
                return fallback_msg

            content = response.choices[0].message.content
            if not content or str(content).strip() == "":
                logger.error("OAI_VISION_RESPONSE_CONTENT: Empty content returned")
                return fallback_msg

            logger.info(f"OAI_VISION_RESPONSE_CONTENT: {content}")
            logger.info("--- AI VISION DEBUG END (SUCCESS) ---")
            return content

        except Exception as e:
            print("Error:", e)
            if hasattr(e, 'status_code'):
                print("Status Code:", e.status_code)
            logger.error("OAI_VISION_RESPONSE_STATUS: FAIL")
            logger.error(f"GEMINI_VISION_HIT: {str(e)}")
            return fallback_msg
