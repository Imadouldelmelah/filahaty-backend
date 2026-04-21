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
        Indestructible AI execution. Guarantees a string return, never throws.
        """
        fallback_msg = "AI_ERROR_FALLBACK"
        
        try:
            # 1. API Key Debug
            api_key = os.getenv("OPENROUTER_API_KEY")
            key_exists = bool(api_key)
            
            # 2. Payload Construction (TASK 1: max_tokens=100)
            safe_message = message[:500]
            max_tokens = 100 

            payload = {
                "model": "openai/gpt-4o-mini",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "system",
                        "content": "Expert Agronomist. Concise expert answers only." # TASK 2: Simple prompt
                    },
                    {"role": "user", "content": safe_message}
                ]
            }
            if response_format:
                payload["response_format"] = response_format

            # Debug EVERYTHING BEFORE REQUEST
            logger.info("--- AI DEBUG START ---")
            logger.info(f"API_KEY_PRESENT: {key_exists}")
            logger.info(f"MODEL: {payload.get('model')}")
            logger.info(f"MAX_TOKENS: {payload.get('max_tokens')}")

            if not key_exists:
                logger.error("GEMINI_SVC_CRITICAL: API Key missing.")
                return fallback_msg

            # 3. Execute Request
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=18 # Reduced timeout for faster failure
            )

            # Debug EVERYTHING AFTER REQUEST
            logger.info(f"STATUS_CODE: {response.status_code}")
            
            # 4. Immediate Fallback if not 200 (TASK 1 & 2)
            if response.status_code != 200:
                print("AI ERROR:", response.text)
                logger.error(f"AI_FAILURE: Status {response.status_code}. Returning fallback.")
                
                # Internal retry logic still allowed for 402
                if response.status_code == 402 and retry_count == 0:
                    logger.warning("Retrying with lower tokens...")
                    return await self.generate(message, retry_count=1, response_format=response_format)
                
                return fallback_msg

            # 5. Safe Parsing (TASK 4: Validate choices)
            try:
                data = response.json()
                
                if "choices" not in data or not data["choices"]:
                    logger.error("GEMINI_SVC_VALIDATION: 'choices' missing in response.")
                    return fallback_msg

                usage = data.get("usage", {})
                if usage:
                    logger.info(f"AI_USAGE: tokens={usage.get('total_tokens')}, cost=${usage.get('cost', 0)}")
                
                content = data["choices"][0]["message"]["content"]
                logger.info("--- AI DEBUG END (SUCCESS) ---")
                return content
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_SVC_PARSE_ERROR: {parse_err}")
                return fallback_msg

        except Exception as e: # TASK 3: Never throw exception
            logger.error(f"GEMINI_SVC_URGENT_HARDENING_HIT: {str(e)}")
            return fallback_msg


    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg", retry_count: int = 0, response_format: dict = None):
        """
        Indestructible Vision AI execution. Guarantees a string return, never throws.
        """
        fallback_msg = "AI_VISION_ERROR_FALLBACK"

        try:
            # 1. API Key Debug
            api_key = os.getenv("OPENROUTER_API_KEY")
            key_exists = bool(api_key)

            # 2. Payload Debug
            safe_prompt = prompt[:500]
            max_tokens = 100 # TASK 1: max_tokens=100

            payload = {
                "model": "openai/gpt-4o-mini",
                "max_tokens": max_tokens,
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
                ]
            }
            if response_format:
                payload["response_format"] = response_format

            # Debug EVERYTHING BEFORE REQUEST
            logger.info("--- AI VISION DEBUG START ---")
            logger.info(f"API_KEY_PRESENT: {key_exists}")
            logger.info(f"MODEL: {payload.get('model')}")

            if not key_exists:
                logger.error("GEMINI_VISION_CRITICAL: API Key missing.")
                return fallback_msg

            # 3. Execute Request
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=25
            )

            # Debug EVERYTHING AFTER REQUEST
            logger.info(f"STATUS_CODE: {response.status_code}")

            # 4. Immediate Fallback if not 200 (TASK 1 & 2)
            if response.status_code != 200:
                print("AI ERROR:", response.text)
                logger.error(f"AI_VISION_FAILURE: Status {response.status_code}. Returning fallback.")
                
                if response.status_code == 402 and retry_count == 0:
                    logger.warning("Retrying vision with lower tokens...")
                    return await self.generate_vision(prompt, base64_image, mime_type, retry_count=1, response_format=response_format)
                
                return fallback_msg

            # 5. Safe Parsing (TASK 4: Validate choices)
            try:
                data = response.json()
                
                if "choices" not in data or not data["choices"]:
                    logger.error("GEMINI_VISION_VALIDATION: 'choices' missing.")
                    return fallback_msg

                usage = data.get("usage", {})
                if usage:
                    logger.info(f"AI_VISION_USAGE: tokens={usage.get('total_tokens')}, cost=${usage.get('cost', 0)}")
                
                content = data["choices"][0]["message"]["content"]
                logger.info("--- AI VISION DEBUG END (SUCCESS) ---")
                return content
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_VISION_PARSE_ERROR: {parse_err}")
                return fallback_msg

        except Exception as e: # TASK 3: Never throw exception
            logger.error(f"GEMINI_VISION_URGENT_HARDENING_HIT: {str(e)}")
            return fallback_msg

