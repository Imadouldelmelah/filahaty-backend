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

        # Debug: log key presence
        print(f"[GEMINI_SVC] OPENROUTER_API_KEY present: {bool(api_key)}")
        logger.info(f"GEMINI_SVC: OPENROUTER_API_KEY present: {bool(api_key)}")

        if not api_key:
            logger.error("GEMINI_SVC: OPENROUTER_API_KEY is missing.")
            return "AI error: OPENROUTER_API_KEY not configured."

        try:
            logger.info("GEMINI_SVC: Sending chat completion request to OpenRouter.")
            print("[GEMINI_SVC] Calling OpenRouter...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert agronomist for Algeria. Be concise."
                        },
                        {"role": "user", "content": message}
                    ]
                },
                timeout=20
            )

            # Debug: log status and raw response
            print(f"[GEMINI_SVC] Response status code: {response.status_code}")
            print(f"[GEMINI_SVC] Response text: {response.text}")
            logger.info(f"GEMINI_SVC: status={response.status_code}")
            logger.debug(f"GEMINI_SVC: raw_response={response.text}")

            if response.status_code != 200:
                logger.error(f"GEMINI_SVC: OpenRouter error {response.status_code}: {response.text}")
                return f"AI error: OpenRouter returned {response.status_code} — {response.text}"

            # Safe JSON parsing
            try:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_SVC: JSON parse error: {parse_err} | raw: {response.text}")
                return "AI error: please try again"

        except requests.exceptions.Timeout:
            logger.error("GEMINI_SVC: Request to OpenRouter timed out.")
            return "AI error: request timed out, please try again"
        except Exception as e:
            logger.error(f"GEMINI_SVC: Unexpected error: {str(e)}")
            return "AI error: please try again"


    async def generate_vision(self, prompt: str, base64_image: str, mime_type: str = "image/jpeg"):
        """
        Safe Vision AI execution.
        """
        import os
        import requests

        api_key = os.getenv("OPENROUTER_API_KEY")

        # Debug: log key presence
        print(f"[GEMINI_VISION] OPENROUTER_API_KEY present: {bool(api_key)}")
        logger.info(f"GEMINI_VISION: OPENROUTER_API_KEY present: {bool(api_key)}")

        if not api_key:
            logger.error("GEMINI_VISION: OPENROUTER_API_KEY is missing.")
            return "AI error: OPENROUTER_API_KEY not configured."

        try:
            logger.info("GEMINI_VISION: Sending vision request to OpenRouter.")
            print("[GEMINI_VISION] Calling OpenRouter Vision...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "max_tokens": 600,
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

            # Debug: log status and raw response
            print(f"[GEMINI_VISION] Response status code: {response.status_code}")
            print(f"[GEMINI_VISION] Response text: {response.text}")
            logger.info(f"GEMINI_VISION: status={response.status_code}")
            logger.debug(f"GEMINI_VISION: raw_response={response.text}")

            if response.status_code != 200:
                logger.error(f"GEMINI_VISION: OpenRouter error {response.status_code}: {response.text}")
                return f"AI error: OpenRouter vision returned {response.status_code} — {response.text}"

            # Safe JSON parsing
            try:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, ValueError) as parse_err:
                logger.error(f"GEMINI_VISION: JSON parse error: {parse_err} | raw: {response.text}")
                return "AI error: please try again"

        except requests.exceptions.Timeout:
            logger.error("GEMINI_VISION: Request to OpenRouter timed out.")
            return "AI error: request timed out, please try again"
        except Exception as e:
            logger.error(f"GEMINI_VISION: Unexpected error: {str(e)}")
            return "AI error: please try again"

