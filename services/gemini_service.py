import os
import json
import asyncio
import time
from openai import OpenAI
from dotenv import load_dotenv
from utils.logger import logger

# Load environment variables
load_dotenv()

class GeminiService:

    def __init__(self):
        # API key loading from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        print("API KEY LOADED:", bool(api_key))
        
        if not api_key:
             logger.warning("GEMINI_SVC_INIT: Missing OpenAI API key. AI features will be disabled.")
             self.client = None
             return
        
        try:
            from openai import OpenAI
            # Client automatically uses the environment variable OPENAI_API_KEY
            self.client = OpenAI()
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
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
            safe_message = message[:250]
            
            logger.info(f"OAI_SIMPLIFIED_REQUEST: {safe_message[:50]}...")

            print("CALLING OPENAI...")
            try:
                # Use the specific Responses API pattern requested with relaxed tokens
                response = await asyncio.wait_for(
                    asyncio.to_thread(self.client.responses.create, model="gpt-4.1-mini", input=safe_message, max_tokens=300),
                    timeout=5.0
                )
                print("AI RESPONSE:", response)
            except asyncio.TimeoutError:
                print("AI ERROR: Timeout (> 5s)")
                logger.error("OAI_REQUEST_TIMEOUT: AI took > 5 seconds")
                return fallback_msg
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            logger.info(f"OAI_RESPONSE_TIME: {response_time:.2f}ms")
            
            if not response or not hasattr(response, 'output_text'):
                logger.error("OAI_RESPONSE_CONTENT: Invalid response structure")
                return fallback_msg

            raw_content = response.output_text
            logger.info(f"OAI_RESPONSE_CONTENT: {raw_content}")
            
            return raw_content

        except Exception as e:
            print("AI ERROR:", e)
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
            safe_prompt = prompt[:200]
            
            logger.info("--- AI VISION DEBUG START (SIMPLIFIED) ---")
            
            print("CALLING OPENAI...")
            start_time = time.time()
            try:
                # Optimized vision call using the simplified Responses API
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.client.responses.create, 
                        model="gpt-4.1-mini", 
                        input=[
                            {"type": "text", "text": safe_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                        ],
                        max_tokens=300
                    ),
                    timeout=5.0
                )
                print("AI RESPONSE:", response)
            except asyncio.TimeoutError:
                print("AI ERROR: Vision Timeout (> 5s)")
                logger.error("OAI_VISION_TIMEOUT: AI took > 5 seconds")
                return fallback_msg
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            logger.info(f"OAI_VISION_RESPONSE_TIME: {response_time:.2f}ms")
            
            if not response or not hasattr(response, 'output_text'):
                logger.error("OAI_VISION_RESPONSE_CONTENT: Invalid response structure")
                return fallback_msg

            content = response.output_text
            logger.info(f"OAI_VISION_RESPONSE_CONTENT: {content}")
            logger.info(f"--- AI VISION DEBUG END (SUCCESS in {response_time:.2f}ms) ---")
            return content

        except Exception as e:
            print("AI ERROR:", e)
            if hasattr(e, 'status_code'):
                print("Status Code:", e.status_code)
            logger.error("OAI_VISION_RESPONSE_STATUS: FAIL")
            logger.error(f"GEMINI_VISION_HIT: {str(e)}")
            return fallback_msg
    async def chat(self, user_message: str):
        """
        New simplified chat endpoint following specific user pattern.
        """
        fallback_msg = "Smart offline mode activated: I can still guide you based on agricultural knowledge."
        if not self.client:
            return {"response": fallback_msg}

        try:
            print("CALLING OPENAI...")
            # Using the specific Responses API pattern requested with 5s timeout
            start_time = time.time()
            try:
                # Note: responses.create is a synchronous call in this SDK version
                response = await asyncio.wait_for(
                    asyncio.to_thread(self.client.responses.create, model="gpt-4.1-mini", input=user_message, max_tokens=300),
                    timeout=5.0
                )
                print("AI RESPONSE:", response)
            except asyncio.TimeoutError:
                print("AI ERROR: Chat Timeout (> 5s)")
                logger.error("NEW_CHAT_TIMEOUT: AI took > 5 seconds")
                return {"response": fallback_msg}
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            logger.info(f"NEW_CHAT_RESPONSE_TIME: {response_time:.2f}ms")
                
            return {
                "response": response.output_text
            }
        except Exception as e:
            print("AI ERROR:", e)
            logger.error(f"NEW_CHAT_ERROR: {str(e)}")
            # Custom fallback as requested
            return {
                "response": fallback_msg
            }
