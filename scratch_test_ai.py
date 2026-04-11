import asyncio
import os
from services.gemini_service import GeminiService

async def test_ai():
    print("Testing GeminiService locally...")
    try:
        service = GeminiService()
        response = await service.ask_ai("Hello, tell me one tip for tomato farming.")
        print("\nLOCAL AI RESPONSE SUCCESSFUL:")
        print(response)
    except Exception as e:
        print("\nLOCAL TEST FAILED:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_ai())
