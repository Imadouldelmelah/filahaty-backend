import sys
import os
import json
import asyncio

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hybrid_agronomist():
    print("Testing Hybrid Agronomy System (Rules + AI)...\n")
    
    # Context for a Tomato in Growth stage (expert rules exist for this)
    context = {
        "crop": "Tomato",
        "stage": "Growth",
        "weather": "Extremely hot (40°C) and dry",
        "soil": "Sandy Loam",
        "field_size": "5 Hectares"
    }
    
    print(f"Input Context: {json.dumps(context, indent=4)}")
    print("\nExpected Hybrid Behavior:")
    print("- Should mention 'Nitrogen-rich fertilizer' or 'Staking/Trellising' (Expert rules)")
    print("- Should ADAPT the irrigation (Expert says 2-3L, AI should adjust for 40°C heat)")
    
    # Use the existing /ai/advice route which calls the hybrid service
    response = client.post("/ai/advice", json=context)
    
    if response.status_code == 200:
        data = response.json()
        print("\nHybrid AI Response:")
        print("-" * 30)
        print(f"ADVICE: {data['advice']}")
        print("\nACTIONS:")
        for action in data["actions"]:
            print(f"- {action}")
        print("-" * 30)
        
        # Informal checks
        advice_lower = data["advice"].lower()
        actions_str = " ".join(data["actions"]).lower()
        
        has_expert_rule = "nitrogen" in actions_str or "staking" in actions_str or "trellising" in actions_str
        has_ai_adaptation = "heat" in actions_str or "temperature" in actions_str or "40" in actions_str or "irrigation" in actions_str
        
        print(f"\nFound Expert Rule keywords? {'Yes' if has_expert_rule else 'No'}")
        print(f"Found AI Adaptation (to heat)? {'Yes' if has_ai_adaptation else 'No'}")
        
        assert "advice" in data
        assert isinstance(data["actions"], list)
    else:
        print(f"Test Failed: Status code {response.status_code}")
        print(response.content)

if __name__ == "__main__":
    test_hybrid_agronomist()
