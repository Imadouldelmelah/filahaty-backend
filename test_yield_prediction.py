import asyncio
import json
from services.yield_prediction_service import yield_prediction_service

async def test_yield_prediction():
    context = {
        "crop_name": "Wheat",
        "field_size_hectares": 5.0,
        "monitoring_data": {
            "soil_moisture": 45.0,
            "ph": 6.5,
            "N": 60,
            "P": 40,
            "K": 35
        },
        "weather_data": {
            "temperature": 24.0,
            "humidity": 60.0,
            "rain": 5.0
        }
    }
    
    print("TESTING YIELD PREDICTION...")
    result = await yield_prediction_service.predict_yield(context)
    print("PREDICTION RESULT:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_yield_prediction())
