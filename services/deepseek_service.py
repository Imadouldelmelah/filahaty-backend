import os
import json
import requests
from utils.logger import logger

class DeepSeekR1Service:
    def __init__(self):
        # 1. Load from environment variable
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # 2. Print debug
        print("API KEY LOADED:", bool(self.api_key))
        
        # 3. Add strict validation
        if not self.api_key:
            raise Exception("OpenRouter API key missing")

    def generate_reasoning(self, user_message: str) -> str:
        """
        Generates advanced agricultural reasoning with 10s timeout and 1 retry.
        Uses raw HTTP requests as requested.
        """
        if not self.api_key:
            raise ValueError("DeepSeek R1 Offline: Missing OPENROUTER_API_KEY")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-r1",
            "messages": [
                {"role": "system", "content": "You are an agricultural expert."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }

        # Retry system logic
        max_retries = 2 # Initial attempt + 1 retry
        for attempt in range(max_retries):
            try:
                print("CALLING OPENROUTER...")
                logger.info(f"CALLING OPENROUTER (DeepSeek R1) - Attempt {attempt + 1}...")
                response = requests.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek/deepseek-r1",
                        "messages": [
                            {"role": "user", "content": user_message}
                        ],
                        "max_tokens": 200
                    },
                    timeout=10 # Strict 10s timeout
                )
                
                print("RESPONSE RECEIVED")
                print("STATUS:", response.status_code)
                print("BODY:", response.text)
                
                # 1. Handle API errors properly
                if response.status_code != 200:
                    print("API ERROR:", response.text)
                    return {"response": "AI error, try again later"}
                
                data = response.json()
                
                # 1. Parse & 2. Extract exactly as requested
                ai_text = data["choices"][0]["message"]["content"]
                
                logger.info("OPENROUTER_RESPONSE: Success")
                # 3. Return structured dictionary
                return {"response": ai_text}

            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
                print("ERROR:", e)
                logger.warning(f"OPENROUTER_TIMEOUT: Attempt {attempt + 1} timed out.")
                if attempt == max_retries - 1:
                    logger.error("OPENROUTER_CRITICAL: All retries failed due to timeout.")
                continue # Try next attempt
            except Exception as e:
                print("ERROR:", e)
                logger.error(f"OPENROUTER_ERROR: {str(e)}")
                break # Non-timeout errors don't trigger retry

        # Fallback return matching the same structure
        return {"response": "DeepSeek R1 reasoning is temporarily unavailable. Attempting standard agricultural response."}

# Export for clean usage
deepseek_svc = DeepSeekR1Service()
