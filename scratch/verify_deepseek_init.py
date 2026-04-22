import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.gemini_service import GeminiService
from dotenv import load_dotenv

# Load .env
load_dotenv('backend/.env')

def test_init():
    print("Testing GeminiService (DeepSeek) initialization...")
    try:
        service = GeminiService()
        if service.client:
            print("SUCCESS: Client initialized.")
            print(f"Base URL: {service.client.base_url}")
        else:
            print("FAILURE: Client NOT initialized.")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_init()
