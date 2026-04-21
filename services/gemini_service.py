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
        Safe AI execution with dynamic token control, 402 retry logic, and JSON schema enforcement.
        """
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            logger.error("GEMINI_SVC: OPENROUTER_API_KEY is missing.")
            return "AI error: OPENROUTER_API_KEY not configured."

        # Safety truncation of input message to 500 characters
        safe_message = message[:500]

        # Calculate tokens
        max_tokens = self._get_dynamic_tokens(safe_message)
        if retry_count > 0:
            max_tokens = 100 # Force low tokens on retry

        try:
            logger.info(f"GEMINI_SVC: Sending chat request (tokens={max_tokens}, retry={retry_count})")
            payload = {
                "model": "openai/gpt-4o-mini",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert agronomist for Algeria. Be concise."
                    },
                    {"role": "user", "content": safe_message}
                ]
            }

            if response_format:
                payload["response_format"] = response_format

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=20
            )

            # Map status codes to user-friendly messages
            if response.status_code != 200:
                logger.error(f"GEMINI_SVC_ERROR: status={response.status_code}, response={response.text}")
                
                if response.status_code == 401:
                    return "AI error: system authentication failed."
                elif response.status_code == 402:
                    if retry_count == 0:
                        logger.warning("GEMINI_SVC: received 402 Error. Retrying with 100 tokens...")
                        return await self.generate(message, retry_count=1)
                    else:
                        return "AI error: credits exhausted. Please try a shorter question."
                elif response.status_code == 429:
                    return "AI error: system is too busy. Please wait a moment."
                elif response.status_code >= 500:
                    return "AI error: internal provider issue. Please try again shortly."
                else:
                    return f"AI error: system returned status {response.status_code}"

            # Safe JSON parsing and usage logging
            try:
                data = response.json()
                
                # Log usage if present
                usage = data.get("usage", {})
                if usage:
                    logger.info(f"AI_USAGE: tokens={usage.get('total_tokens')}, prompt={usage.get('prompt_tokens')}, completion={usage.get('completion_tokens')}, cost=${usage.get('cost', 0)}")

                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_SVC: JSON parse error: {parse_err}")
                return "AI error: failed to process response, please try again."

        except requests.exceptions.Timeout:
            logger.error("GEMINI_SVC: Request timed out.")
            return "AI error: request timed out. Check your connection."
        except Exception as e:
            logger.error(f"GEMINI_SVC: Unexpected error: {str(e)}")
            return "AI error: please try again."


    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg", retry_count: int = 0, response_format: dict = None):
        """
        Safe Vision AI execution with 402 retry logic and JSON schema support.
        """
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            logger.error("GEMINI_VISION: OPENROUTER_API_KEY is missing.")
            return "AI error: OPENROUTER_API_KEY not configured."

        # Safety truncation of prompt to 500 chars
        safe_prompt = prompt[:500]

        # Vision needs slightly more, but we still cap it.
        max_tokens = 200 if retry_count > 0 else 300 

        try:
            logger.info(f"GEMINI_VISION: Sending vision request (tokens={max_tokens})")
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

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=25
            )

            if response.status_code != 200:
                logger.error(f"GEMINI_VISION_ERROR: status={response.status_code}, response={response.text}")
                
                if response.status_code == 401:
                    return "AI vision error: authentication failed."
                elif response.status_code == 402:
                    if retry_count == 0:
                        logger.warning("GEMINI_VISION: received 402 Error. Retrying with 200 tokens...")
                        return await self.generate_vision(prompt, base64_image, mime_type, retry_count=1)
                    else:
                        return "AI vision error: credits exhausted. Please try a simpler image."
                elif response.status_code == 429:
                    return "AI vision error: system too busy. Please wait a moment."
                elif response.status_code >= 500:
                    return "AI vision error: internal provider issue. Please try again soon."
                else:
                    return f"AI vision error: status {response.status_code}"

            try:
                data = response.json()
                
                # Log usage
                usage = data.get("usage", {})
                if usage:
                    logger.info(f"AI_VISION_USAGE: tokens={usage.get('total_tokens')}, prompt={usage.get('prompt_tokens')}, cost=${usage.get('cost', 0)}")

                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_VISION: JSON parse error: {parse_err}")
                return "AI error: failed to process vision response."

        except requests.exceptions.Timeout:
             logger.error("GEMINI_VISION: Timeout.")
             return "AI error: request timed out."
        except Exception as e:
            logger.error(f"GEMINI_VISION: Error: {str(e)}")
            return "AI error: please try again."

