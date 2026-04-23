import asyncio
import os
import sys
import json
from unittest.mock import AsyncMock, patch

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

from services.gemini_service import GeminiService

async def verify_safe_ai():
    print("Verifying Ultra-Safe AI Integration...")
    service = GeminiService()
    
    # Check current API KEY setup
    os.environ["OPENAI_API_KEY"] = "sk-safe-test-key"

    print("\n--- Testing Token Limit & Simple Prompt ---")
    # We mock requests.post to check the PAYLOAD
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Test"}}]
        }
        
        await service.generate("Hello world")
        
        # Verify payload
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]
        
        print(f"Payload Max Tokens: {payload['max_tokens']}")
        print(f"System Prompt: {payload['messages'][0]['content']}")
        
        assert payload["max_tokens"] == 100
        assert "Expert Agronomist" in payload["messages"][0]["content"]
        print("PASS: max_tokens is 100 and prompt is simplified.")

    print("\n--- Testing 'choices' Validation ---")
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        # Simulated malformed response (missing choices)
        mock_post.return_value.json.return_value = {"error": "quota exceeded"} 
        
        response = await service.generate("Trigger error")
        print(f"Response on missing choices: {response}")
        
        assert response == "AI_ERROR_FALLBACK"
        print("PASS: Missing 'choices' correctly triggered fallback.")

    print("\nULTRA-SAFE AI INTEGRATION VERIFIED.")

if __name__ == "__main__":
    asyncio.run(verify_safe_ai())
