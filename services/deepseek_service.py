import os
import requests
import json
from utils.logger import logger

class DeepSeekR1Service:
    def generate_reasoning(self, user_message: str) -> dict:
        """
        Generates advanced reasoning. Safe: Keys loaded only at call time.
        """
        # 1. Load inside function
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # 2. Early return if missing
        if not api_key:
            print("WARNING: No OpenRouter API key found.")
            return {"response": "no key"}

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://filahaty.com", # Optional for OpenRouter
            "X-Title": "Filahaty"
        }

        payload = {
            "model": "deepseek/deepseek-r1",
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 200
        }

        # Attempt call
        try:
            print("CALLING OPENROUTER...")
            response = requests.post(
                base_url,
                headers=headers,
                json=payload,
                timeout=10 
            )
            
            print("RESPONSE RECEIVED")
            print("STATUS:", response.status_code)
            
            if response.status_code != 200:
                print("API ERROR:", response.text)
                return {"response": "AI error, try again later"}
            
            data = response.json()
            ai_text = data["choices"][0]["message"]["content"]
            
            return {"response": ai_text}

        except Exception as e:
            print("ERROR:", e)
            return {"response": "AI error, try again later"}

def get_deepseek_svc():
    # Return a lightweight instance; actual work/checks happen inside the method
    return DeepSeekR1Service()
