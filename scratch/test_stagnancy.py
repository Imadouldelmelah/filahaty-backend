import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from routes.prediction import predict_crop, DIVERSITY_CACHE
from models.soil_models import SoilData

async def test_stagnancy_trigger():
    print("--- STARTING STAGNANCY DETECTION TEST ---")
    
    # Clear history
    DIVERSITY_CACHE["global_history"] = []
    
    # Trigger 5 requests with same pH (forces Potato override) but different NPK
    for i in range(5):
        n_val = 10 + (i * 10)
        print(f"\n>> Request {i+1} (N={n_val}, ph=5.2):")
        data = SoilData(
            nitrogen=n_val,
            phosphorus=40,
            potassium=40,
            temperature=25,
            humidity=60,
            ph=5.2,
            rainfall=500
        )
        
        response = await predict_crop(data)
        
        is_stagnant = response["validation"]["is_stagnant"]
        print(f"   Result: {response['crop']}, Stagnant: {is_stagnant}")
        if is_stagnant:
            print(f"   [!] WARNING RECEIVED: {response['validation']['logic_warning']}")

    if is_stagnant:
        print("\nVERIFICATION SUCCESS: Stagnancy detection correctly triggered.")
    else:
        print("\nVERIFICATION FAILURE: Stagnancy warning never triggered.")

if __name__ == "__main__":
    asyncio.run(test_stagnancy_trigger())
