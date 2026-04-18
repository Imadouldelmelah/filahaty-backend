import asyncio
import json
from services.unified_ai_brain import unified_ai_brain
from services.tracking_service import tracking_service

async def test_unified_brain():
    print("TESTING UNIFIED AI BRAIN SYSTEM...")
    
    # 1. Setup a mock field
    field_id = tracking_service.start_journey(
        crop_name="Potatoes", 
        start_date="2026-03-01", 
        lat=36.75, 
        lon=3.05
    )
    print(f"Mock journey started: {field_id}")
    
    # 2. Trigger Unified Intelligence Synthesis
    try:
        print("\nSynthesizing Unified Intelligence package...")
        intelligence = await unified_ai_brain.get_unified_intelligence(field_id)
        
        # 3. Verify Structure
        keys = ["health", "yield_projection", "decision", "advice", "context"]
        missing = [k for k in keys if k not in intelligence]
        
        if missing:
            print(f"FAILURE: Missing intelligence keys: {missing}")
        else:
            print("SUCCESS: All localized intelligence modules synthesized.")
            print("\nSAMPLE INTELLIGENCE PACKET:")
            # Truncate some values for readability in terminal
            summary = {
                "health_status": intelligence["health"]["status"],
                "expected_yield": intelligence["yield_projection"]["expected_yield"],
                "primary_decision": intelligence["decision"]["decision"],
                "advice_summary": intelligence["advice"]["advice"][:100] + "..."
            }
            print(json.dumps(summary, indent=2))
            
    except Exception as e:
        print(f"ERROR: Synthesis failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_unified_brain())
