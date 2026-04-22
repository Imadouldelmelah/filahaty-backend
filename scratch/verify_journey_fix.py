import sys
import os
import asyncio

# Setup path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.ai_agronomist import AIAgronomistService

async def test_journey():
    print("Testing Farming Journey Generation...")
    
    agronomist_svc = AIAgronomistService()
    
    # Simulate a journey generation context
    context = {
        "crop_name": "tomato",
        "current_stage": "Growth",
        "weather_data": None,
        "soil": "Sandy"
    }
    
    result = await agronomist_svc.generate_advice(context)
    
    print("\nResult:")
    import json
    print(json.dumps(result, indent=2))
    
    print("\nStatus:", result.get("status"))

if __name__ == "__main__":
    asyncio.run(test_journey())
