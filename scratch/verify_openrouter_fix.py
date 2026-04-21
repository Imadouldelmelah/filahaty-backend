import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.gemini_service import GeminiService

async def test_402_retry():
    print("Testing 402 Retry Logic...")
    service = GeminiService()
    
    # Mocking requests.post
    mock_response_402 = MagicMock()
    mock_response_402.status_code = 402
    
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "choices": [{"message": {"content": "Retry successful response"}}]
    }
    
    with patch('requests.post') as mock_post:
        # First call returns 402, second returns 200
        mock_post.side_effect = [mock_response_402, mock_response_200]
        
        result = await service.generate("Hello world")
        print(f"Result (Should be successful): {result}")
        
        # Verify it was called twice
        assert mock_post.call_count == 2
        print("PASS: Called twice (Retry worked)")
        
        # Verify second call used 100 tokens
        second_call_json = mock_post.call_args_list[1][1]['json']
        print(f"Second call tokens: {second_call_json['max_tokens']}")
        assert second_call_json['max_tokens'] == 100
        print("PASS: Second call used 100 tokens")

async def test_402_fallback():
    print("\nTesting 402 Fallback Logic...")
    service = GeminiService()
    
    mock_response_402 = MagicMock()
    mock_response_402.status_code = 402
    
    with patch('requests.post') as mock_post:
        # Both calls return 402
        mock_post.side_effect = [mock_response_402, mock_response_402]
        
        result = await service.generate("Hello world")
        print(f"Result (Should be fallback): {result}")
        assert "AI error: credits exhausted" in result
        print("PASS: Fallback triggered correctly")

async def test_dynamic_tokens():
    print("\nTesting Dynamic Token Calculation...")
    service = GeminiService()
    
    # Simple
    assert service._get_dynamic_tokens("hi") == 100
    print("PASS: Simple msg -> 100")
    
    # Medium
    assert service._get_dynamic_tokens("a" * 60) == 150
    print("PASS: Medium msg -> 150")
    
    # Complex
    assert service._get_dynamic_tokens("a" * 160) == 200
    print("PASS: Complex msg -> 200")

async def test_truncation():
    print("\nTesting Message Truncation...")
    from unittest.mock import AsyncMock
    from services.ai_agronomist import AIAgronomistService
    service = AIAgronomistService()
    
    long_msg = "A" * 1000
    # Use AsyncMock for the async generate method
    service._ai.generate = AsyncMock(return_value="resp")
    
    await service.generate_advanced_chat({}, long_msg)
    
    # Get the prompt sent to AI
    call_args = service._ai.generate.call_args[0][0]
    # AIAgronomist truncates to 200 before sending
    assert "Farmer says: " + ("A" * 200) in call_args
    assert ("A" * 201) not in call_args
    print("PASS: AIAgronomist truncated msg to 200")

async def test_history_limit():
    print("\nTesting History Limiting...")
    from unittest.mock import AsyncMock
    from services.ai_agronomist import AIAgronomistService
    service = AIAgronomistService()
    
    # Mock tracking service
    with patch('services.tracking_service.TrackingService') as mock_tracking:
        mock_inst = mock_tracking.return_value
        mock_inst.get_progress.return_value = {
            "history": [
                {"action": "Action 1", "timestamp": "1"},
                {"action": "Action 2", "timestamp": "2"},
                {"action": "Action 3", "timestamp": "3"}
            ]
        }
        
        service._ai.generate = AsyncMock(return_value="{}")
        
        await service.generate_advice({"journey_id": "123"})
        
        call_args = service._ai.generate.call_args[0][0]
        # Only last 2 history items included
        assert "Action 1" not in call_args
        assert "Action 2" in call_args
        assert "Action 3" in call_args
        print("PASS: Only last 2 history items included")

async def test_error_mapping():
    print("\nTesting Error Code Mapping...")
    service = GeminiService()
    
    codes = {
        401: "system authentication failed",
        429: "system is too busy",
        500: "internal provider issue"
    }
    
    for code, expected_msg in codes.items():
        mock_resp = MagicMock()
        mock_resp.status_code = code
        mock_resp.text = f"Internal {code} error"
        
        with patch('requests.post', return_value=mock_resp):
            result = await service.generate("Hi")
            print(f"Code {code} -> {result}")
            assert expected_msg in result
            print(f"PASS: Code {code} mapped correctly")

async def test_usage_logging():
    print("\nTesting Usage Logging...")
    service = GeminiService()
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "usage": {"total_tokens": 50, "prompt_tokens": 30, "completion_tokens": 20, "cost": 0.005},
        "choices": [{"message": {"content": "Hello!"}}]
    }
    
    with patch('requests.post', return_value=mock_resp):
        with patch('utils.logger.logger.info') as mock_log:
            await service.generate("Hi")
            # Check if usage was logged
            log_msgs = [c[0][0] for c in mock_log.call_args_list]
            usage_logged = any("AI_USAGE: tokens=50" in msg for msg in log_msgs)
            assert usage_logged
            print("PASS: Usage metrics logged correctly")

if __name__ == "__main__":
    asyncio.run(test_402_retry())
    asyncio.run(test_402_fallback())
    asyncio.run(test_dynamic_tokens())
    asyncio.run(test_truncation())
    asyncio.run(test_history_limit())
    asyncio.run(test_error_mapping())
    asyncio.run(test_usage_logging())
