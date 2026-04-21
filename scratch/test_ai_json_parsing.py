import sys
import os
import asyncio
from unittest.mock import AsyncMock, patch

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_agronomist import AIAgronomistService

async def test_resilient_parsing():
    print("Testing Resilient JSON Parsing...")
    service = AIAgronomistService()
    
    # 1. Test Markdown-wrapped JSON
    print("\n1. Testing Markdown-wrapped JSON...")
    dirty_json = """
Here is your advice:
```json
{
  "stage": "Growth",
  "tasks": ["Watering"],
  "advice": "Keep it wet",
  "alerts": []
}
```
I hope this helps!
"""
    service._ai.generate = AsyncMock(return_value=dirty_json)
    result = await service.generate_advice({"crop_name": "Tomato", "current_stage": "Growth"})
    assert result["stage"] == "Growth"
    assert result["tasks"] == ["Watering"]
    print("PASS: Extracted JSON from markdown and text.")

    # 2. Test Missing Keys (Auto-fill)
    print("\n2. Testing Missing Keys (Auto-fill)...")
    partial_json = '{"advice": "Some advice"}'
    service._ai.generate = AsyncMock(return_value=partial_json)
    result = await service.generate_advice({"crop_name": "Tomato", "current_stage": "Growth"})
    assert result["advice"] == "Some advice"
    assert "stage" in result
    assert "tasks" in result
    assert "alerts" in result
    print("PASS: Partial JSON auto-filled missing keys.")

    # 3. Test Recovery from Garbage text
    print("\n3. Testing Recovery from Garbage text...")
    garbage_json = "Wait... { \"stage\": \"Flowering\", \"tasks\": [\"Pruning\"], \"advice\": \"Cut it\", \"alerts\": [] } ...End"
    service._ai.generate = AsyncMock(return_value=garbage_json)
    result = await service.generate_advice({"crop_name": "Tomato", "current_stage": "Growth"})
    assert result["stage"] == "Flowering"
    print("PASS: Cleaned garbage text surrounding JSON.")

    # 5. Test Multi-Attempt Retry
    print("\n5. Testing Multi-Attempt Retry...")
    # First call returns garbage, second returns valid JSON
    service._ai.generate = AsyncMock(side_effect=[
        "First call garbage text",
        '{"stage": "Retry", "tasks": ["Success"], "advice": "Worked", "alerts": []}'
    ])
    
    result = await service.generate_advice({"crop_name": "Tomato", "current_stage": "Growth"})
    assert result["stage"] == "Retry"
    assert service._ai.generate.call_count == 2
    print("PASS: Successfully retried and got valid data on second attempt.")

if __name__ == "__main__":
    asyncio.run(test_resilient_parsing())
