import asyncio
import os
import sys
import json
from unittest.mock import AsyncMock, patch, MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd()))

from services.hybrid_controller import HybridDecisionController
from models.chat_models import ChatResponse

async def test_stabilization():
    print("Verifying Zero-Null Stabilization...")
    
    # 1. Test Controller Deep Repair
    print("\n--- Testing Controller Deep Repair ---")
    
    def baseline_with_nulls():
        return {
            "crop": None,
            "tasks": None,
            "status": "test",
            "other_field": None
        }
    
    async def ai_stub():
        return "{}"

    result = await HybridDecisionController.execute(
        baseline_func=baseline_with_nulls,
        ai_func=ai_stub,
        schema_repair_keys=["crop", "tasks"],
        feature_name="TEST_NULLS"
    )
    
    print(f"Controller Result: {json.dumps(result, indent=2)}")
    
    # Assertions
    assert result["crop"] == "System standard"
    assert result["tasks"] == []
    assert result["other_field"] == ""
    assert "null" not in json.dumps(result)
    print("PASS: Controller repaired all missing and null fields.")

    # 2. Test ChatResponse Model Defaults
    print("\n--- Testing ChatResponse Model Defaults ---")
    chat_fallback = ChatResponse(response="Fallback text")
    json_output = chat_fallback.model_dump_json()
    print(f"ChatResponse JSON: {json_output}")
    
    assert "null" not in json_output
    data = json.loads(json_output)
    assert data["error"] == ""
    assert data["message"] == ""
    assert data["status"] == "ai_optimized"
    print("PASS: ChatResponse model has zero null fields.")

    print("\nZERO-NULL STABILIZATION VERIFIED.")

if __name__ == "__main__":
    asyncio.run(test_stabilization())
