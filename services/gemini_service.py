import os
import asyncio
from google import genai
from dotenv import load_dotenv

# Load environment variables (needed to ensure os.getenv works locally)
load_dotenv()

class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing")

        # Official Google GenAI Client
        self.client = genai.Client(api_key=api_key)

    async def generate_response(self, message: str):
        """
        Officially compliant Gemini 2.0 Flash implementation.
        Uses non-blocking .aio for high performance.
        """
        # Using the exact model and parameter format requested
        response = await self.client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=message
        )

        return response.text
