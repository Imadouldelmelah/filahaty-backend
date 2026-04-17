import sys
import os
import asyncio
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_agronomist import ai_agronomist

async def test_ai_sensory_reaction():
    print("--- Testing AI Reaction to Dry Soil ---")
    context_dry = {
        "crop_name": "Tomato",
        "current_stage": "Growth",
        "weather": "Sunny, 30°C",
        "soil": "Sandy",
        "field_size": "2 Hectares",
        "monitoring_data": {
            "soil_moisture": 15.5, # Very dry
            "ph": 6.5,
            "temperature": 32.0,
            "humidity": 40.0,
            "N": 50, "P": 30, "K": 40
        }
    }
    
    response = await ai_agronomist.generate_advice(context_dry)
    print(f"Advice: {response['advice']}")
    print(f"Actions: {response['actions']}")
    
    # Check if AI noticed the dry soil
    if "moisture" in response['advice'].lower() or "irrigate" in str(response['actions']).lower():
        print("✅ SUCCESS: AI reacted to low soil moisture.")
    else:
        print("❌ FAILURE: AI ignored low soil moisture.")

    print("\n--- Testing AI Reaction to High pH ---")
    context_ph = {
        "crop_name": "Tomato",
        "current_stage": "Harvest",
        "weather": "Cloudy, 22°C",
        "soil": "Clay",
        "field_size": "1 Hectare",
        "monitoring_data": {
            "soil_moisture": 45.0,
            "ph": 8.5, # Alkaline
            "temperature": 21.0,
            "humidity": 60.0,
            "N": 40, "P": 20, "K": 35
        }
    }
    
    response = await ai_agronomist.generate_advice(context_ph)
    print(f"Advice: {response['advice']}")
    
    if "ph" in response['advice'].lower() or "alkaline" in response['advice'].lower():
        print("✅ SUCCESS: AI reacted to high pH.")
    else:
        print("❌ FAILURE: AI ignored high pH.")

if __name__ == "__main__":
    asyncio.run(test_ai_sensory_reaction())
