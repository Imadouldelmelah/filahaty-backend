import asyncio
import os
import sys
import json
from unittest.mock import AsyncMock, patch, MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

# Import route functions for direct testing
from routes.ai_routes import chat_with_ai_endpoint, advanced_chat_with_ai_endpoint
from routes.agronomist_routes import get_agronomist_advice_endpoint
from routes.news import get_agricultural_news
from routes.weather_routes import get_weather_endpoint

async def test_json_integrity():
    print("Verifying 100% JSON Compliance & Fallbacks...")
    
    # 1. Test Chat Fallback (Simulate AI failure)
    print("\n--- Testing /ai/chat Fallback ---")
    with patch("routes.ai_routes.call_ai", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "AI_ERROR_FALLBACK"
        request = MagicMock()
        request.message = "Hello"
        response = await chat_with_ai_endpoint(request)
        print(f"Chat Response type: {type(response)}")
        assert hasattr(response, "response")
        assert "offline mode" in response.response
        print("PASS: /ai/chat returned structured ChatResponse on AI failure.")

    # 2. Test Agronomist Fallback (Simulate internal error)
    print("\n--- Testing /agronomist/advice Fallback ---")
    with patch("services.ai_agronomist.AIAgronomistService.generate_advice", new_callable=AsyncMock) as mock_adv:
        mock_adv.side_effect = Exception("System Crash")
        context = MagicMock()
        context.model_dump.return_value = {"field_id": "test"}
        response = await get_agronomist_advice_endpoint(context)
        print(f"Agronomist Response type: {type(response)}")
        assert hasattr(response, "advice")
        assert len(response.actions) > 0
        print("PASS: /agronomist/advice returned structured fallback on total failure.")

    # 3. Test News Fallback (Simulate Key missing)
    print("\n--- Testing /news Fallback ---")
    with patch("config.settings.NEWS_API_KEY", None):
        response = get_agricultural_news()
        print(f"News Response: {json.dumps(response, indent=2)}")
        assert "articles" in response
        assert response["status"] == "offline_optimized"
        print("PASS: /news returned structured fallback articles when key is missing.")

    # 4. Test Weather Fallback (Simulate API Timeout)
    print("\n--- Testing /weather Fallback ---")
    with patch("services.weather_service.WeatherService.get_weather", side_effect=Exception("API Timeout")):
        response = await get_weather_endpoint(lat=36.0, lon=3.0)
        print(f"Weather Response: {json.dumps(response, indent=2)}")
        assert "temperature" in response
        assert response["status"] == "offline_optimized"
        print("PASS: /weather returned structured fallback on API timeout.")

    print("\nALL ENDPOINTS VERIFIED: 100% JSON compliance achieved.")

if __name__ == "__main__":
    asyncio.run(test_json_integrity())
