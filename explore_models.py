import asyncio
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

async def list_models():
    print("Listing available models for the current API key...")
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        for model in client.models.list():
            print(f"- {model.name} (Support: {model.supported_methods})")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
