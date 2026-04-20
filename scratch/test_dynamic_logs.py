import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.fake_monitoring_service import FakeMonitoringService
from routes.prediction import predict_crop
from models.soil_models import SoilData

async def verify_dynamic_data():
    print("--- STARTING DYNAMIC DATA VERIFICATION ---")
    monitor = FakeMonitoringService()
    
    seen_n = set()
    seen_temp = set()
    
    for i in range(3):
        print(f"\n>> Request {i+1}:")
        data = monitor.get_fake_monitoring_data("test_field")
        
        # Convert to SoilData model as the route expects
        soil_input = SoilData(
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            ph=data['ph'],
            rainfall=data['rainfall']
        )
        
        # Trigger the route logic (which has our new logs)
        await predict_crop(soil_input)
        
        seen_n.add(data['nitrogen'])
        seen_temp.add(data['temperature'])
        
    print("\n--- RESULTS ---")
    print(f"Nitrogen values seen: {seen_n}")
    print(f"Temperature values seen: {seen_temp}")
    
    if len(seen_n) > 1 or len(seen_temp) > 1:
        print("VERIFICATION SUCCESS: Data is dynamic and changing per request.")
    else:
        print("VERIFICATION FAILURE: Data appears constant.")

if __name__ == "__main__":
    asyncio.run(verify_dynamic_data())
