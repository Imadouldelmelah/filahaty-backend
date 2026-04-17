import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.agronomy_engine import get_crop_plan

def test_agronomy_engine():
    print("Testing Agronomy Engine...\n")
    
    crops_to_test = ["tomato", "pepper", "cucumber"]
    
    for crop in crops_to_test:
        print(f"--- Testing Crop: {crop} ---")
        plan = get_crop_plan(crop)
        print(json.dumps(plan, indent=4))
        print("\n")

if __name__ == "__main__":
    test_agronomy_engine()
