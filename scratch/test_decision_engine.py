import sys
import os
import asyncio
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_decision_engine import ai_decision_engine

async def test_decision_engine():
    print("--- Testing AI Decision Engine ---")
    
    # 1. Dry Soil Scenario
    context_dry = {
        "crop_name": "Wheat",
        "current_stage": "Tillering",
        "weather_data": {
            "temperature": 32.0,
            "humidity": 40.0,
            "rain": 0.0
        },
        "monitoring_data": {
            "soil_moisture": 18.0, # Very dry
            "ph": 6.8,
            "N": 40, "P": 30, "K": 35,
            "temperature": 34.0,
            "humidity": 38.0
        }
    }
    
    print("\nEvaluating Scenario 1: Extremely Dry Soil & Hot Weather")
    result_dry = await ai_decision_engine.generate_decision(context_dry)
    print(json.dumps(result_dry, indent=2))

    # 2. Impending Rain Scenario
    context_rain = {
        "crop_name": "Tomato",
        "current_stage": "Fruiting",
        "weather_data": {
            "temperature": 24.0,
            "humidity": 85.0,
            "rain": 12.0 # Heavy rain
        },
        "monitoring_data": {
            "soil_moisture": 60.0, # Healthy moisture
            "ph": 6.5,
            "N": 50, "P": 40, "K": 60,
            "temperature": 23.0,
            "humidity": 80.0
        }
    }
    
    print("\nEvaluating Scenario 2: Impending Heavy Rain & Healthy Moisture")
    result_rain = await ai_decision_engine.generate_decision(context_rain)
    print(json.dumps(result_rain, indent=2))

if __name__ == "__main__":
    asyncio.run(test_decision_engine())
