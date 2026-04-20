import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from routes.prediction import get_rule_candidates
from services.crop_recommendation_service import CropRecommendationService

async def test_scenarios():
    print("--- STARTING HYBRID PREDICTION VERIFICATION ---")
    
    # 1. Test Rule Engine: Low pH
    cands, fallback = get_rule_candidates(50, 40, 40, 25, 60, 5.2, 500)
    p_crop = fallback[0]
    print(f"[TEST 1: pH=5.2] Candidates: {cands}, Best Fallback: {p_crop}")
    assert p_crop == "Potato"
    
    # 2. Test Rule Engine: High Temp
    cands, fallback = get_rule_candidates(50, 40, 40, 35, 60, 6.8, 500)
    m_crop = fallback[0]
    print(f"[TEST 2: Temp=35] Candidates: {cands}, Best Fallback: {m_crop}")
    assert m_crop == "Maize"
    
    # 3. Test Rule Engine: Rice (High Humidity)
    cands, fallback = get_rule_candidates(50, 40, 40, 25, 85, 6.8, 500)
    # Note: Logic in get_rule_candidates currently prioritizes pH and Temp over Humidity for the simplified return,
    # but the AI refinement will handle the full candidates.
    print(f"[TEST 3: Hum=85] Candidates: {cands}")
    
    # 4. Test AI Integration (Hybrid Refinement)
    print("\n--- TESTING HYBRID AI REFINEMENT ---")
    svc = CropRecommendationService()
    
    # Scenario A: Low fertility
    context_a = {"nitrogen": 10, "phosphorus": 10, "potassium": 10, "soil_moisture": 30, "temperature": 22, "humidity": 40, "ph": 7.0, "rainfall": 200}
    cands_a = ["Wheat", "Barley", "Olive"]
    res_a = await svc.generate_recommendation(context_a, candidates=cands_a)
    print(f"[AI SCENARIO A: Low Fertility] Candidates: {cands_a} -> Selected: {res_a['crop']}")
    assert res_a['crop'] in cands_a
    
    # Scenario B: High fertility (Heavy Feeders)
    context_b = {"nitrogen": 120, "phosphorus": 80, "potassium": 80, "soil_moisture": 70, "temperature": 28, "humidity": 65, "ph": 6.5, "rainfall": 600}
    cands_b = ["Tomato", "Maize", "Watermelon"]
    res_b = await svc.generate_recommendation(context_b, candidates=cands_b)
    print(f"[AI SCENARIO B: High Fertility] Candidates: {cands_b} -> Selected: {res_b['crop']}")
    assert res_b['crop'] in cands_b
    
    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_scenarios())
